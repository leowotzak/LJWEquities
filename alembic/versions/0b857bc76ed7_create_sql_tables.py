"""create sql tables

Revision ID: 0b857bc76ed7
Revises: 
Create Date: 2021-08-30 12:53:38.289375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b857bc76ed7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'symbols',
        sa.Column('symbol_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('ticker', sa.String),
        sa.Column('description', sa.String),
        sa.Column('sector', sa.String),
        sa.Column('asset_type', sa.String),
        sa.Column('created_date', sa.DateTime),
        sa.Column('last_updated_date', sa.DateTime)
    )


def downgrade():
    op.drop_table('symbols')
