from datetime import datetime
from typing import AnyStr

from .event import Event, EventType


class MarketEvent(Event):
    """
    Event type created in response to changes in underlying assets

    Market events are created in order to 'advance' the trading system.
    In the context of live trading, that means every time an update
    comes from the data feed. In the context of a backtest, that means
    after each event in the previous bar has been processed
    """

    def __init__(self, ticker: AnyStr, time: datetime, price: float):
        super().__init__(EventType.MARKET, ticker, time)
        self.price = price
