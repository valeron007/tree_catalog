"""added column products

Revision ID: 50b373ef9a05
Revises: 7fd9abe8e9c5
Create Date: 2026-01-18 02:55:48.940945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50b373ef9a05'
down_revision: Union[str, Sequence[str], None] = '7fd9abe8e9c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('count', sa.BigInteger(), nullable=True, default=0))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'count')
