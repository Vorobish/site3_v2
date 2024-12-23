"""Initial migration.

Revision ID: 6c0b0cd874c3
Revises: 
Create Date: 2024-11-14 12:29:55.891886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c0b0cd874c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name_food', sa.VARCHAR(length=30), nullable=False),
    sa.Column('category', sa.INTEGER(), nullable=False),
    sa.Column('weight_gr', sa.INTEGER(), nullable=True),
    sa.Column('price', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('ingredients', sa.TEXT(), nullable=True),
    sa.Column('image', sa.VARCHAR(length=30), nullable=True),
    sa.Column('time_create', sa.DATETIME(), nullable=True),
    sa.Column('time_update', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
