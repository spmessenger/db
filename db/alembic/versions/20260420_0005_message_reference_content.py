"""add reference content for messages

Revision ID: 20260420_0005
Revises: 20260420_0004
Create Date: 2026-04-20 00:10:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260420_0005"
down_revision = "20260420_0004"
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
    if "reference_content" not in columns:
        op.add_column("messages", sa.Column("reference_content", sa.String(length=2048), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("messages"))
        if name
    }
    if "reference_content" in columns:
        op.drop_column("messages", "reference_content")
