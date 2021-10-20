import logging
import operator
from datetime import datetime, timedelta
from queue import Queue
from typing import AnyStr, Callable, List, Sequence

from pandas import DataFrame

from ljwtrader.broker import InteractiveBrokers
from ljwtrader.data import Backtest, DataHandler
from ljwtrader.eventhandler import EventHandler
from ljwtrader.portfolio import Portfolio
from ljwtrader.strategy import Strategy, Position

# TODO: Need to create better logging & log formatting

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

    def __init__(self):
        self.queue = Queue()
        self._data_handler = DataHandler()
        self._strategy = Strategy(self.queue, self._data_handler)
        self._portfolio = Portfolio(self.queue, self._data_handler)
        self._broker = InteractiveBrokers(self.queue)
        self._event_handler = EventHandler(self.queue, self._strategy, self._portfolio, self._broker)

    def _add_positions(self, *positions):
        x = list(positions)
        if x:
            position = x.pop()
            self._strategy.add_position_to_strategy(position)
            self.data_handler.add_symbol_to_data_handler(position.ticker)
            self._add_positions(*x)
        else:
            return 
    
    # def add_position(self, *positions):

    #     # * Recursion candidate

    #     for position in positions:
    #         try:
    #             # FIXME These should either both pass the entire position
    #             self._strategy.add_position_to_strategy(position)
    #             self._data_handler.add_symbol_to_data_handler(position.indicator.args)
    #         except AttributeError as e:
    #             logger.error(e)


    def run(self, config):
        """
        Initiates a backtest with the provided details using the current system positions

        Attaches the given backtest to the trading system then executes all current
        system positions on the data
        """
        if isinstance(config, Backtest):
            logger.info('...Initiating backtest...')
            config.bind_to_system(self.queue, self._data_handler, self._event_handler)
            self._add_positions()
            config.start_backtest()
            return self._portfolio.generate_historical_portfolio_df()
