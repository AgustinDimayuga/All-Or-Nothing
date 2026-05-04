"""add users_creds

Revision ID: 85b8252762b0
Revises: e88d23f7b0e5
Create Date: 2026-05-04 09:44:35.301227

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "85b8252762b0"
down_revision: Union[str, Sequence[str], None] = "e88d23f7b0e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("username", sa.String, nullable=False, unique=True)
    )
    op.create_table(
        "user_creds",
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("password", sa.String, nullable=False),
    )

    op.create_foreign_key(
        "user_creds_user_id_fkey",
        "user_creds",
        "users",
        ["user_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "username")
    op.drop_constraint("users_creds_user_id_fkey", "user_creds", type_="foreignkey")
    op.drop_table("user_creds")
    pass
