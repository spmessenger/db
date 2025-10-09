from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(16), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    refresh_tokens: Mapped[list[str]] = mapped_column(JSON, default=list)


class Chat(Base):
    __tablename__ = 'chats'

    type: Mapped[str] = mapped_column(String(16))
    title: Mapped[str | None] = mapped_column(String(64), nullable=True)

    participants: Mapped[list['Participant']] = relationship('Participant', back_populates='chat')


class Message(Base):
    __tablename__ = 'messages'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(String(256), nullable=False)


class Participant(Base):
    __tablename__ = 'participants'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    chat: Mapped['Chat'] = relationship('Chat', back_populates='participants', userlist=False, foreign_keys=[chat_id])
