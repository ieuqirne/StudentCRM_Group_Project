"""add degree equality

Revision ID: ce448b41dcfb
Revises: 6f4c166dda75
Create Date: 2019-03-18 11:10:50.373718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce448b41dcfb'
down_revision = '6f4c166dda75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #with op.batch_alter_table('equality_monitoring', schema=None) as batch_op:
    #    batch_op.add_column(sa.Column('degree_id', sa.Integer(), nullable=True))

    #with op.batch_alter_table('staff', schema=None) as batch_op:
     #   batch_op.create_unique_constraint(None, ['staff_email'])
     #   batch_op.create_unique_constraint(None, ['token'])

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('equality_monitoring', schema=None) as batch_op:
        batch_op.drop_column('degree_id')

    # ### end Alembic commands ###
