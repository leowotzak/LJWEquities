import logging
from typing import Callable, Any, List, Sequence

from ljwtrader.events import Event, StrategyEvent, MarketEvent
from ljwtrader.datahandler import DataHandler

logger = logging.getLogger(__name__)


class Strategy:

    def __init__(self,
                 queue: Sequence[Event],
                 data_handler: DataHandler,
                 long=None,
                 short=None):
        self.queue = queue
        self.data_handler = data_handler
        self.positions = {'long': {}, 'short': {}}

        for tup in long:
            self.positions['long'].update({tup[0]: []})

        if short is not None:
            for tup in short:
                self.positions['short'].update({tup[0]: []})

        for tup in long:
            self.positions['long'][tup[0]].append(tup[1])

        if short is not None:
            for tup in short:
                self.positions['short'][tup[0]].append(tup[1])

        self.directions = {}

    def add_strategy_event_to_queue(self, ticker, direction,
                                    event: MarketEvent):
        new_event = StrategyEvent(ticker, event.datetime, 'deez', direction)
        self.queue.put(new_event)

    def check_all(self, event: MarketEvent):

        for ticker, indicators in self.positions['long'].items():

            result = all(map(lambda func: func(self.data_handler), indicators))
            prev_state = self.directions.get(ticker, False)

            if result and not prev_state:
                self.directions[ticker] = True
                self.add_strategy_event_to_queue(ticker, 'BUY', event)
            elif not result and prev_state:
                self.directions[ticker] = False
                self.add_strategy_event_to_queue(ticker, 'SELL', event)

        for ticker, indicators in self.positions['short'].items():

            result = all(map(lambda func: func(self.data_handler), indicators))
            prev_state = self.directions.get(ticker, False)

            if result and not prev_state:
                prev_state = True
                self.directions[ticker] = True
                self.add_strategy_event_to_queue(ticker, 'SELL', event)
            elif not result and prev_state:
                self.directions[ticker] = False
                self.add_strategy_event_to_queue(ticker, 'BUY', event)
