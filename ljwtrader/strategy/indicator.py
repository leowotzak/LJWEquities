import logging
import operator
from typing import Any, AnyStr, Callable, NewType

import numpy as np
from ljwtrader.datahandler import DataHandler

Indicator = NewType('Indicator', Callable[[DataHandler], bool])

logger = logging.getLogger(__name__)

# ! Issue with how this function is added to new objects 
# ! To call the outer function,  no self attribute is needed for
# ! But when you do not use self you cannot use the associated ticker

def XDayHigh(ticker: str, N: int, condition: Callable[[Any], Any],
             value: float) -> Indicator:
    """Returns the maximum of the high prices over past N days"""
    def XDayHigh(self, data_handler: DataHandler) -> float:
        high: np.ndarray = data_handler.get_latest_symbol_high(self.ticker, N)
        max_: float = np.max(high) if len(high) != 0 else np.nan
        logger.debug(high)
        logger.info(max_)
        return max_

    return lambda data_handler: operator.lt(XDayHigh(data_handler), value)
