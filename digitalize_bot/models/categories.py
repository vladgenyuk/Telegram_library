from sqlalchemy import Column, Integer, String

from digitalize_bot.db import metadata, Base


class Category(Base):
    __tablename__ = 'category'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))
