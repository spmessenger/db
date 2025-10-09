from sqlalchemy import String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(16), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    refresh_tokens: Mapped[list[str]] = mapped_column(ARRAY(String(128)))


class Message(Base):
    __tablename__ = 'messages'
