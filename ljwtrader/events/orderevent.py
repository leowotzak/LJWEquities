from typing import AnyStr
from datetime import datetime

from .event import Event


class OrderEvent(Event):
    """Created in response to price changes in underlying assets"""
    def __init__(self, ticker: AnyStr, time: datetime, strategy_id: str, price: float, quantity: int):
        super().__init__('ORDER', ticker, time)
        self.strategy_id = strategy_id
        self.price = price
        self.quantity = quantity