"""add user subscription tier

Revision ID: 20260423_0008
Revises: 20260420_0007
Create Date: 2026-04-23 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260423_0008"
down_revision = "20260420_0007"
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
    if "subscription_tier" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "subscription_tier",
                sa.String(length=16),
                nullable=False,
                server_default="free",
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
    if "subscription_tier" in columns:
        op.drop_column("users", "subscription_tier")
