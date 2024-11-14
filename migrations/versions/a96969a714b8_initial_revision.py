"""Initial revision.

Revision ID: a96969a714b8
Revises: 6c0b0cd874c3
Create Date: 2024-11-14 12:48:26.560064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a96969a714b8'
down_revision = '6c0b0cd874c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_food', sa.String(length=30), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('weight_gr', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('ingredients', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=30), nullable=True),
    sa.Column('time_create', sa.DateTime(), nullable=True),
    sa.Column('time_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('menu')
    # ### end Alembic commands ###
