from enum import StrEnum
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
    DB_PORt: int = 5432

    @property
    def sqlalchemy_database_url(self):
        match self.DB_TYPE:
            case DatabaseTypeEnum.POSTGRESQL:
                return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORt}/{self.DB_NAME}'
            case DatabaseTypeEnum.IN_MEMORY:
                return 'sqlite:///:memory:'
            case _:
                raise ValueError(f'Unknown database type: {self.DB_TYPE}')
