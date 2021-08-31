import logging
import sqlite3

import pandas as pd
from ljwtrader.events import MarketEvent

logger = logging.getLogger(__name__)


class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, queue_, start_date, end_date, frequency, vendor, process_events_func):
        self._queue = queue_
        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency
        self._vendor = vendor
        self._process_events_func = process_events_func

        self.data = (
            (index, row)
            for index, row in pd.read_sql('SELECT * FROM daily_bar_data',
                                          sqlite3.connect('app.db'),
                                          index_col='timestamp')
                                          .sort_index()
                                          .iterrows())

            self._process_events_func()

