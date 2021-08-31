import logging
from typing import Callable

from queue import Queue
from .events import MarketEvent

logger = logging.getLogger(__name__)
class EventHandler:
    """Object that serves to route events to the proper system component based on their type"""

    def __init__(self, queue: Queue):
        self._queue = queue
    
    def _handle_market(self, event: MarketEvent):
        print(repr(event))

    def process_events(self) -> None:
        """Initiates and continues to execute backtest until there are no more bars in the datahandler"""
        EVENT_MAP = {
            'MARKET': self._handle_market
        }

        while not self._queue.empty():
            event = self._queue.get() #? Type hint?
    
            try:
                handler: Callable = EVENT_MAP[event.event_type]
            except Exception as e:
                raise e
            else:
                handler(event)