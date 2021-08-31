import logging
import sqlite3
from datetime import datetime
from queue import Queue
from typing import AnyStr, Callable, Generator, List

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ljwtrader.data import DailyBar, Symbols
from ljwtrader.events import MarketEvent

logger = logging.getLogger(__name__)

engine = create_engine('sqlite+pysqlite:///app.db', echo=True, future=True)
Session = sessionmaker(engine)

class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, symbols: List[AnyStr], queue_: Queue,
                 start_date: datetime, end_date: datetime, frequency: AnyStr,
                 vendor: AnyStr, process_events_func: Callable[[None], None]):
        self._symbols = symbols
        self._process_events_func = process_events_func
        self.data = ( tup for tup in pd.read_sql("SELECT * FROM symbols JOIN daily_bar_data ON symbols.symbol_id=daily_bar_data.symbol_id WHERE symbols.ticker IN ('%s')" % "', '".join(self._symbols),
                                          sqlite3.connect('app.db'),
                                          index_col='timestamp').sort_index().groupby(level=0) )
        self.latest_symbol_data = { sym: {} for sym in self._symbols }

    
    def _get_next_bar(self) -> None:
        try:
            index, row = next(self.data)
        except StopIteration:
            self._contine_backtest = False
        else:
            for bar in map(convert_bar, row.iterrows()):
                self._queue.put(MarketEvent(bar['ticker'], bar['timestamp']))
                self.latest_symbol_data[bar['ticker']][index]= bar

    def get_latest_symbol_data(self, ticker: str, category: str, num_days: int) -> np.ndarray:
        """Retrieves the bars for a given ticker's category over the # of specified days"""

        latest_data = self.latest_symbol_data[ticker].copy()
        try:
            arr = [ latest_data.popitem()[1][category] for _ in range(num_days) ]
        except KeyError as e:
            arr = []
        return np.array(arr)
    def start_backtest(self) -> None:
        self._contine_backtest = True
        while self._contine_backtest:
            self._get_next_bar()
            self._process_events_func()

