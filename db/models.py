from .base import Base


class User(Base):
    __tablename__ = 'users'


class Message(Base):
    __tablename__ = 'messages'
