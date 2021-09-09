import logging

import numpy as np

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

    def add_symbol_to_data_handler(self, ticker: str):
        """Adds a symbol to be tracked by data sources"""
        # TODO: Should add validation for symbols in DB
        self.symbols.append(ticker)
        
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
