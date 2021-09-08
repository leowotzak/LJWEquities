from typing import AnyStr
from datetime import datetime

from .event import Event


class FillEvent(Event):
    """Created in response to price changes in underlying assets"""
    def __init__(self, ticker: AnyStr, time: datetime, strategy_id: str, direction: str, price: float, quantity: int, commission: float = 0, slippage: float = 0.0):
        super().__init__('FILL', ticker, time)
        self.strategy_id = strategy_id
        self.direction = direction
        self.price = price
        self.quantity = quantity
        self.commission = commission
        self.slippage = slippage