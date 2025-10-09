from typing import AsyncGenerator, Generator
from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from .settings import settings


extra_params = settings.sqlalchemy_engine_params

async_engine = create_async_engine(settings.sqlalchemy_database_url, **extra_params)
engine = create_engine(settings.sync_only_sqlalchemy_database_url, **extra_params)

AsyncSessionLocal = async_sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


@asynccontextmanager
async def aget_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
