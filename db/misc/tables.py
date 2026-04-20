from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn
from ..base import Base
from ..session import engine


def _inspected_name(entry) -> str | None:
    if isinstance(entry, dict):
        return entry.get("name")
    return getattr(entry, "name", None)


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


def get_missing_columns() -> list[str]:
    inspector = inspect(engine)
    missing_columns: list[str] = []
    existing_tables = set(inspector.get_table_names())

    for table_name, table in Base.metadata.tables.items():
        if table_name not in existing_tables:
            continue

        existing_columns = {
            name
            for name in (_inspected_name(column) for column in inspector.get_columns(table_name))
            if name
        }
        expected_columns = {column.name for column in table.columns}
        missing_columns.extend(
            f'{table_name}.{column_name}'
            for column_name in sorted(expected_columns - existing_columns)
        )

    return missing_columns


def create_missing_columns() -> list[str]:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    created_columns: list[str] = []
    preparer = engine.dialect.identifier_preparer

    with engine.begin() as connection:
        for table_name, table in Base.metadata.tables.items():
            if table_name not in existing_tables:
                continue

            existing_columns = {
                name
                for name in (_inspected_name(column) for column in inspector.get_columns(table_name))
                if name
            }
            for column_name in sorted(column.name for column in table.columns if column.name not in existing_columns):
                column = table.columns[column_name]
                compiled_column = str(CreateColumn(
                    column).compile(dialect=engine.dialect))
                quoted_table_name = preparer.quote(table_name)
                connection.execute(
                    text(f'ALTER TABLE {quoted_table_name} ADD COLUMN {compiled_column}'))
                created_columns.append(f'{table_name}.{column_name}')

    return created_columns


def sync_schema() -> dict[str, list[str]]:
    created_tables_before = set(inspect(engine).get_table_names())
    create_tables()
    created_tables_after = set(inspect(engine).get_table_names())
    created_tables = sorted(created_tables_after - created_tables_before)
    created_columns = create_missing_columns()
    return {
        'tables': created_tables,
        'columns': created_columns,
    }


def ensure_tables_exist():
    missing_tables = get_missing_tables()
    if missing_tables:
        missing = ', '.join(missing_tables)
        raise RuntimeError(
            f'Database schema is incomplete. Missing tables: {missing}')

    missing_columns = get_missing_columns()
    if missing_columns:
        missing = ', '.join(missing_columns)
        raise RuntimeError(
            f'Database schema is incomplete. Missing columns: {missing}')
