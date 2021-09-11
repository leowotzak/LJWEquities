from datetime import datetime
from typing import AnyStr

from .event import Event


class StrategyEvent(Event):
    """
    Event type created in response to a change in the state of the strategy

    Strategy events are created whenever the indicators that make up a 
    strategy change from true to false or vice versa. Strategy events
    contain the context of the desired action, as in, what to order
    in response to changes in which indicators, as well as the direction
    (long, short) of the order. Once the event is created, it is passed on
    to the portfolio where it is processed before becoming an order
    """

    def __init__(self, ticker: AnyStr, time: datetime, strategy_id: str,
                 direction: str):
        """
        :param direction: Either 'long' or 'short', indicating which direction the order should go
        :type direction: str
        """
        super().__init__('STRATEGY', ticker, time)
        self.strategy_id = strategy_id
        self.direction = direction
