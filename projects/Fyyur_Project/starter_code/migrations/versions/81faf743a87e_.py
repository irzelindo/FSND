"""empty message

Revision ID: 81faf743a87e
Revises: eb03ad4dfbf7
Create Date: 2019-10-04 13:50:30.422281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81faf743a87e'
down_revision = 'eb03ad4dfbf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('ticket_price', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
