from abc import ABCMeta, abstractmethod
import logging
import operator
from typing import List, AnyStr

import numpy as np
from ljwtrader.datahandler import DataHandler
from ljwtrader.strategy.indicator import XDayHigh

logger = logging.getLogger(__name__)


class Strategy(metaclass=ABCMeta):
    """
    The Strategy is simply a collection of one or more condition-position groups. 
    Buy (Sell) or Sell (Buy) what, when x, y, & z are true/false?
    """

    @abstractmethod
    def check_all(self):
        """Evaluate the status of each conditional position in strategy"""
        return NotImplementedError("Strategy must have a check_all() function")


class Strategy(Strategy):
    def __init__(self, symbols: List[AnyStr], N: int, operator_, value: float,
                 data_handler: DataHandler):

        self.symbols = symbols
        self.N = N
        self.operator = operator_
        self.data_handler = data_handler
        self.value = value

        self.conditional_positions = []
        for symbol in self.symbols:
            self.conditional_positions.append(XDayHigh(symbol, self.N, self.operator, self.value))


    def check_all(self):
        results = []
        for position in self.conditional_positions:
            calc_value = position(self.data_handler)
            results.append(calc_value)
            logger.debug(f'Check: {calc_value}')
