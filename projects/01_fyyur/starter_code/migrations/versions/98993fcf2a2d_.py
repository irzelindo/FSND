"""empty message

Revision ID: 98993fcf2a2d
Revises: b1e88e77fa82
Create Date: 2019-10-10 17:41:50.957827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98993fcf2a2d'
down_revision = 'b1e88e77fa82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue_address', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'venue_address', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venue_address', type_='foreignkey')
    op.drop_column('venue_address', 'venue_id')
    # ### end Alembic commands ###
