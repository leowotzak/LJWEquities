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

    # op.create_table(
    #     'daily_bar_data',
    #     sa.Column('timestamp', sa.DateTime, primary_key=True),
    #     sa.Column('symbol_id', sa.Integer, sa.ForeignKey('symbols.symbol_id'), primary_key=True),
    #     sa.Column('open', sa.Float),
    #     sa.Column('high', sa.Float),
    #     sa.Column('low', sa.Float),
    #     sa.Column('close', sa.Float),
    #     sa.Column('adj_close', sa.Float),
    #     sa.Column('volume', sa.Float),
    #     sa.Column('dividend_amount', sa.Float),
    #     sa.Column('created_date', sa.DateTime, nullable=False),
    #     sa.Column('last_updated_date', sa.DateTime, nullable=False)
    # )


def downgrade():
    op.drop_table('symbols')
