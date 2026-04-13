"""init

Revision ID: d8c9bebdee09
Revises: 20260410_0001
Create Date: 2026-04-10 23:15:16.920143
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8c9bebdee09'
down_revision = '20260410_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("participants")}
    if "last_read_message_id" not in columns:
        op.add_column("participants", sa.Column("last_read_message_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("participants")}
    if "last_read_message_id" in columns:
        op.drop_column("participants", "last_read_message_id")
