import logging
from typing import Callable, Mapping, NoReturn, Sequence

from ljwtrader.events import (Event, EventType, FillEvent, MarketEvent, OrderEvent,
                              StrategyEvent)
from ljwtrader.portfolio import Portfolio
from ljwtrader.strategy import Strategy

logger = logging.getLogger(__name__)


class EventHandler:
    """
    Object that serves to route events to the proper system component based on their type

    The event handler consists of a collection of event handlers, an event map that 
    maps each event type to the proper handler, and process_events() method.
    """

    def __init__(self, queue: Sequence[Event], strategy: Strategy, portfolio: Portfolio, broker):
        self.queue = queue
        self._most_recent_event: Event = None
        self.strategy = strategy
        self.portfolio = portfolio
        self.broker = broker

    def _handle_market(self, event: MarketEvent):
        self.strategy.check_all(event)

    def _handle_strategy(self, event: StrategyEvent):
        self.portfolio.process_signal_event(event)

    def _handle_order(self, event: OrderEvent):
        self.broker.process_order_event(event)

    def _handle_fill(self, event: FillEvent):
        self.portfolio.update_holdings_from_fill(event)

    def process_events(self):
        """
        Pops each event in the queue and directs it to the proper handler

        Event types are looked up and used as keys to a premade event map,
        if no handler is found an error is logged

        :raises KeyError: Unknown event type, no handler exists
        """

        EVENT_MAP: Mapping[EventType, Callable] = {
            EventType.MARKET: self._handle_market,
            EventType.STRATEGY: self._handle_strategy,
            EventType.ORDER: self._handle_order,
            EventType.FILL: self._handle_fill,
        }

        while not self.queue.empty():
            event = self.queue.get()
            try:
                event_handler = EVENT_MAP[event.event_type]
            except KeyError as e:
                logger.error(e)
            else:
                logger.debug(f"Handling {event.event_type} event")
                self._most_recent_event = event.datetime
                event_handler(event)

        # HACK Figure out a better way to pass the current analysis date to the portfolio
        # ! Shouldn't rely on whatever is left over in the event to determine the timestamp
        self.portfolio.update_holdings_from_market(event.datetime)