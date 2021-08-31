from typing import AnyStr
from datetime import datetime

from .event import EventBaseClass


class MarketEvent(EventBaseClass):
    """Created in response to price changes in underlying assets"""
    def __init__(self, ticker: AnyStr, time: datetime):
        super().__init__('MARKET', ticker, time)
