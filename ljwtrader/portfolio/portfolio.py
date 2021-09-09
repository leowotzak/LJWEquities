import logging
from typing import NoReturn
from datetime import datetime

from ljwtrader.events import Event, StrategyEvent, OrderEvent, FillEvent

logger = logging.getLogger(__name__)


class Portfolio:
    """
    Responsible for handling and implementing all portfolio logic for the trading system. 
    At a high level, the portfolio receives signals from all of the strategies that constitute
    it. The portfolio can then decide whether to follow through with these strategies, or it can 
    ignore them in favor of some other over-arching portfolio strategy. The portfolio should also 
    keep track of any rebalancing and issue orders to achieve certain targets.
    """

    def __init__(self, queue, data_handler):
        self._queue = queue
        self.data_handler = data_handler
        self._positions = {}
        self._holdings = {'cash': 100000, 'commission': 0, 'slippage': 0}

        # ? Should these be lists or dicts? they're going to be converted to
        # ? DataFrames for pyfolio
        self._historical_positions = {}
        self._historical_holdings = {}

    def get_percent_of_cash_holdings(self, percent: float) -> float:
        """Returns the dollar value of a given % of the portfolio's cash on hand"""
        return self._holdings['cash'] * percent

    def trigger_order(self, event: StrategyEvent) -> NoReturn:
        """Takes a signal event and applies portfolio logic"""
        self._place_order(event)

    def _place_order(self, event: StrategyEvent) -> NoReturn:
        """Generates an OrderEvent and places it on the queue"""
        new_event = OrderEvent(event.ticker, event.datetime, event.strategy_id,
                               event.direction, 50.0, 1)
        self._queue.put(new_event)

    def _update_historicals(self, timestamp: datetime) -> NoReturn:
        """Stores current portfolio values in historicals dictionaries"""

        # ! I need to ensure that the portfolios arent duplicated for each date
        # ! by multiple market events

        self._historical_positions[timestamp] = self._positions.copy()
        self._historical_holdings[timestamp] = self._holdings.copy()

    def update_holdings_from_fill(self, event: FillEvent) -> NoReturn:
        """Takes an FillEvent and updates the share/contract amounts & dollar amounts of the portfolio"""
        if event.direction == 'BUY':
            direction = 1
        elif event.direction == 'SELL':
            direction = -1
        else:
            raise ValueError('event direction must be either "BUY" or "SELL"')

        current_quantity = self._positions.get(event.ticker, 0)
        self._positions[
            event.ticker] = current_quantity + direction * event.quantity

        current_holding = self._holdings.get(event.ticker, 0)
        self._holdings[
            event.
            ticker] = current_holding + direction * event.quantity * event.price
        self._holdings['cash'] -= direction * event.quantity * event.price
        self._holdings['cash'] -= event.commission + event.slippage
        self._holdings['commission'] += event.commission
        self._holdings['slippage'] += event.slippage

        logger.info(
            "%s -- Current quantity: %i, Current holding: %f, Current cash: %f, Current commission: %f, Current slippage: %f"
            % (event.ticker, self._positions[event.ticker],
               self._holdings[event.ticker], self._holdings['cash'],
               self._holdings['commission'], self._holdings['slippage']))

    def update_holdings_from_market(self):
        """Updates the dollar amounts of the portfolio in response to a change in market prices"""
        
