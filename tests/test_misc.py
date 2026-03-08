from sqlalchemy import create_engine

from db.base import Base
from db import misc


def test_get_missing_tables_returns_all_tables_for_empty_schema(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(misc, 'engine', engine)

    missing_tables = misc.get_missing_tables()

    assert missing_tables == sorted(Base.metadata.tables)


def test_ensure_tables_exist_raises_for_incomplete_schema(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(misc, 'engine', engine)

    try:
        misc.ensure_tables_exist()
    except RuntimeError as exc:
        assert 'Missing tables' in str(exc)
    else:
        raise AssertionError('ensure_tables_exist() should raise when tables are missing')


def test_ensure_tables_exist_passes_when_schema_is_ready(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(misc, 'engine', engine)
    Base.metadata.create_all(engine)

    misc.ensure_tables_exist()
