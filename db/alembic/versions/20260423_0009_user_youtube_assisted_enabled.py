"""add user youtube assisted enabled flag

Revision ID: 20260423_0009
Revises: 20260423_0008
Create Date: 2026-04-23 00:00:01.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260423_0009"
down_revision = "20260423_0008"
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
        for name in (_inspected_name(column) for column in inspector.get_columns("users"))
        if name
    }
    if "youtube_assisted_enabled" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "youtube_assisted_enabled",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("users"))
        if name
    }
    if "youtube_assisted_enabled" in columns:
        op.drop_column("users", "youtube_assisted_enabled")
