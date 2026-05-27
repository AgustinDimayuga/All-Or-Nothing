"""create balance table

Revision ID: 46391ff7c5e8
Revises: 173dfeb3e0b5
Create Date: 2026-05-26 12:30:23.584762

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "46391ff7c5e8"
down_revision: Union[str, Sequence[str], None] = "383d64614811"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_balances",
        sa.Column("user_id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("balance", sa.Numeric(precision=15, scale=2), nullable=False),
    )
    op.create_foreign_key(
        "user_bal_user_id_fk",
        "user_balances",
        "users",
        ["user_id"],
        ["id"],
    )
    op.alter_column("wallet", "change", type_=sa.Numeric(precision=15, scale=2))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("user_balances", " user_bal_user_id_fk")
    op.drop_table("user_balances")
    op.alter_column("wallet", "change", type_=sa.Integer)
    pass
