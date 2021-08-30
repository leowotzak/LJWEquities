#!/usr/bin/env python
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite+pysqlite:///app.db', echo=True, future=True)
Base = declarative_base()


class Symbols(Base):

    __tablename__ = 'symbols'

    symbol_id = Column(Integer(), primary_key=True)
    name = Column(String())
    ticker = Column(String())
    description = Column(String())
    sector = Column(String())
    asset_type = Column(String())
    created_date = Column(DateTime())
    last_updated_date = Column(DateTime())

    def __repr__(self):
        return f'Symbol(symbol_id={self.symbol_id}, ticker={self.ticker}, name={self.name})'

class DailyBar(Base):

    __tablename__ = 'daily_bar_data'

    timestamp = Column(DateTime(), primary_key=True)
    symbol_id = Column(Integer(), ForeignKey('symbols.symbol_id'), primary_key=True)
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    close_price = Column(Float())
    adj_close_price = Column(Float())
    volume = Column(Float())
    dividend_amount = Column(Float())
    created_date = Column(DateTime())
    last_updated_date = Column(DateTime())

    def __repr__(self):
        return f"DailyBar(symbol_id={self.symbol_id}, timestamp={self.timestamp}, close_price={self.close_price})"


class WeeklyBar(Base):

    __tablename__ = 'weekly_bar_data'

    timestamp = Column(DateTime(), primary_key=True)
    symbol_id = Column(Integer(), primary_key=True)
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    close_price = Column(Float())
    adj_close_price = Column(Float())
    volume = Column(Float())
    dividend_amount = Column(Float())
    created_date = Column(DateTime())
    last_updated_date = Column(DateTime())


    def __repr__(self):
        return f"WeeklyBar(symbol_id={self.symbol_id}, timestamp={self.timestamp}, close_price={self.close_price})"


class MonthlyBar(Base):

    __tablename__ = 'monthly_bar_data'

    timestamp = Column(DateTime(), primary_key=True)
    symbol_id = Column(Integer(), primary_key=True)
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    close_price = Column(Float())
    adj_close_price = Column(Float())
    volume = Column(Float())
    dividend_amount = Column(Float())
    created_date = Column(DateTime())
    last_updated_date = Column(DateTime())


    def __repr__(self):
        return f"MonthlyBar(symbol_id={self.symbol_id}, timestamp={self.timestamp}, close_price={self.close_price})"