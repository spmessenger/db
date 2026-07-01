"""add message replies table

Revision ID: 20260630_0012
Revises: 31f01d047020
Create Date: 2026-06-30 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260630_0012"
down_revision = "31f01d047020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "replies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("replying_msg_id", sa.Integer(), nullable=False),
        sa.Column("reply_to_msg_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["replying_msg_id"], ["messages.id"]),
        sa.ForeignKeyConstraint(["reply_to_msg_id"], ["messages.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("replying_msg_id", name="uq_replies_replying_msg_id"),
    )
    op.create_index(op.f("ix_replies_id"), "replies", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_replies_id"), table_name="replies")
    op.drop_table("replies")
