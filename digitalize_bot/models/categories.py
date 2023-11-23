from datetime import date, datetime

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import Column, Integer, String, func

from digitalize_bot.db import metadata, Base


class Category(Base):
    __tablename__ = 'category'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))# , unique=True)


class CategoryCrud:
    def __init__(self, model):
        self.model = model

    async def get_category_count(
            self,
            session: AsyncSession
    ):
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        return result

    async def get_all_categories(
            self,
            session: AsyncSession
    ):
        stmt = select(self.model)
        result = await session.execute(stmt)
        result = [dict(r._mapping)[f'{self.model}'] for r in result]
        return result

    async def create_category(
            self,
            session: AsyncSession,
            data: dict
    ):
        data = {
            'title': f'Category-{int(datetime.now().strftime("%Y%m%d%H%M%S"))}',
        }
        # data = {
        #     'title': 'Программирование'
        # }
        stmt = insert(self.model).values(**data)
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            print(e.detail)
        finally:
            await session.close()
        return data


category = CategoryCrud(Category)
