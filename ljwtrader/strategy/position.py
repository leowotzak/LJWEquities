from abc import ABCMeta, abstractmethod
from typing import List, Callable, Any
import numpy as np
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
