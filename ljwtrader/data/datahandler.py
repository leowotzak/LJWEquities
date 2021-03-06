import logging

import numpy as np

logger = logging.getLogger(__name__)


def convert_bar(row):
    index, data = row     #* These are the fields the system watches
    output_dict = dict((k, v)
                       for k, v in data.to_dict().items()
                       if k in ['ticker', 'adj_close_price', 'high_price'])
    output_dict['timestamp'] = index
    return output_dict


class DataHandler:
    """
    The Data Handler object is a crucial component of the trading system. At a high level, 
    the Data Handler serves as an interface for the trading system to interact with data 
    of different forms and varieties (ex. historical bar data, stream data). Regardless of 
    the data source, the Data Handler allows the trading system to retrieve the most recent 
    tracked data, assuming the data is separated at regular intervals, defined as the 
    frequency of the Data Handler. In addition, the Data Handler should be able to generate 
    Market Events for the trading system to react to in response to both the next bar of a 
    backtest and the next bar of a live-streamed data source.
    """

    def __init__(self):
        self.symbols = []
        self.latest_symbol_data = {}

    def _get_latest_symbol_data(self, ticker: str, category: str,
                                num_days: int) -> np.ndarray:
        # * Retrieves the bars for a given ticker's category over the # of specified days

        latest_data = self.latest_symbol_data.get(ticker, {}).copy()

        try:
            arr = [latest_data.popitem()[1][category] for _ in range(num_days)]
        except KeyError as e:
            arr = []
        return np.array(arr)

    def add_symbol_to_data_handler(self, tickers: tuple[str]):
        """Adds a symbol to be tracked by data sources

        Args:
            ticker (str): ticker of symbol to track with data handler
        """
        # TODO: Should add validation for symbols in DB
        map(self.symbols.append, tickers)

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
