from typing import AnyStr
from datetime import datetime

class EventBaseClass:
    """
    Event is base class providing an interface for all subsequent (inherited) events, that will trigger further
    events in the trading infrastructure.
    """
    def __init__(self, event_type: AnyStr, ticker: AnyStr, datetime: datetime):
        self.event_type = event_type
        self.ticker     = ticker
        self.datetime   = datetime

    def __str__(self) -> str:
        return f'  --  '.join([self.ticker, self.event_type, self.datetime])

    def __repr__(self) -> str:
            f'{key}: {value}' for key, value in self.__dict__.items()
        ])