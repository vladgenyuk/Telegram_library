import re
from datetime import date

from sqlalchemy import select, insert, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio.session import AsyncSession

from digitalize_bot.db import metadata, Base


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(length=100))
    last_name: str = Column(String(length=100))
    email: str = Column(String(length=100), unique=True)
    registered_at: date = Column(DateTime, default=func.now())

    books = relationship('UsersBooks', back_populates='user')


class UserCrud:
    def __init__(self, model):
        self.model = model

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError('Invalid email')
        return email

    async def get_user_count(
            self,
            session: AsyncSession
    ):
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        await session.close()
        return result

    async def get_all_users(
            self,
            session: AsyncSession
    ):
        stmt = select(self.model)
        result = await session.execute(stmt)
        result = [dict(r._mapping)[f'{self.model}'] for r in result]
        await session.close()
        return result

    async def create_user(
            self,
            session: AsyncSession,
            data: dict
    ):
        data['email'] = self.validate_email(data['email'])
        stmt = insert(self.model).values(**data)

        await session.execute(stmt)
        await session.commit()
        return data

    async def get_user_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.close()
        return result.scalar_one_or_none()


user = UserCrud(User)
