import logging
from functools import partial
from typing import Any, Callable

import numpy as np

from ljwtrader.data import DataHandler

logger = logging.getLogger(__name__)


def indicator(func: Callable) -> Callable:
    """Decorator function that allows indicators to be partially initialized prior to execution by trading system"""

    def wrapper(*args, **kwargs) -> Callable:
        return partial(func, *args, **kwargs)

    return wrapper


def pct_change(arr: np.ndarray) -> np.ndarray:
    """Converts an array of values into an array of the % change of values"""
    return np.diff(arr) / arr[1:] * 100


@indicator
def XDayHigh(ticker: str, N: int, operator: Callable, value: Any,
             data_handler: DataHandler) -> bool:
    """The high for the past N bars"""
    high: np.ndarray = data_handler.get_latest_symbol_high(ticker, N)
    max_ = np.max(high) if len(high) != 0 else np.nan
    logger.info(f"{ticker}: {max_} {operator} {value}")
    return operator(max_, value)

@indicator
def ZScore(ticker_one: str,
           ticker_two: str,
           N_short: int = None,
           N_long: int = None,
           data_handler: DataHandler = None,
           operator: Callable = None,
           value: float = None) -> float:
    """The Z-score utilizing the provided mean and standard deviation lookbacks"""
    ticker_one_returns = data_handler.get_latest_symbol_adj_close(
        ticker_one, N_long)
    ticker_two_returns = data_handler.get_latest_symbol_adj_close(
        ticker_two, N_long)

    # HACK Cannot divide by zero, probably a cleaner way to do this?
    if len(ticker_two_returns) == 0:
        return False

    cointegrated_returns = np.divide(ticker_one_returns, ticker_two_returns)

    short_mean = np.mean(cointegrated_returns[:N_short])
    long_mean = np.mean(cointegrated_returns)
    std = np.std(cointegrated_returns)
    result = (short_mean - long_mean) / std
    logger.info(f"{ticker_one} -- {ticker_two}: {result} {operator} {value}")
    return operator(result, value)
