import logging
import sqlite3
from datetime import datetime, timedelta
from typing import AnyStr, Callable, Generator, List, NoReturn, Sequence

import numpy as np
import pandas as pd

from ljwtrader.events import Event, MarketEvent
from ljwtrader.utils import convert_bar

from .models import DailyBar, Symbols

logger = logging.getLogger(__name__)

class Backtest:
    """Object that handles all data access for other system components"""

    def __init__(
        self,
        *positions,
        start_date: datetime = None,
        end_date: datetime = None,
        # TODO Change these (below) to enumerations
        frequency: str = '1d',
        vendor: str = 'av',
    ):

        self._start_date = start_date if start_date else datetime.today() - timedelta(days=365)
        self._end_date = end_date if end_date else datetime.today() - timedelta(days=1)
        self._frequency = frequency
        self._vendor = vendor
        self.symbols = set()
        self.data = None
        self.queue = None
        self._continue_backtest = False
        self._data_handler = None
        self._event_handler = None

    def bind_to_system(self, queue, data_handler, event_handler):
        self.queue = queue
        self.data_handler = data_handler
        self._event_handler = event_handler

    def _get_next_bar(self):
        # * Retrieves next bar from datahandler and places it on queue
        try:
            timestamp, bar_data = next(self.data)
        except StopIteration:
            self._continue_backtest = False
        else:
            for bar in map(convert_bar, bar_data.iterrows()):
                ticker = bar['ticker']
                self.queue.put(MarketEvent(ticker, timestamp, bar['adj_close_price']))

                # ! I think the try-except block isn't writing the new dictionary for empty key
                try:
                    self.data_handler.latest_symbol_data[ticker]
                except KeyError as e:
                    logger.error(e)
                    self.data_handler.latest_symbol_data[ticker] = {}
                finally:
                    ticker_data = self.data_handler.latest_symbol_data[ticker][
                        timestamp] = bar

    def add_position_to_backtest(self, *positions):
        for position in positions:
            self.symbols.add(position.ticker)

    def start_backtest(self) -> NoReturn:
        """Calls the datahandler and eventhandler repeatedly until datahandler is empty"""
        self.data = ( tup for tup in  pd.read_sql(
            "SELECT * FROM symbols JOIN daily_bar_data ON symbols.symbol_id=daily_bar_data.symbol_id WHERE symbols.ticker IN ('%s')"
            % "', '".join(self.symbols),
            sqlite3.connect('app.db'),
            index_col='timestamp').sort_index().groupby(level=0))
        
        self._continue_backtest = True
        while self._continue_backtest:
            self._get_next_bar()
            self._event_handler.process_events()
            