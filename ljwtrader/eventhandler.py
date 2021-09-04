import logging
from typing import Callable

from queue import Queue
from .strategy import Strategy
from .events import MarketEvent, StrategyEvent

logger = logging.getLogger(__name__)


class EventHandler:
    """
    Object that serves to route events to the proper system component based on their type
    """
    def __init__(self, queue: Sequence[Event]):
        self._queue = queue
        self.strategy: Strategy = None

    def _handle_market(self, event: MarketEvent) -> NoReturn:
        self.strategy.check_all()

    def _handle_strategy(self, event: StrategyEvent) -> NoReturn:
        pass

    def process_events(self) -> NoReturn:
        """Pops each event in the queue and assigns it to the proper handler

        Currently handles event types: MarketEvent, StrategyEvent

        Raises:
            e (KeyError): The type of the given event is not in the event map, i.e. does not exist
        """
        EVENT_MAP: Mapping[Event, Callable] = {
            'MARKET': self._handle_market,
            'STRATEGY': self._handle_strategy
        }

        while not self._queue.empty():
            event = self._queue.get()  #? Type hint?

            try:
                handler: Callable = EVENT_MAP[event.event_type]
            except Exception as e:
                logger.error(e)
                raise e
            else:
                handler(event)
