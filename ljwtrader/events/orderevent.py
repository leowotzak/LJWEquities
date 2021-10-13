from datetime import datetime
from typing import AnyStr

from .event import Event


class OrderEvent(Event):
    """
    Event type created to change the current state of portfolio holdings

    Order events are created either after a signal event has successfully
    passed any portfolio-level logic, or a portfolio-level event has
    occurred, such as a rebalancing or reallocation.
    """

    def __init__(self, ticker: AnyStr, time: datetime, strategy_id: str,
                 direction: str, price: float, quantity: int):
        super().__init__('ORDER', ticker, time)
        self.strategy_id = strategy_id
        self.direction = direction
        self.price = price
        self.quantity = quantity