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

