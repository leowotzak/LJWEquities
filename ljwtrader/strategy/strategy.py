from collections.abc import ABCMeta, abstractmethod
from operator import operator
from typing import List

from ljwtrader.datahandler import DataHandler
from .position import Position
from indicator import Indicator


class Strategy(meta_class=ABCMeta):
    """
    The Strategy is simply a collection of one or more condition-position groups. 
    Buy (Sell) or Sell (Buy) what, when x, y, & z are true/false?
    """

    id: str
    conditional_positions: List[Position]
    data_handler: DataHandler

    @abstractmethod
    def check_all(self):
        """Evaluate the status of each conditional position in strategy"""
        return NotImplementedError("Strategy must have a check_all() function")


class StrategySpec(Strategy):
    def __init__(self, conditional_positions: List[Position],
                 data_handler: DataHandler):

        self.positions = conditional_positions
        self.data_handler = data_handler

    def check_all(self):
        results = []
        for position in self.positions:
            calc_value = position.check(self.data_handler)
            results.append(calc_value)
            logger.debug(f'Ticker: {position.ticker} Check: {calc_value}')
        print(results)

