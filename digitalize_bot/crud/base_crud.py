from sqlalchemy import select, insert, func, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseCrud:
    def __init__(self, model):
        self.model = model

    async def get_all(
            self,
            session: AsyncSession,
    ):
        stmt = select(self.model)
        result = await session.execute(stmt)
        result = [dict(r._mapping) for r in result]
        await session.close()
        return result

    async def get_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.close()
        return result.scalar_one_or_none()

    async def get_count(
            self,
            session: AsyncSession
    ):
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        await session.close()
        return result

    async def create(
            self,
            session: AsyncSession,
            data: dict
    ):
        stmt = insert(self.model).values(**data)
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            print(e.detail)
        finally:
            await session.close()

    async def update(
            self,
            session: AsyncSession,
            id: int,
            new_data: dict
    ):
        stmt = update(self.model).values(**new_data).where(self.model.id == id)

        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print(e)
        finally:
            await session.close()

    async def delete(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)

        response = await session.execute(stmt)
        obj = response.scalar_one()
        if obj:
            await session.delete(obj)
            await session.commit()
        await session.close()
        return obj
