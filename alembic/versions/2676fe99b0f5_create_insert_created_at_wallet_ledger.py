"""create insert created_at wallet ledger

Revision ID: 2676fe99b0f5
Revises: 173dfeb3e0b5
Create Date: 2026-05-26 21:43:45.772649

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2676fe99b0f5"
down_revision: Union[str, Sequence[str], None] = "173dfeb3e0b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "wallet",
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("wallet", "created_at")
    pass
