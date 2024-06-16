"""Added Instutution relation

Revision ID: 305b35cc87ab
Revises: 435f73519706
Create Date: 2024-06-16 13:29:14.720271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '305b35cc87ab'
down_revision: Union[str, None] = '435f73519706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('turnover', sa.Column('institution_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(op.f('fk_turnover_institution_id_institution'), 'turnover', 'institution', ['institution_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_turnover_institution_id_institution'), 'turnover', type_='foreignkey')
    op.drop_column('turnover', 'institution_id')
    # ### end Alembic commands ###
