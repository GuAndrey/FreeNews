"""add index for news

Revision ID: 6c743c571061
Revises: 7672d7c954d4
Create Date: 2022-05-15 06:12:01.415564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c743c571061'
down_revision = '7672d7c954d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_news_title'), 'news', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_news_title'), table_name='news')
    # ### end Alembic commands ###