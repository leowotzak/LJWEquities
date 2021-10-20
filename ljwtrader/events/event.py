import logging
from datetime import datetime
from typing import AnyStr
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(Enum):
    MARKET = 1
    STRATEGY = 2
    ORDER = 3
    FILL = 4


class Event:
    """
    Base class for all subsequent (inherited) events that provides some convenience methods

    Currently, Event only exposes __str__ and __repr__ methods for its children
    """

    def __init__(self, event_type: EventType, ticker: AnyStr, datetime: datetime):
        """
        :param event_type: Context in which event was generated in (i.e. Market)
        :type event_type: AnyStr
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

@dataclass
class Test:
    event_type: Event
    ticker: str
    datetime: datetime

