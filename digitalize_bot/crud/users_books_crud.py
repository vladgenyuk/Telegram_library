from sqlalchemy import select,  insert, func, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from digitalize_bot.models.books import Book
from digitalize_bot.models.users_books import UsersBooks


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
        result = [dict(r._mapping) for r in result]
        await session.close()
        return result

    async def create_users_books(
            self,
            session: AsyncSession,
            data: dict
    ):  # Borrow
        stmt = select(Book).where(Book.id == data['book_id'])
        book = await session.execute(stmt)
        if book.scalar_one_or_none().status == 'borrowed':
            raise ValueError("The book is already borrowed")
        stmt = insert(self.model).values(**data)
        stmt2 = update(Book).values(status='borrowed').where(Book.id == data['book_id'])
        await session.execute(stmt)
        await session.execute(stmt2)
        await session.commit()
        await session.close()
        return data

    async def update_users_books(
            self,
            session: AsyncSession,
            data: dict
    ):  # Return
        stmt = update(self.model).values(**data).\
            where(
                (self.model.book_id == data['book_id']) &
                (self.model.user_id == data['user_id'])
            )
        stmt2 = update(Book).values(status='in_library').where(Book.id == data['book_id'])
        await session.execute(stmt)
        await session.execute(stmt2)

        await session.commit()
        await session.close()

    async def get_history(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(UsersBooks, Book.title).\
            join(Book, Book.id == UsersBooks.book_id).\
            where(UsersBooks.user_id == id).\
            group_by(Book.id)
        result = await session.execute(stmt)
        result = [dict(r._mapping) for r in result]
        await session.close()
        return result


users_books = UsersBooksCrud(UsersBooks)
