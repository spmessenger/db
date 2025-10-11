from sqlalchemy import inspect
from ..base import Base
from ..session import engine


def create_tables() -> list[str]:
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    return inspector.get_table_names()


def drop_tables():
    Base.metadata.drop_all(engine)
