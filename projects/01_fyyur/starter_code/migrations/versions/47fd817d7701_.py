"""empty message

Revision ID: 47fd817d7701
Revises: f529ec78ddf2
Create Date: 2019-09-21 17:16:16.553567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47fd817d7701'
down_revision = 'f529ec78ddf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'teste')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('teste', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
