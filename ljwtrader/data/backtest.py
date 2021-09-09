import logging
import sqlite3
from datetime import datetime, timedelta
from typing import AnyStr, Callable, Generator, List, NoReturn, Sequence

import pandas as pd
import numpy as np
from .models import DailyBar, Symbols
from ljwtrader.events import MarketEvent, Event

logger = logging.getLogger(__name__)


def convert_bar(row):
    index, data = row  #* These are the fields the system watches
    output_dict = dict((k, v)
                       for k, v in data.to_dict().items()
                       if k in ['ticker', 'adj_close_price', 'high_price'])
    output_dict['timestamp'] = index
    return output_dict


class Backtest:
    """Object that handles all data access for other system components"""

    def __init__(
        self,
        start_date: datetime = datetime.today() - timedelta(days=365),
        end_date: datetime = datetime.today() - timedelta(days=1),
        frequency: str = '1d',
        vendor: str = 'av',
    ):

        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency
        self._vendor = vendor
        self.symbols: List[str] = None
        self.data = None
        self.queue = None
        self._continue_backtest = False
        self.process_events_func: Callable = None

    def _get_next_bar(self):
        # * Retrieves next bar from datahandler and places it on queue
        try:
            timestamp, bar_data = next(self.data)
        except StopIteration:
            self._continue_backtest = False
        else:
            for bar in map(convert_bar, bar_data.iterrows()):
                ticker = bar['ticker']
                self.queue.put(MarketEvent(bar['ticker'], timestamp))

                try:
                    self.latest_symbol_data[ticker]
                except KeyError as e:
                    logger.error(e)
                    self.latest_symbol_data[ticker] = {}
                finally:
                    ticker_data = self.latest_symbol_data[ticker][timestamp] = bar

    def start_backtest(self) -> NoReturn:
        """Calls the datahandler and eventhandler repeatedly until datahandler is empty"""

        # TODO: Should rename this, I think it was tuple because when iterated it comes out as a (index, row)
        
        self.data = (tup for tup in pd.read_sql(
            "SELECT * FROM symbols JOIN daily_bar_data ON symbols.symbol_id=daily_bar_data.symbol_id WHERE symbols.ticker IN ('%s')"
            % "', '".join(self.symbols),
            sqlite3.connect('app.db'),
            index_col='timestamp').sort_index().groupby(level=0))

        self._continue_backtest = True
        while self._continue_backtest:
            self._get_next_bar()
            self.process_events_func()
