from sqlalchemy import Boolean, Column, Integer, Numeric, String, JSON, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .misc.defaults import default_timestamp


MESSAGE_LEN = 2048


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(16), unique=True)
    email: Mapped[str | None] = mapped_column(String(254), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    refresh_tokens: Mapped[list[str]] = mapped_column(JSON, default=list)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String(16), nullable=False, default='free')
    youtube_assisted_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


chat_last_message_association_table = Table(
    'chat_last_messages',
    Base.metadata,
    Column('chat_id', ForeignKey('chats.id'), nullable=False, unique=True),
    Column('message_id', ForeignKey('messages.id'), nullable=False, unique=True),
)

chat_group_chat_association_table = Table(
    'chat_group_chats',
    Base.metadata,
    Column('group_id', ForeignKey('chat_groups.id'), nullable=False),
    Column('chat_id', ForeignKey('chats.id'), nullable=False),
)


class Chat(Base):
    __tablename__ = 'chats'

    type: Mapped[str] = mapped_column(String(16))
    title: Mapped[str | None] = mapped_column(String(64), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_message: Mapped['Message'] = relationship(
        'Message',
        secondary=chat_last_message_association_table,
        uselist=False,
        viewonly=True,
    )

    participants: Mapped[list['Participant']] = relationship('Participant', back_populates='chat')
    messages: Mapped[list['Message']] = relationship(
        'Message', back_populates='chat', foreign_keys='Message.chat_id'
    )


class Message(Base):
    __tablename__ = 'messages'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'))
    reference_message_id: Mapped[int | None] = mapped_column(ForeignKey('messages.id'), nullable=True)
    reference_author: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reference_content: Mapped[str | None] = mapped_column(String(MESSAGE_LEN), nullable=True)
    forwarded_from_message_id: Mapped[int | None] = mapped_column(ForeignKey('messages.id'), nullable=True)
    forwarded_from_author: Mapped[str | None] = mapped_column(String(64), nullable=True)
    forwarded_from_author_avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    forwarded_from_content: Mapped[str | None] = mapped_column(String(MESSAGE_LEN), nullable=True)
    content: Mapped[str] = mapped_column(String(MESSAGE_LEN), nullable=False)
    created_at_timestamp: Mapped[float | None] = mapped_column(Numeric(16, 4), nullable=False, default=default_timestamp)
    chat: Mapped['Chat'] = relationship('Chat', back_populates='messages', foreign_keys=[chat_id], uselist=False)


class Participant(Base):
    __tablename__ = 'participants'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    draft: Mapped[str | None] = mapped_column(String(MESSAGE_LEN), nullable=True)
    pin_position: Mapped[int] = mapped_column(Integer, default=0)
    chat_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    last_read_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unread_messages_count: Mapped[int] = mapped_column(Integer, default=0)

    chat: Mapped['Chat'] = relationship('Chat', back_populates='participants', uselist=False, foreign_keys=[chat_id])
    user: Mapped['User'] = relationship('User', uselist=False, foreign_keys=[user_id])


class ChatGroup(Base):
    __tablename__ = 'chat_groups'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(64), nullable=False)

    chats: Mapped[list['Chat']] = relationship(
        'Chat',
        secondary=chat_group_chat_association_table,
        uselist=True,
    )
