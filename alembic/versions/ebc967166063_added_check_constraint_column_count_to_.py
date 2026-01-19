"""added check constraint column count to product

Revision ID: ebc967166063
Revises: 50b373ef9a05
Create Date: 2026-01-18 16:43:44.523693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebc967166063'
down_revision: Union[str, Sequence[str], None] = '50b373ef9a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "check_count_positive",  # name of the constraint
        "products",  # table name
        "count >= 0"  # SQL expression (can also be SQLAlchemy expression)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "check_count_positive",  # name
        "products",  # table name
        type_="check"  # specify the type of constraint
    )
