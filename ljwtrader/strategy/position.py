from abc import ABCMeta, abstractmethod
from typing import List, Callable, Any
import numpy as np
from .indicator import HighFunc
from ljwtrader.datahandler import DataHandler

import logging
logger = logging.getLogger(__name__)


class Position(metaclass=ABCMeta):

    indicator: Any
    ticker: str
    condition: Callable[[Any], bool]
    value: Any
    conditions: List[Callable]

    @abstractmethod
    def check(self, data_handler: DataHandler) -> bool:
        """Called by strategy object on each tick"""
        raise NotImplementedError(
            """Position needs to have a condition check to know if it is active or not"""
        )


class HighPosition(Position):
    def __init__(self, indicator: Indicator, ticker: str, N: int, condition, value: Any):
        self.ID = 'X-DAY-HIGH'
        self.ticker = ticker
        self.func = indicator(ticker, N)
        self.condition = condition
        self.value = value

    def check(self, data_handler: DataHandler) -> bool:
        """Evaluates the calculated indicator against the provided condition & value"""

        return self.condition(self.func(data_handler), self.value)
        
