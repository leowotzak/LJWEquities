from ljwtrader.datahandler import DataHandler
import numpy as np
from abc import ABCMeta, abstractmethod


class Indicator(metaclass=ABCMeta):
    
    id: str
    N: int

    @abstractmethod
    def calc(self, arr: np.ndarray) -> Any:
        """Calculation that the indicator will perform"""
        raise NotImplementedError("An indicator must have a calculation implementation")


class High(Indicator):
    def __init__(self, N: int):
        self.id: str = 'X-DAY-HIGH'
        self.N: int = N

    def calc(self, arr: np.ndarray) -> Any:
        """Calculates high of high-price for N days"""
        return np.max(arr)


