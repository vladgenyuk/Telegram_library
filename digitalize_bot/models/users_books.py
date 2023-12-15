from datetime import date

from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from digitalize_bot.db import metadata, Base


class UsersBooks(Base):
    __tablename__ = 'users_books'
    id: int = Column(Integer, primary_key=True)

    book_id: int = Column(Integer, ForeignKey('book.id'), default=1)
    user_id: int = Column(Integer, ForeignKey('user.id'), default=1)

    issued_at: date = Column(DateTime, default=func.now())
    returned_at: date = Column(DateTime, default=None)

    book = relationship("Book", back_populates="users")
    user = relationship("User", back_populates="books")
