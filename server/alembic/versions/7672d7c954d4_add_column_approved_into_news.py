"""add column approved into news

Revision ID: 7672d7c954d4
Revises: 1af365fab8b7
Create Date: 2022-05-15 02:46:47.285462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7672d7c954d4'
down_revision = '1af365fab8b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('approved', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'approved')
    # ### end Alembic commands ###
