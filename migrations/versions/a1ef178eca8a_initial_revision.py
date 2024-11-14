"""Initial revision.

Revision ID: a1ef178eca8a
Revises: a96969a714b8
Create Date: 2024-11-14 21:01:40.960068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1ef178eca8a'
down_revision = 'a96969a714b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('summa', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('time_create', sa.DateTime(), nullable=True),
    sa.Column('time_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('orderins', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_orderins_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_orderins_menu_id'), ['menu_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_orderins_order_id'), ['order_id'], unique=False)

    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('summa', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('delivery', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('pay_stat', sa.String(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('time_create', sa.DateTime(), nullable=True),
    sa.Column('time_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_orders_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_orders_id'))

    op.drop_table('orders')
    with op.batch_alter_table('orderins', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_orderins_order_id'))
        batch_op.drop_index(batch_op.f('ix_orderins_menu_id'))
        batch_op.drop_index(batch_op.f('ix_orderins_id'))

    op.drop_table('orderins')
    # ### end Alembic commands ###