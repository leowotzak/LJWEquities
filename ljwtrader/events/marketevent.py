from typing import AnyStr
from datetime import datetime

from .event import EventBaseClass


class MarketEvent(EventBaseClass):
    """Created in response to price changes in underlying assets"""
    def __init__(self, ticker: AnyStr, time: datetime):
        """Created in response to price changes in underlying assets

        Args:
            ticker (AnyStr): The ticker, symbol or identifier of the underlying asset
            time (datetime): The datetime in which the event occurred
        """
        super().__init__('MARKET', ticker, time)
