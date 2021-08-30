import os
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

engine = create_engine('sqlite+pysqlite:///app.db', echo=True, future=True)
Session = sessionmaker(engine)


def get_data_from_alphavantage(symbol: str,
                               interval: str,
                               outputsize: str = 'full'):
    """Retrieves data from alpha vantage for the provided ticker & interval"""

    load_dotenv()
    ts = TimeSeries(key=os.environ.get('AV_API_KEY'), output_size=outputsize)

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

    if interval == '1d':
        return DailyBar(timestamp=index,
                symbol_id=1,
                open_price=row['open'],
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                adj_close_price=row['adj_close_price'],
                volume=row['volume'],
                dividend_amount=row['dividend_amount'])

    elif interval == '1w':
        return WeeklyBar(timestamp=index, 
                symbol_id=1, 
                open_price=row['open'], 
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                adj_close_price=row['adj_close_price'],
                volume=row['volume'],
                dividend_amount=row['dividend_amount'])

    elif interval == '1m':
        return MonthlyBar(timestamp=index, 
                symbol_id=1, 
                open_price=row['open'], 
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                adj_close_price=row['adj_close_price'],
                volume=row['volume'],
                dividend_amount=row['dividend_amount'])


def update_database(symbol, interval):
    with Session() as session:
        for index, row in get_data_from_alphavantage('AAPL', interval).iterrows():
            session.merge(convert_bar_to_sql_object(index, row, interval))
        session.commit()