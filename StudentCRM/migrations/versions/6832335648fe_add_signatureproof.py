"""add signatureProof

Revision ID: 6832335648fe
Revises: ce448b41dcfb
Create Date: 2019-04-01 15:33:46.824727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6832335648fe'
down_revision = 'ce448b41dcfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('signature_image_link', sa.String(length=100), nullable=True))
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('dataConfirm',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.drop_column('signature_image_link')

    # ### end Alembic commands ###
