"""add_dic_tables\

Revision ID: d7577a2fdd7d
Revises: aa8fd50c6259
Create Date: 2023-08-13 14:41:15.553364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7577a2fdd7d'
down_revision: Union[str, None] = 'aa8fd50c6259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dic_knowledge_field',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dic_work_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('portfolio_knowledge_field',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('portfolio_id', sa.Integer(), nullable=False),
    sa.Column('knowledge_field_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['knowledge_field_id'], ['dic_knowledge_field.id'], ),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portfolio_knowledge_field')
    op.drop_table('dic_work_schedule')
    op.drop_table('dic_knowledge_field')
    # ### end Alembic commands ###
