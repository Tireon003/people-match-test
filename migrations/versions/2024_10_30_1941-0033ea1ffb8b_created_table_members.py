"""Created table members

Revision ID: 0033ea1ffb8b
Revises: 
Create Date: 2024-10-30 19:41:18.680310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0033ea1ffb8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', name='gender'), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('avatar', sa.Uuid(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('lat', sa.Float(precision=4), nullable=False),
    sa.Column('lon', sa.Float(precision=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_members_id'), 'members', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_members_id'), table_name='members')
    op.drop_table('members')
    # ### end Alembic commands ###