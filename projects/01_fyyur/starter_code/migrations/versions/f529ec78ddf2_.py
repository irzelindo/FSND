"""empty message

Revision ID: f529ec78ddf2
Revises: 110bc63bbefa
Create Date: 2019-09-21 17:14:33.302004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f529ec78ddf2'
down_revision = '110bc63bbefa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('teste', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'teste')
    # ### end Alembic commands ###
