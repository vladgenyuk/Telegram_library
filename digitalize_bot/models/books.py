from datetime import datetime

from sqlalchemy import select, insert, Column, Integer, String, func, ForeignKey, and_
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from digitalize_bot.db import metadata, Base
from digitalize_bot.models.categories import Category
from digitalize_bot.models.users_books import UsersBooks


class Book(Base):
    __tablename__ = 'book'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))
    position_number: int = Column(Integer)
    category_id: int = Column(Integer, ForeignKey('category.id'))

    users = relationship('UsersBooks', back_populates='book')


class BookCrud:
    def __init__(self, model):
        self.model = model

    async def get_my_books(
            self,
            session: AsyncSession,
            user_id: int
    ):
        stmt = select(Book.id, Book.title, UsersBooks.issued_at, UsersBooks.returned_at). \
            join(Book, UsersBooks.book_id == Book.id).\
            where(and_(
                UsersBooks.user_id == user_id,
                UsersBooks.returned_at == None
            )
        )
        result = await session.execute(stmt)
        result = [dict(r._mapping) for r in result]
        await session.close()
        return result

    async def get_book_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.close()
        return result.scalar_one_or_none()

    async def get_book_count(
            self,
            session: AsyncSession
    ):
        stmt = select(func.count()).select_from(Book)
        result = await session.execute(stmt)
        await session.close()
        return result

    async def get_all_books(
            self,
            session: AsyncSession
    ):
        stmt = select(Book, Category.title, UsersBooks).\
            join(Category, Book.category_id == Category.id).\
            join(UsersBooks, UsersBooks.book_id == Book.id, isouter=True).\
            group_by(Book.id)
        result = await session.execute(stmt)
        ans = []
        for r in result:  # result = [dict(r._mapping)['Book'] for r in result]
            mapping = dict(r._mapping)
            book_obj = mapping['Book']
            book_obj.category_title = mapping['title']  # only cat_title added
            ans.append(book_obj)

        await session.close()
        return ans

    async def create_book(
            self,
            session: AsyncSession,
            data: dict
    ):
        data = {
            'title': f'«Чистый код. Создание, анализ и рефакторинг»Автор Роберт К. Мартин',
            'position_number': 1,
            'category_id': 3
        }
        stmt = insert(Book).values(**data)
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            print(e.detail)
        finally:
            await session.close()


book = BookCrud(Book)
