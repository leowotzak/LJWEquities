from abc import ABCMeta, abstractmethod
from typing import List, Callable
import numpy as np
from .indicator import HighFunc


class Position(metaclass=ABCMeta):

    indicator: Indicator
    condition: Callable[[Any], bool]
    value: Any
    conditions: List[Callable]

    @abstractmethod
    def check(self, arr: np.ndarray) -> bool:
        """Called by strategy object on each tick"""
        raise NotImplementedError(
            """Position needs to have a condition check to know if it is active or not"""
        )


class HighPosition(Position):
    def __init__(self, indicator: Indicator, condition, value: Any):
        self.indicator = indicator
        self.condition = condition
        self.value = value
