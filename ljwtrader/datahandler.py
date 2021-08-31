import logging
import sqlite3
from datetime import datetime
from queue import Queue
from typing import AnyStr, Callable, Generator, List

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ljwtrader.data import DailyBar, Symbols
from ljwtrader.events import MarketEvent

logger = logging.getLogger(__name__)

engine = create_engine('sqlite+pysqlite:///app.db', echo=True, future=True)
Session = sessionmaker(engine)

def convert_bar(row):
    index, data = row
    output_dict = dict( (k, v) for k, v in data.to_dict().items() if k in ['ticker', 'adj_close_price'] )
    output_dict['timestamp'] = index
    return output_dict

class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, symbols: List[AnyStr], queue_: Queue,
                 start_date: datetime, end_date: datetime, frequency: AnyStr,
                 vendor: AnyStr, process_events_func: Callable[[None], None]):
        self._symbols = symbols
        self._queue = queue_
        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency
        self._vendor = vendor
        self._contine_backtest = False
        self._process_events_func = process_events_func
        self.latest_symbol_data = {sym: {} for sym in self._symbols}
                                          index_col='timestamp').sort_index().groupby(level=0) )
        self.latest_symbol_data = { sym: {} for sym in self._symbols }

    
    def _get_next_bar(self) -> None:
        """Retrieves next bar from datahandler and places it on queue"""

        try:
            index, row = next(self.data)
        except StopIteration:
            self._contine_backtest = False
        else:
            for bar in map(convert_bar, row.iterrows()):
                self._queue.put(MarketEvent(bar['ticker'], bar['timestamp']))
                self.latest_symbol_data[bar['ticker']][index] = bar

    def _get_latest_symbol_data(self, ticker: str, category: str,
                                num_days: int) -> np.ndarray:
        """Retrieves the bars for a given ticker's category over the # of specified days"""

        latest_data = self.latest_symbol_data[ticker].copy()
        try:
            arr = [latest_data.popitem()[1][category] for _ in range(num_days)]
        except KeyError as e:
            arr = []
        return np.array(arr)

    def start_backtest(self) -> None:
        """Calls the datahandler and eventhandler repeatedly until datahandler is empty"""

        self._contine_backtest = True
        while self._contine_backtest:
            self._get_next_bar()
            self._process_events_func()
