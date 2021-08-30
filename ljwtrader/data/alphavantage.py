import os
from datetime import datetime

from .models import (Symbols, DailyBar, WeeklyBar, MonthlyBar)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

engine = create_engine('sqlite+pysqlite:///app.db', echo=True, future=True)
Session = sessionmaker(engine)

MODEL_MAP = {'1d': DailyBar, '1w': WeeklyBar, '1m': MonthlyBar}


def get_data_from_alphavantage(symbol: str,
                               interval: str,
                               outputsize: str = 'full'):
    """Retrieves data from alpha vantage for the provided ticker & interval"""

    load_dotenv()
    ts = TimeSeries(key=os.environ.get('AV_API_KEY'), output_format='pandas')

    if interval == '1d':
        data, metadata = ts.get_daily_adjusted(symbol=symbol, output_size=outputsize)
    elif interval == '1w':
        data, metadata = ts.get_weekly_adjusted(symbol=symbol)
    elif interval == '1m':
        data, metadata = ts.get_monthly_adjusted(symbol=symbol)
    else:
        raise NotImplementedError('Frequency not implemented yet')

    return data.rename(
        columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. adjusted close': 'adj_close_price',
            '6. volume': 'volume',
            '7. dividend amount': 'dividend_amount'
        })

def convert_bar_to_sql_object(index, row, interval):

def convert_bar_to_sql_object(index, row, interval, symbol_id):

    try:
        model = MODEL_MAP[interval]
    except KeyError as e:
        raise e
    else:
        return model(timestamp=index,
                     symbol_id=symbol_id,
                     open_price=row['open'],
                open_price=row['open'], 
                     open_price=row['open'],
                open_price=row['open'], 
                     open_price=row['open'],
                     high_price=row['high'],
                     low_price=row['low'],
                     close_price=row['close'],
                     adj_close_price=row['adj_close_price'],
                     volume=row['volume'],
                     dividend_amount=row['dividend_amount'],
                     created_date=datetime.utcnow(),
                     last_updated_date=datetime.utcnow())


def update_database(symbol, interval):
    with Session() as session:
        for index, row in get_data_from_alphavantage('AAPL', interval).iterrows():
            session.merge(convert_bar_to_sql_object(index, row, interval))
        session.commit()