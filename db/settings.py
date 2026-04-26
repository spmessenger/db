from enum import StrEnum
from functools import lru_cache
from pydantic_settings import BaseSettings


class DatabaseTypeEnum(StrEnum):
    POSTGRESQL = 'postgresql'
    IN_MEMORY = 'in_memory'


class Settings(BaseSettings):
    DB_TYPE: DatabaseTypeEnum = DatabaseTypeEnum.POSTGRESQL

    DB_NAME: str = 'messenger'
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432

    @property
    def sqlalchemy_database_url(self):
        match self.DB_TYPE:
            case DatabaseTypeEnum.POSTGRESQL:
                return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
            case DatabaseTypeEnum.IN_MEMORY:
                return 'sqlite+aiosqlite:///:memory:'
            case _:
                raise ValueError(f'Unknown database type: {self.DB_TYPE}')

    @property
    def sync_only_sqlalchemy_database_url(self):
        url = self.sqlalchemy_database_url
        return url.replace('+aiosqlite', '').replace('+asyncpg', '')

    @property
    def sqlalchemy_engine_params(self):
        match self.DB_TYPE:
            case DatabaseTypeEnum.POSTGRESQL:
                return {}
            case DatabaseTypeEnum.IN_MEMORY:
                return {
                    'connect_args': {
                        'check_same_thread': False
                    }
                }
            case _:
                return {}


@lru_cache()
def get_settings():
    return Settings()
