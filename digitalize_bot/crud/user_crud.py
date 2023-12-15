import re

from sqlalchemy.ext.asyncio.session import AsyncSession

from .base_crud import BaseCrud
from digitalize_bot.models.categories import Category
from digitalize_bot.models.users import User


class UserCrud(BaseCrud):
    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError('Invalid email')
        return email

    async def create_user(
            self,
            session: AsyncSession,
            data: dict
    ):
        data['email'] = self.validate_email(data['email'])
        await self.create(session, data)
        return data



user = UserCrud(User)
