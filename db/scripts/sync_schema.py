import argparse

from db.misc import sync_schema


def main():
    parser = argparse.ArgumentParser(
        description='Create missing tables and columns from SQLAlchemy metadata.',
    )
    parser.parse_args()

    result = sync_schema()
    created_tables = result['tables']
    created_columns = result['columns']

    if not created_tables and not created_columns:
        print('Schema is already up to date.')
        return

    if created_tables:
        print('Created tables:')
        for table_name in created_tables:
            print(f' - {table_name}')

    if created_columns:
        print('Created columns:')
        for column_name in created_columns:
            print(f' - {column_name}')
