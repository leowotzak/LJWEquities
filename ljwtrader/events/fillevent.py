from datetime import datetime
from typing import AnyStr

from .event import Event


class FillEvent(Event):
    """
    Created in response to a fulfilled order event

    After an order has been placed, it needs to be executed by the broker, 
    which will not necessarily occur at the same price or quantity as the 
    original order. To handle this, fill events have their own independent 
    price and quantity. In addition, fill events contain details about any 
    broker/exchange fees and slippage.
    """

    def __init__(self,
                 ticker: AnyStr,
                 time: datetime,
                 strategy_id: str,
                 direction: str,
                 price: float,
                 quantity: int,
                 commission: float = 0,
                 slippage: float = 0.0):
        super().__init__('FILL', ticker, time)
        self.strategy_id = strategy_id
        self.direction = direction
        self.price = price
        self.quantity = quantity
        self.commission = commission
        self.slippage = slippage
