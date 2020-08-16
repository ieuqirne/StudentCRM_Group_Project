"""Change FK

Revision ID: 8cef2462a243
Revises: 1f41d8140243
Create Date: 2019-02-28 11:08:26.025527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cef2462a243'
down_revision = '1f41d8140243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('staff', schema=None) as batch_op:
        #batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_student')
    #with op.batch_alter_table('students', schema=None) as batch_op:
    #    batch_op.add_column(sa.Column('id_staff', sa.INTEGER(), nullable=True))
    #    batch_op.create_foreign_key(None, 'staff', ['id_staff'], ['id_staff'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_student', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'students', ['id_student'], ['id_student'])

    # ### end Alembic commands ###