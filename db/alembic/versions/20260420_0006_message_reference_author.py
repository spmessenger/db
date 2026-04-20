"""add reference author for message replies

Revision ID: 20260420_0006
Revises: 20260420_0005
Create Date: 2026-04-20 00:20:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260420_0006"
down_revision = "20260420_0005"
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
    if "reference_author" not in columns:
        op.add_column("messages", sa.Column("reference_author", sa.String(length=64), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("messages"))
        if name
    }
    if "reference_author" in columns:
        op.drop_column("messages", "reference_author")
