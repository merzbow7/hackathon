"""Added User and Institution

Revision ID: 7fab97dca9b1
Revises: 
Create Date: 2024-06-15 18:20:07.593362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fab97dca9b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('institution',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_institution')),
    sa.UniqueConstraint('name', name=op.f('uq_institution_name'))
    )
    op.create_table('telegram_user',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('keycloak_id', sa.UUID(), nullable=True),
    sa.Column('verification_code', sa.UUID(), nullable=True),
    sa.Column('institution_id', sa.BigInteger(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['institution_id'], ['institution.id'], name=op.f('fk_telegram_user_institution_id_institution'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_telegram_user')),
    sa.UniqueConstraint('keycloak_id', name=op.f('uq_telegram_user_keycloak_id')),
    sa.UniqueConstraint('telegram_id', name=op.f('uq_telegram_user_telegram_id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram_user')
    op.drop_table('institution')
    # ### end Alembic commands ###
