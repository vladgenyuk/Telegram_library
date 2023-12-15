from sqlalchemy import select,  and_
from sqlalchemy.ext.asyncio.session import AsyncSession

from digitalize_bot.models.categories import Category
from digitalize_bot.models.users_books import UsersBooks
from digitalize_bot.models.books import Book


from .base_crud import BaseCrud


class BookCrud(BaseCrud):
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
        ).group_by(Book.id)
        result = await session.execute(stmt)
        result = [dict(r._mapping) for r in result]
        await session.close()
        return result

    async def get_all_books(
            self,
            session: AsyncSession
    ):
        stmt = select(Book, Category.title, UsersBooks).\
            join(Category, Book.category_id == Category.id).\
            join(UsersBooks, UsersBooks.book_id == Book.id, isouter=True).\
            where(Book.status == 'in_library').\
            group_by(Book.id)
        result = await session.execute(stmt)
        ans = []
        for r in result:
            mapping = dict(r._mapping)
            book_obj = mapping['Book']
            book_obj.category_title = mapping['title']  # only cat_title added
            ans.append(book_obj)

        await session.close()
        return ans


book = BookCrud(Book)
