"""add chat groups tables

Revision ID: 20260411_0002
Revises: d8c9bebdee09
Create Date: 2026-04-11 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260411_0002"
down_revision = "d8c9bebdee09"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_groups",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chat_groups_id"), "chat_groups", ["id"], unique=False)

    op.create_table(
        "chat_group_chats",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["chats.id"]),
        sa.ForeignKeyConstraint(["group_id"], ["chat_groups.id"]),
    )


def downgrade() -> None:
    op.drop_table("chat_group_chats")
    op.drop_index(op.f("ix_chat_groups_id"), table_name="chat_groups")
    op.drop_table("chat_groups")
