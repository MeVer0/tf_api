"""add tables2

Revision ID: ae81f3ba7173
Revises: 3bbda22832e1
Create Date: 2023-08-12 10:57:14.595772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae81f3ba7173'
down_revision: Union[str, None] = '3bbda22832e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(80), nullable=False),
    sa.Column('email', sa.String(100), nullable=False),
    sa.Column('hashed_password', sa.String(200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('work_experience', sa.Integer(), nullable=True),
    sa.Column('knowledge_field', sa.Integer(), nullable=True),
    sa.Column('github_link', sa.String(200), nullable=True),
    sa.Column('linkedin_link', sa.String(200), nullable=True),
    sa.Column('hh_link', sa.String(200), nullable=True),
    sa.Column('work_schedule', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(2000), nullable=False),
    sa.Column('application_field', sa.Integer(), nullable=True),
    sa.Column('is_commercial', sa.Boolean(), nullable=False),
    sa.Column('development_stage', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_program_lang',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('python', sa.Boolean(), nullable=True),
    sa.Column('java', sa.Boolean(), nullable=True),
    sa.Column('c', sa.Boolean(), nullable=True),
    sa.Column('c_sharp', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_program_lang')
    op.drop_table('project')
    op.drop_table('portfolio')
    op.drop_table('user')
    # ### end Alembic commands ###
