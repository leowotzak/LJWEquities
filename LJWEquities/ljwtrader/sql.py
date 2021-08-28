#!/usr/bin/env python
from dotenv import load_dotenv

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)
Base = declarative_base()
Session = sessionmaker(engine)


class Bar(Base):

    __tablename__ = 'bar_data'

    timestamp = Column(DateTime, primary_key=True)
    symbol_id = Column(Integer, primary_key=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)

    def __repr__(self):
        return f"Bar({self.timestamp}) {self.symbol_id} {self.close_price})"


Base.metadata.create_all(engine)


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


def convert_bar_to_sql_object(index, row):
    return Bar(timestamp=index,
               symbol_id=1,
               open_price=row['open'],
               high_price=row['high'],
               low_price=row['low'],
               close_price=row['close'],
               volume=row['volume'])


if __name__ == '__main__':

    load_dotenv()

    with Session() as session:
        for index, row in get_data_from_alphavantage('AAPL').iterrows():
            session.merge(convert_bar_to_sql_object(index, row))
        session.commit()
