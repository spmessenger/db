# db

Database package with SQLAlchemy models and Alembic migrations.

## Alembic

Run all commands from this directory (`db/`):

```bash
poetry run alembic current
poetry run alembic upgrade head
poetry run alembic downgrade -1
```

Create a new migration:

```bash
poetry run alembic revision --autogenerate -m "describe change"
```

## Existing utility script

Schema sync script is still available:

```bash
poetry run sync_schema
```
