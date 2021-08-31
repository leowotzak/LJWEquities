from typing import AnyStr
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class EventBaseClass:
    """
    Event is base class providing an interface for all subsequent (inherited) events, that will trigger further
    events in the trading infrastructure.
    """
    def __init__(self, event_type: AnyStr, ticker: AnyStr, datetime: datetime):
        self.event_type = event_type
        self.ticker     = ticker
        self.datetime   = datetime
        logger.debug(f'Creating {self.event_type} event for ticker {self.ticker} @ {self.datetime}')

    def __str__(self) -> str:
        return f'  --  '.join([self.ticker, self.event_type, str(self.datetime)])

    def __repr__(self) -> str:
        return ' -- '.join([
            f'{key}: {value}' for key, value in self.__dict__.items()
        ])