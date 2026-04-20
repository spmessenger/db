"""add message forward metadata

Revision ID: 20260420_0007
Revises: 20260420_0006
Create Date: 2026-04-20 00:40:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260420_0007"
down_revision = "20260420_0006"
branch_labels = None
depends_on = None


def _inspected_name(entry) -> str | None:
    if isinstance(entry, dict):
        return entry.get("name")
    return getattr(entry, "name", None)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("messages"))
        if name
    }

    if "forwarded_from_message_id" not in columns:
        op.add_column("messages", sa.Column("forwarded_from_message_id", sa.Integer(), nullable=True))
    if "forwarded_from_author" not in columns:
        op.add_column("messages", sa.Column("forwarded_from_author", sa.String(length=64), nullable=True))
    if "forwarded_from_author_avatar_url" not in columns:
        op.add_column("messages", sa.Column("forwarded_from_author_avatar_url", sa.Text(), nullable=True))
    if "forwarded_from_content" not in columns:
        op.add_column("messages", sa.Column("forwarded_from_content", sa.String(length=2048), nullable=True))

    indexes = {
        name
        for name in (_inspected_name(index) for index in inspector.get_indexes("messages"))
        if name
    }
    if "ix_messages_forwarded_from_message_id" not in indexes:
        op.create_index(
            "ix_messages_forwarded_from_message_id",
            "messages",
            ["forwarded_from_message_id"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    indexes = {
        name
        for name in (_inspected_name(index) for index in inspector.get_indexes("messages"))
        if name
    }
    if "ix_messages_forwarded_from_message_id" in indexes:
        op.drop_index("ix_messages_forwarded_from_message_id", table_name="messages")

    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("messages"))
        if name
    }
    if "forwarded_from_content" in columns:
        op.drop_column("messages", "forwarded_from_content")
    if "forwarded_from_author_avatar_url" in columns:
        op.drop_column("messages", "forwarded_from_author_avatar_url")
    if "forwarded_from_author" in columns:
        op.drop_column("messages", "forwarded_from_author")
    if "forwarded_from_message_id" in columns:
        op.drop_column("messages", "forwarded_from_message_id")
