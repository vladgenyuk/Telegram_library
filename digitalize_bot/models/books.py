from typing import Literal

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from digitalize_bot.db import metadata, Base


class Book(Base):
    __tablename__ = 'book'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))
    position_number: int = Column(Integer)
    category_id: int = Column(Integer, ForeignKey('category.id'))
    status: Literal['in_library', 'borrowed'] = Column(String(length=20), default='in_library')

    users = relationship('UsersBooks', back_populates='book')
