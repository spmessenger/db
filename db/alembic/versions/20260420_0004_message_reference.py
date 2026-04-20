"""add message reference field

Revision ID: 20260420_0004
Revises: 20260413_0003
Create Date: 2026-04-20 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260420_0004"
down_revision = "20260413_0003"
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
    if "reference_message_id" not in columns:
        op.add_column(
            "messages",
            sa.Column("reference_message_id", sa.Integer(), nullable=True),
        )
    indexes = {
        name
        for name in (_inspected_name(index) for index in inspector.get_indexes("messages"))
        if name
    }
    if "ix_messages_reference_message_id" not in indexes:
        op.create_index(
            "ix_messages_reference_message_id",
            "messages",
            ["reference_message_id"],
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
    if "ix_messages_reference_message_id" in indexes:
        op.drop_index("ix_messages_reference_message_id", table_name="messages")

    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("messages"))
        if name
    }
    if "reference_message_id" in columns:
        op.drop_column("messages", "reference_message_id")
