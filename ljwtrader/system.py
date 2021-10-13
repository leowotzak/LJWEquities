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

    def __init__(self,
                 long: Sequence[tuple] = [],
                 short: Sequence[tuple] = [],
                 backtest: Backtest = None):
        """
        :param long: List of ticker-indicator pairs that should be long when true, defaults to []
        :type long: Sequence[tuple], optional

        :param short: List of ticker-indicator pairs that should be short when true, defaults to []
        :type short: Sequence[tuple], optional

        :param backtest: Details for the desired backtest to run, defaults to None
        :type backtest: Backtest, optional
        """

        self.queue = Queue()
        self._broker = InteractiveBrokers(self.queue)
        self._event_handler = EventHandler(self.queue)

        if backtest:
            backest.queue = self.queue
            backtest.process_events: Callable = self._event_handler.process_events

        self._data_handler = DataHandler()

        self._strategy = Strategy(self.queue,
                                  self._data_handler)

        self._portfolio = Portfolio(self.queue, self._data_handler)

        # TODO: This seems kinda sloppy tbh, goes along with how long and shorts are issued from strategy
        self._event_handler.strategy = self._strategy
        self._event_handler.portfolio = self._portfolio
        self._event_handler.broker = self._broker

    def add_position(self, *positions):
        for position in positions:
            try:
                # FIXME These should either both pass the entire position
                self._strategy.add_position_to_strategy(position)
                self._data_handler.add_symbol_to_data_handler(position.indicator.args)
            except AttributeError as e:
                logger.error(e)


    def run_backtest(self, backtest: Backtest) -> DataFrame:
        """
        Initiates a backtest with the provided details using the current system positions

        Attaches the given backtest to the trading system then executes all current
        system positions on the data

        :param backtest: Details of desired backtest, i.e start date, frequency etc...
        :type backtest: Backtest
        :return: Results of the backtest prepped for display
        :rtype: DataFrame
        """
        logger.info('Initiating backtest')
        backtest.queue = self.queue
        backtest.process_events_func = self._event_handler.process_events
        backtest.latest_symbol_data = self._data_handler.latest_symbol_data
        backtest.start_backtest()
        return self._portfolio.generate_historical_portfolio_df()
