import logging
from typing import Callable, Any
from functools import partial

from ljwtrader.datahandler import DataHandler

logger = logging.getLogger(__name__)


def indicator(func: Callable) -> Callable:
    """Takes the raw array calculation for each indicator and initializes it for the datahandler

    Args:
        func (Callable): Calculation function for the given indicator

    Returns:
        Callable: Partially initialized indicator function
    """
    def wrapper(ticker: str, N: int, operator: Callable,
                value: Any) -> Callable:
        return partial(func, ticker, N, operator, value)

    return wrapper
