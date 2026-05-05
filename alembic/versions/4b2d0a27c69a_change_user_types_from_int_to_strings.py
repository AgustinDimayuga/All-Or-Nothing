"""change user types from int to strings

Revision ID: 4b2d0a27c69a
Revises: 5523b17937ec
Create Date: 2026-05-04 17:38:39.121416

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4b2d0a27c69a"
down_revision: Union[str, Sequence[str], None] = "5523b17937ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_column("users", "name")

    op.drop_column("users", "email")

    op.drop_column("users", "phone")

    op.add_column("users", sa.Column("name", sa.String(255), nullable=False))

    op.add_column("users", sa.Column("email", sa.String(255), nullable=False))

    op.add_column("users", sa.Column("phone", sa.String(20), nullable=False))


def downgrade() -> None:

    op.drop_column("users", "name")

    op.drop_column("users", "email")

    op.drop_column("users", "phone")

    op.add_column("users", sa.Column("name", sa.Integer(), nullable=False))

    op.add_column("users", sa.Column("email", sa.Integer(), nullable=False))

    op.add_column("users", sa.Column("phone", sa.Integer(), nullable=False))
