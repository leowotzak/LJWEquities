import logging
import sqlite3
from datetime import datetime
from typing import AnyStr, Callable, Generator, List, NoReturn, Sequence

import pandas as pd
import numpy as np
from ljwtrader.data import DailyBar, Symbols
from ljwtrader.events import MarketEvent, Event

logger = logging.getLogger(__name__)


def convert_bar(row):
    index, data = row  #* These are the fields the system watches
    output_dict = dict((k, v)
                       for k, v in data.to_dict().items()
                       if k in ['ticker', 'adj_close_price', 'high_price'])
    output_dict['timestamp'] = index
    return output_dict


class DataHandler:
    """Object that handles all data access for other system components"""

    def __init__(self, symbols: List[AnyStr], queue_: Sequence[Event],
                 start_date: datetime, end_date: datetime, frequency: AnyStr,
                 vendor: AnyStr, process_events_func: Callable[[None], None]):

        self._positions = symbols
        self._queue = queue_
        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency
        self._vendor = vendor
        self._contine_backtest = False
        self._process_events_func = process_events_func
        self.latest_symbol_data = {sym: {} for sym in self._positions}

        self.data = (tup for tup in pd.read_sql(
            "SELECT * FROM symbols JOIN daily_bar_data ON symbols.symbol_id=daily_bar_data.symbol_id WHERE symbols.ticker IN ('%s')"
            % "', '".join(self._positions),
            sqlite3.connect('app.db'),
            index_col='timestamp').sort_index().groupby(level=0))

    def _get_next_bar(self) -> NoReturn:
        # * Retrieves next bar from datahandler and places it on queue
        try:
            timestamp, bar_data = next(self.data)
        except StopIteration:
            self._contine_backtest = False
        else:
            for bar in map(convert_bar, bar_data.iterrows()):
                self._queue.put(MarketEvent(bar['ticker'], bar['timestamp']))
                self.latest_symbol_data[bar['ticker']][timestamp] = bar

    def _get_latest_symbol_data(self, ticker: str, category: str,
                                num_days: int) -> np.ndarray:
        # * Retrieves the bars for a given ticker's category over the # of specified days
        latest_data = self.latest_symbol_data[ticker].copy()
        try:
            arr = [latest_data.popitem()[1][category] for _ in range(num_days)]
        except KeyError as e:
            arr = []
        return np.array(arr)

    # * Convenience methods
    # * Used as the building blocks for indicators, positions, and strategies

    def get_latest_symbol_open(self, ticker: str, num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'open_price', num_days)

    def get_latest_symbol_high(self, ticker: str, num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'high_price', num_days)

    def get_latest_symbol_low(self, ticker: str, num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'low_price', num_days)

    def get_latest_symbol_close(self, ticker: str, num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'close_price', num_days)

    def get_latest_symbol_adj_close(self, ticker: str,
                                    num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'adj_close_price', num_days)

    def get_latest_symbol_volume(self, ticker: str,
                                 num_days: int) -> np.ndarray:
        return self._get_latest_symbol_data(ticker, 'volume', num_days)

    def get_latest_pct_change(self, ticker: str, num_days: int) -> np.ndarray:
        arr = self._get_latest_symbol_data(ticker, 'adj_close_price', num_days) 
        return np.diff(arr) / arr[1:]

    def start_backtest(self) -> NoReturn:
        """Calls the datahandler and eventhandler repeatedly until datahandler is empty

        Returns:
            NoReturn: 
        """
        self._contine_backtest = True
        while self._contine_backtest:
            self._get_next_bar()
            self._process_events_func()
