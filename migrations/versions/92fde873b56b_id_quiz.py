"""id_quiz

Revision ID: 92fde873b56b
Revises: c3f3f5c5b4a8
Create Date: 2025-06-14 09:49:39.313165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92fde873b56b'
down_revision: Union[str, None] = 'c3f3f5c5b4a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
