import logging
from typing import Callable, NoReturn, Mapping, Sequence

from .strategy import Strategy
from .portfolio import Portfolio
from .events import Event, MarketEvent, StrategyEvent, OrderEvent, FillEvent
from ljwtrader.broker import InteractiveBrokers

logger = logging.getLogger(__name__)


class EventHandler:
    """
    Object that serves to route events to the proper system component based on their type
    """
    def __init__(self, queue: Sequence[Event]):
        self._queue = queue
        self.strategy: Strategy = None
        self.portfolio: Portfolio = None
        self.broker: InteractiveBrokers = None


    def _handle_market(self, event: MarketEvent) -> NoReturn:
        self.strategy.check_all(event)

    def _handle_strategy(self, event: StrategyEvent) -> NoReturn:
        self.portfolio.trigger_order(event)

    def _handle_order(self, event: OrderEvent) -> NoReturn:
        self.broker.generate_fill_order(event)

    def _handle_fill(self, event: FillEvent) -> NoReturn:
        pass

    def process_events(self) -> NoReturn:
        """Pops each event in the queue and assigns it to the proper handler

        Currently handles event types: MarketEvent, StrategyEvent

        Raises:
            e (KeyError): The type of the given event is not in the event map, i.e. does not exist
        """
        EVENT_MAP: Mapping[Event, Callable] = {
            'MARKET': self._handle_market,
            'STRATEGY': self._handle_strategy,
            'ORDER': self._handle_order,
            'FILL': self._handle_fill,
        }

        while not self._queue.empty():
            event = self._queue.get()
            try:
                event_handler = EVENT_MAP[event.event_type]
            except KeyError as e:
                logger.error(e)
            else:
                logger.info(f"Handling {event.event_type} event")
                event_handler(event)
