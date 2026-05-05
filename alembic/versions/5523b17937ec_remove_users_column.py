"""remove users column

Revision ID: 5523b17937ec
Revises: 31c2d62527a5
Create Date: 2026-05-04 17:19:58.572875

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5523b17937ec"
down_revision: Union[str, Sequence[str], None] = "31c2d62527a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users", "wallet_id")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
