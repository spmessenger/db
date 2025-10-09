from typing import AsyncGenerator, Generator
from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from .settings import settings


extra_params = settings.sqlalchemy_engine_params

aengine = create_async_engine(settings.sqlalchemy_database_url, **extra_params)
engine = create_engine(settings.sync_only_sqlalchemy_database_url, **extra_params)

AsyncSessionLocal = async_sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=aengine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


@asynccontextmanager
async def aget_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def asession_factory(func):
    async def wrapper(*args, **kwargs):
        if kwargs.get('session') is None:
            async with aget_session() as session:
                kwargs['session'] = session
                return await func(*args, **kwargs)
        else:
            return await func(*args, **kwargs)
    return wrapper


def session_factory(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('session') is None:
            with aget_session() as session:
                kwargs['session'] = session
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper


def ping_connection():
    try:
        with engine.connect() as con:
            con.execute(text('SELECT 1'))
            return True
    except Exception:
        return False


async def aping_connection():
    try:
        async with aengine.connect() as con:
            await con.execute(text('SELECT 1'))
            return True
    except Exception:
        return False
