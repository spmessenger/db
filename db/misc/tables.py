from sqlalchemy import inspect
from ..base import Base
from ..session import engine


def create_tables() -> list[str]:
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    return inspector.get_table_names()


def drop_tables():
    Base.metadata.drop_all(engine)


def get_missing_tables() -> list[str]:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    expected_tables = set(Base.metadata.tables)
    return sorted(expected_tables - existing_tables)


def ensure_tables_exist():
    missing_tables = get_missing_tables()
    if missing_tables:
        missing = ', '.join(missing_tables)
        raise RuntimeError(
            f'Database schema is incomplete. Missing tables: {missing}')
