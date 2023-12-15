from datetime import date

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from digitalize_bot.db import metadata, Base


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(length=100))
    last_name: str = Column(String(length=100))
    email: str = Column(String(length=100), unique=True)
    registered_at: date = Column(DateTime, default=func.now())

    books = relationship('UsersBooks', back_populates='user')


