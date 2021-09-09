from typing import AnyStr
from datetime import datetime

from .event import Event


class MarketEvent(Event):

    def __init__(self, ticker: AnyStr, time: datetime):
        """Created in response to price changes in underlying assets

        Args:
            ticker (AnyStr): The ticker, symbol or identifier of the underlying asset
            time (datetime): The datetime in which the event occurred
        """
        # TODO: Add price so that slippage can be calculated
        super().__init__('MARKET', ticker, time)
