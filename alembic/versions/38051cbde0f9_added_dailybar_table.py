"""added DailyBar table

Revision ID: 38051cbde0f9
Revises: 0b857bc76ed7
Create Date: 2021-08-30 15:01:06.312908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38051cbde0f9'
down_revision = '0b857bc76ed7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'daily_bar_data',
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('symbol_id', sa.Integer, sa.ForeignKey('symbols.symbol_id'), primary_key=True),
        sa.Column('open_price', sa.Float),
        sa.Column('high_price', sa.Float),
        sa.Column('low_price', sa.Float),
        sa.Column('close_price', sa.Float),
        sa.Column('adj_close_price', sa.Float),
        sa.Column('volume', sa.Float),
        sa.Column('dividend_amount', sa.Float),
        sa.Column('created_date', sa.DateTime, nullable=False),
        sa.Column('last_updated_date', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('daily_bar_data')
