"""Add verify Table

Revision ID: d16cc621347d
Revises: 64a54d346268
Create Date: 2019-04-04 18:30:40.248930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd16cc621347d'
down_revision = '64a54d346268'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verify',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_student', sa.Integer(), nullable=True),
    sa.Column('verifyString', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['id_student'], ['students.id_student'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('verifyString')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verify')
    # ### end Alembic commands ###
