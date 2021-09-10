from queue import Queue
import operator
from datetime import datetime, timedelta
from typing import Sequence, Callable, List, AnyStr

from ljwtrader.data import DataHandler
from ljwtrader.data import Backtest
from ljwtrader.eventhandler import EventHandler
from ljwtrader.broker import InteractiveBrokers
from ljwtrader.portfolio import Portfolio
from ljwtrader.strategy import Strategy

import logging

logging.basicConfig(
    filename='ljwtrader.log',
    level=logging.DEBUG,
    format="[%(module)s:%(lineno)3s]%(funcName)12s() -- %(message)s")
logger = logging.getLogger(__name__)


class TradingSystem:
    """
    Object that serves as an interface to the components of the trading system.

    The TradingSystem initializes all system components as well as the system-wide queue.
    All user input should be applied in this class, which acts as a unifier between 
    all of the system components. The system is composed of several components, including: 

        1) data handler
        2) event handler
        3) strategy
        4) portfolio
        5) broker

        -- For a more detailed explanation of each component, see their docstrings.

    In addition, the trading system exposes methods that allow users to use the system.
    Users are able to add positions to the system and launch backtests.
    """

    def __init__(self,
                 long: Sequence[tuple] = [],
                 short: Sequence[tuple] = [],
                 backtest: Backtest = None):

        self.queue = Queue()
        self._broker = InteractiveBrokers(self.queue)
        self._event_handler = EventHandler(self.queue)

        if backtest:
            backest.queue = self.queue
            backtest.process_events: Callable = self._event_handler.process_events

        self._data_handler = DataHandler()

        self._strategy = Strategy(self.queue,
                                  self._data_handler,
                                  long=long,
                                  short=short)

        self._portfolio = Portfolio(self.queue, self._data_handler)

        # TODO: This seems kinda sloppy tbh, goes along with how long and shorts are issued from strategy
        self._event_handler.strategy = self._strategy
        self._event_handler.portfolio = self._portfolio
        self._event_handler.broker = self._broker

    def add_position(self, indicator: tuple, direction: str):
        """Adds an indicator for the trading system's calculations"""
        if direction == 'long':
            self._strategy.add_indicator_to_strategy(indicator[0], indicator[1],
                                                     direction)
        elif direction == 'short':
            self._strategy.add_indicator_to_strategy(indicator[0], indicator[1],
                                                     direction)
        else:
            e = ValueError('Direction must be either "long" or "short"')
            logger.error(e)

        self._data_handler.add_symbol_to_data_handler(indicator[0])

    def run_backtest(self, backtest: Backtest):
        logger.info('Initiating backtest')
        backtest.symbols = self._data_handler.symbols
        backtest.queue = self.queue
        backtest.process_events_func = self._event_handler.process_events
        backtest.latest_symbol_data = self._data_handler.latest_symbol_data
        backtest.start_backtest()
