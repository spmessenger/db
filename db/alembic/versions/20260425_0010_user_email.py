"""add user email column

Revision ID: 20260425_0010
Revises: 20260423_0009
Create Date: 2026-04-25 00:00:01.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260425_0010"
down_revision = "20260423_0009"
branch_labels = None
depends_on = None


def _inspected_name(entry) -> str | None:
    if isinstance(entry, dict):
        return entry.get("name")
    return getattr(entry, "name", None)


def _inspected_unique_name(entry) -> str | None:
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

    if "email" not in columns:
        op.add_column(
            "users",
            sa.Column("email", sa.String(length=254), nullable=True),
        )

    op.execute(
        sa.text(
            "UPDATE users "
            "SET email = LOWER(username || '@local') "
            "WHERE email IS NULL OR email = ''"
        )
    )
    op.alter_column("users", "email", nullable=False)

    unique_constraints = {
        name
        for name in (_inspected_unique_name(item) for item in inspector.get_unique_constraints("users"))
        if name
    }
    if "uq_users_email" not in unique_constraints:
        op.create_unique_constraint("uq_users_email", "users", ["email"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        name
        for name in (_inspected_name(column) for column in inspector.get_columns("users"))
        if name
    }
    if "email" in columns:
        unique_constraints = {
            name
            for name in (_inspected_unique_name(item) for item in inspector.get_unique_constraints("users"))
            if name
        }
        if "uq_users_email" in unique_constraints:
            op.drop_constraint("uq_users_email", "users", type_="unique")
        op.drop_column("users", "email")
