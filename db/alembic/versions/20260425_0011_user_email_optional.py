"""make user email nullable

Revision ID: 20260425_0011
Revises: 20260425_0010
Create Date: 2026-04-25 00:00:02.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260425_0011"
down_revision = "20260425_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", "email", existing_type=sa.String(length=254), nullable=True)


def downgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE users "
            "SET email = LOWER(username || '@local') "
            "WHERE email IS NULL OR email = ''"
        )
    )
    op.alter_column("users", "email", existing_type=sa.String(length=254), nullable=False)
