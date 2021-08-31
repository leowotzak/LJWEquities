import logging
import sqlite3
from datetime import datetime
from queue import Queue
from typing import AnyStr, Callable, Generator
from pandas import Series

import pandas as pd
from .events import MarketEvent

logger = logging.getLogger(__name__)


class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, queue_: Queue, start_date: datetime, end_date: datetime, frequency: AnyStr, vendor: AnyStr, process_events_func: Callable[[None], None]):
        self._process_events_func = process_events_func

        self.data: Generator[Series]= (
            (index, row)
            for index, row in pd.read_sql('SELECT * FROM daily_bar_data',
                                          sqlite3.connect('app.db'),
                                          index_col='timestamp')
                                          .sort_index()
                                          .iterrows())

    def _get_next_bar(self) -> None:
        try:
            index, row = next(self.data)
        except StopIteration:
            self._contine_backtest = False
        else:
            self._queue.put(MarketEvent('AAPL', index))

    def start_backtest(self) -> None:
        self._contine_backtest = True
        while self._contine_backtest:
            self._get_next_bar()
            self._process_events_func()

