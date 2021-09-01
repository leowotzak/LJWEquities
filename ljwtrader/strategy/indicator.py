import logging
from typing import Any, Callable, NewType

import numpy as np
from ljwtrader.datahandler import DataHandler
from ljwtrader.strategy import StrategySpec

Indicator = NewType('Indicator', Callable[[DataHandler], float])

logger = logging.getLogger(__name__)


def XDayHigh(ticker: str, N: int, condition: Callable[[Any], Any],
             value: float) -> Indicator:
    """Returns the maximum of the high prices over past N days"""
    def XDayHigh(data_handler: DataHandler) -> float:
        high: np.ndarray = data_handler.get_latest_symbol_high(ticker, N)
        max_: float = np.max(high) if len(high) != 0 else np.nan
        logger.debug(high)
        logger.info(max_)
        return max_

    cond = condition

    return condition(XDayHigh, value)
