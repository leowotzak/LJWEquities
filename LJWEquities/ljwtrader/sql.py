#!/usr/bin/env python
from dotenv import load_dotenv

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)
Base = declarative_base()
Session = sessionmaker(engine)

def get_data_from_alphavantage(symbol: str,
                               interval: str = '1min',
                               outputsize: str = 'pandas'):
    """Retrieves data from alpha vantage for the provided ticker & interval"""

    import os
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=os.environ.get('AV_API_KEY'), output_format='pandas')
    data, metadata = ts.get_intraday(symbol='AAPL',
                                     interval='1min',
                                     outputsize='full')

    return data.rename(
        columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })
if __name__ == '__main__':

    load_dotenv()

