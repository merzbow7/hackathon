"""Add Institution data

Revision ID: 54c3460d1fd5
Revises: 4e536ca0124d
Create Date: 2024-06-16 19:27:44.145421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '54c3460d1fd5'
down_revision: Union[str, None] = '4e536ca0124d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO institution (name) VALUES
            ('Школа 21'),
            ('Гимназия 42')
        ON CONFLICT (name) DO NOTHING;
        """
    )


def downgrade() -> None:
    pass
