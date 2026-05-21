"""change parented id to nullable

Revision ID: 3b1b233e16c0
Revises: 20a4a4724e51
Create Date: 2026-05-09 19:34:40.318698

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3b1b233e16c0"
down_revision: Union[str, Sequence[str], None] = "1e23635aa2fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("fk_parent_id", "comments")
    op.drop_column("comments", "parent_id")
    op.add_column("comments", sa.Column("parent_id", sa.Integer, nullable=True))
    op.add_column("comments", sa.Column("game_id", sa.Integer, nullable=False))
    # 6. Foreign Key from "comments" to "comments" to create replies
    op.create_foreign_key(
        "fk_parent_id",
        "comments",
        "comments",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_comment_game_id",
        "comments",
        "games",
        ["game_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_parent_id", "comments", type_="foreignkey")
    op.drop_constraint("fk_comment_game_id", "comments", type_="foreignkey")
    op.drop_column("comments", "parent_id")
    op.add_column("comments", sa.Column("parent_id", sa.Integer, nullable=True))
    op.create_foreign_key(
        "fk_parent_id",
        "comments",
        "comments",
        ["parent_id"],
        ["id"],
    )
