import logging
from functools import partial
from typing import Any, Callable

import numpy as np

from ljwtrader.data import DataHandler

logger = logging.getLogger(__name__)


def indicator(func: Callable) -> Callable:
    """Takes the raw array calculation for each indicator and initializes it for the datahandler

    Args:
        func (Callable): Calculation function for the given indicator

    Returns:
        Callable: Partially initialized indicator function
    """

    # TODO: Properly document

    def wrapper(ticker: str, N: int, operator: Callable,
                value: Any) -> Callable:
        return partial(func, ticker, N, operator, value)

    return wrapper


@indicator
def XDayHigh(ticker: str, N: int, operator: Callable, value: Any,
             data_handler: DataHandler) -> bool:
    """The high for the past N bars"""
    high: np.ndarray = data_handler.get_latest_symbol_high(ticker, N)
    max_ = np.max(high) if len(high) != 0 else np.nan
    logger.info(f"{ticker}: {max_} {operator} {value}")
    return operator(max_, value)
