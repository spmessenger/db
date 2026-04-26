from sqlalchemy import create_engine, inspect, text

from db.base import Base
from db import misc
from db.misc import tables


def test_get_missing_tables_returns_all_tables_for_empty_schema(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(tables, 'engine', engine)

    missing_tables = misc.get_missing_tables()

    assert missing_tables == sorted(Base.metadata.tables)


def test_ensure_tables_exist_raises_for_incomplete_schema(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(tables, 'engine', engine)

    try:
        misc.ensure_tables_exist()
    except RuntimeError as exc:
        assert 'Missing tables' in str(exc)
    else:
        raise AssertionError('ensure_tables_exist() should raise when tables are missing')


def test_ensure_tables_exist_passes_when_schema_is_ready(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(tables, 'engine', engine)
    Base.metadata.create_all(engine)

    misc.ensure_tables_exist()


def test_get_missing_columns_returns_missing_chat_avatar_url(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(tables, 'engine', engine)

    with engine.begin() as connection:
        connection.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR(16), hashed_password VARCHAR(128), refresh_tokens JSON)'))
        connection.execute(text('CREATE TABLE chats (id INTEGER PRIMARY KEY, type VARCHAR(16), title VARCHAR(64))'))
        connection.execute(text('CREATE TABLE messages (id INTEGER PRIMARY KEY, chat_id INTEGER, participant_id INTEGER, content VARCHAR(2048), created_at_timestamp NUMERIC(16, 4))'))
        connection.execute(text('CREATE TABLE participants (id INTEGER PRIMARY KEY, chat_id INTEGER, user_id INTEGER, role VARCHAR(16), draft VARCHAR(2048), pin_position INTEGER, chat_visible BOOLEAN)'))
        connection.execute(text('CREATE TABLE chat_last_messages (chat_id INTEGER NOT NULL UNIQUE, message_id INTEGER NOT NULL UNIQUE)'))

    missing_columns = misc.get_missing_columns()

    assert 'chats.avatar_url' in missing_columns
    assert 'participants.last_read_message_id' in missing_columns
    assert 'participants.unread_messages_count' in missing_columns


def test_sync_schema_creates_missing_columns(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    monkeypatch.setattr(tables, 'engine', engine)

    with engine.begin() as connection:
        connection.execute(text('CREATE TABLE chats (id INTEGER PRIMARY KEY, type VARCHAR(16), title VARCHAR(64))'))

    result = misc.sync_schema()
    inspector = inspect(engine)
    chat_columns = {column['name'] for column in inspector.get_columns('chats')}

    assert 'users' in result['tables']
    assert 'participants' in result['tables']
    assert 'messages' in result['tables']
    assert 'chat_last_messages' in result['tables']
    assert 'chats.avatar_url' in result['columns']
    assert 'avatar_url' in chat_columns
    misc.ensure_tables_exist()
