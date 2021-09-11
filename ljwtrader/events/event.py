import logging
from datetime import datetime
from typing import AnyStr

logger = logging.getLogger(__name__)


class Event:
    """
    Base class for all subsequent (inherited) events that provides some convenience methods

    Currently, Event only exposes __str__ and __repr__ methods for its children
    """

    def __init__(self, event_type: AnyStr, ticker: AnyStr, datetime: datetime):
        """
        :param event_type: Context in which event was generated in (i.e. Market)
        :type event_type: AnyStr
        :param ticker: Ticker of the asset that generated the event
        :type ticker: AnyStr
        :param datetime: Timestamp of the event instance
        :type datetime: datetime
        """

        self.event_type = event_type
        self.ticker = ticker
        self.datetime = datetime
        logger.debug(
            f'Creating {self.event_type} event for ticker {self.ticker} @ {self.datetime}'
        )

    def __str__(self) -> str:
        return f'  --  '.join(
            [self.ticker, self.event_type,
             str(self.datetime)])

    def __repr__(self) -> str:
        return ' -- '.join(
            [f'{key}: {value}' for key, value in self.__dict__.items()])
