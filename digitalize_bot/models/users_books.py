from datetime import date

from sqlalchemy import Column, DateTime, Integer, ForeignKey, func, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from digitalize_bot.db import metadata, Base


class UsersBooks(Base):
    __tablename__ = 'users_books'
    id: int = Column(Integer, primary_key=True)

    book_id: int = Column(Integer, ForeignKey('book.id'), default=1)
    user_id: int = Column(Integer, ForeignKey('user.id'), default=1)

    issued_at: date = Column(DateTime, default=func.now())
    returned_at: date = Column(DateTime, default=None)

    book = relationship("Book", back_populates="users")
    user = relationship("User", back_populates="books")


class UsersBooksCrud:
    def __init__(self, model):
        self.model = model

    async def get_users_books_count(
            self,
            session: AsyncSession
    ):
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        await session.close()
        return result

    async def get_all_users_books(
            self,
            session: AsyncSession
    ):
        stmt = select(self.model)
        result = await session.execute(stmt)
        result = [dict(r._mapping)[f'{self.model}'] for r in result]
        await session.close()
        return result

    async def create_users_books(
            self,
            session: AsyncSession,
            data: dict
    ):
        """
        I.E. Borrow book
        :param session:
        :param data:
        :return:
        """
        stmt = insert(self.model).values(**data)

        await session.execute(stmt)
        await session.commit()
        await session.close()
        return data

    async def update_users_books(
            self,
            session: AsyncSession,
            data: dict
    ):
        """
        I.E. Return book
        :param session:
        :param data:
        :return:
        """
        stmt = update(self.model).values(**data).\
            where(
                (self.model.book_id == data['book_id']) &
                (self.model.user_id == data['user_id'])
            )
        await session.execute(stmt)

        await session.commit()
        await session.close()



users_books = UsersBooksCrud(UsersBooks)
