"""add rate table

Revision ID: 1fdf538ffc93
Revises: 2f6c56f0af54
Create Date: 2014-07-16 21:54:56.619193

"""

# revision identifiers, used by Alembic.
revision = '1fdf538ffc93'
down_revision = '2f6c56f0af54'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rate',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('drive_request_id', sa.String(), nullable=False),
    sa.Column('rater_user_id', sa.String(), nullable=False),
    sa.Column('rated_user_id', sa.String(), nullable=False),
    sa.Column('rater_is_driver', sa.Boolean(), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['drive_request_id'], ['drive_request.id'], ),
    sa.ForeignKeyConstraint(['rated_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['rater_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rate')
    ### end Alembic commands ###
