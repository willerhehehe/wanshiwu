"""empty message

Revision ID: 4b6e5798ca3e
Revises: 57b081d08f30
Create Date: 2018-05-09 17:26:46.524201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b6e5798ca3e'
down_revision = '57b081d08f30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'time')
    # ### end Alembic commands ###
