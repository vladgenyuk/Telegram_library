from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from digitalize_bot.config import SQLITE_DB_FILE


metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_async_engine(f"sqlite+aiosqlite:///{SQLITE_DB_FILE}", poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


