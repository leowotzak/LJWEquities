from typing import AnyStr
from datetime import datetime

from .event import Event


class StrategyEvent(Event):
    """Created in response to price changes in underlying assets"""
    def __init__(self, ticker: AnyStr, time: datetime, strategy_id: str, direction: str):
        super().__init__('STRATEGY', ticker, time)
        self.strategy_id = strategy_id
        self.direction = direction