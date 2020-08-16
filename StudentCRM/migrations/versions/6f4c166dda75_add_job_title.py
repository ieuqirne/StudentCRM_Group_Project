"""Add job Title

Revision ID: 6f4c166dda75
Revises: 9a98411827a7
Create Date: 2019-03-12 13:50:23.659790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f4c166dda75'
down_revision = '9a98411827a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employmentStartDate', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('jobTitle', sa.String(length=50), nullable=True))
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('filledIn',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('filledIn',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.drop_column('jobTitle')
        batch_op.drop_column('employmentStartDate')

    # ### end Alembic commands ###