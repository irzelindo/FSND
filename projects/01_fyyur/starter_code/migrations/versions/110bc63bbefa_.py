"""empty message

Revision ID: 110bc63bbefa
Revises: f70861485255
Create Date: 2019-09-20 20:04:46.238860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110bc63bbefa'
down_revision = 'f70861485255'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('instagram_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'instagram_link')
    # ### end Alembic commands ###
