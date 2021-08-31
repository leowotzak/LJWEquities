from ljwtrader.datahandler import DataHandler
import numpy as np
from abc import ABCMeta, abstractmethod

import logging
logger = logging.getLogger(__name__)

def HighFunc(ticker: str, N: int):
    """Takes inputs and returns a function that calculates the metric"""

    def calc(data_handler: DataHandler):
        """calculation function that is provided to parent"""
        high = data_handler.get_latest_symbol_high(ticker, N)
        return np.max(high) if len(high) != 0 else np.nan

    return calc

def XDayHigh(ticker: str, N: int):
    """Takes inputs and returns a function that calculates the metric"""

    def calc(data_handler: DataHandler):
        """calculation function that is provided to parent"""
        high = data_handler.get_latest_symbol_high(ticker, N)
        return np.max(high) if len(high) != 0 else np.nan

    return calc

def XDayLow(ticker: str, N: int):
    """Takes inputs and returns a function that calculates the metric"""

    def calc(data_handler: DataHandler):
        """calculation function that is provided to parent"""
        high = data_handler.get_latest_symbol_low(ticker, N)
        return np.min(high) if len(high) != 0 else np.nan

    return calc
