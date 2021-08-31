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

class HighStrategy(Strategy):
    def __init__(self, conditional_positions: List[Position], data_handler: DataHandler):
        self.id = 'HIGH_STRATEGY'