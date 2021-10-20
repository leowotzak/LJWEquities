import logging
from datetime import datetime
from queue import Queue
from typing import NoReturn

import pandas as pd

from ljwtrader.data import DataHandler
from ljwtrader.events import Event, FillEvent, OrderEvent, StrategyEvent
from ljwtrader.portfolio.ordersizer import OrderSizer, PercentPortfolioValue

logger = logging.getLogger(__name__)

DEFAULT_ORDER_SIZER_PERCENT = .1
DEFAULT_STARTING_CASH = 100_000


class Portfolio:
    """
    Responsible for handling and implementing all portfolio logic for the trading system. 

    At a high level, the portfolio receives signals from all of the strategies that constitute
    it. The portfolio can then decide whether to follow through with these strategies, or it can 
    ignore them in favor of some other over-arching portfolio strategy. The portfolio should also 
    keep track of any rebalancing and issue orders to achieve certain targets.
    """

    def __init__(self, queue: Queue, data_handler: DataHandler, order_sizer: OrderSizer = None):
        self.queue = queue
        self.data_handler = data_handler
        self._positions = {}
        self._holdings = {'cash': DEFAULT_STARTING_CASH, 'commission': 0, 'slippage': 0}
        self._historical_positions = {}
        self._historical_holdings = {}

        self.order_sizer = 'temp' if order_sizer else PercentPortfolioValue(self, DEFAULT_ORDER_SIZER_PERCENT)

    def get_percent_of_cash_holdings(self, percent: float) -> float:

        # ? Should this be a part of a @property getter/setter?

        return self._holdings['cash'] * percent

    def process_signal_event(self, event: StrategyEvent) -> NoReturn:
        # * Currently serves as a wrapper function so that portfolio logic may be applied
        self._process_signal_event(event)

    def _process_signal_event(self, event: StrategyEvent) -> NoReturn:
        p = event.price
        new_event = OrderEvent(event.ticker, event.datetime, event.strategy_id,
                               event.direction, p, self._order_sizer.size_order(p))
        self.queue.put(new_event)

    def update_holdings_from_fill(self, event: FillEvent) -> NoReturn:
        direction = self._get_order_direction(event.direction)
        current_quantity = self._positions.get(event.ticker, 0)
        current_holding = self._holdings.get(event.ticker, 0)

        self._positions[
            event.ticker] = current_quantity + direction * event.quantity
        self._holdings[
            event.
            ticker] = current_holding + direction * event.quantity * event.price

        self._holdings['cash'] -= direction * event.quantity * event.price
        self._holdings['cash'] -= event.commission + event.slippage
        self._holdings['commission'] += event.commission
        self._holdings['slippage'] += event.slippage

        # FIXME This isn't logging correctly from what I'm seeing on debugger

        logger.info(
            f"{event.ticker} -- {self._positions[event.ticker]} {self._holdings[event.ticker]} \
            {self._holdings['cash']} {self._holdings['commission']} {self._holdings['slippage']}"
        )

    def update_holdings_from_market(self, dt: datetime):
        self._historical_positions[dt] = self._positions.copy()
        self._historical_holdings[dt] = self._holdings.copy()

    def generate_historical_portfolio_df(self) -> pd.DataFrame:
        # TODO Align the lengths of the positions and holdings dataframes
        # + The positions frame is longer than the holdings b/c of the incomplete lookback periods
        # + at the start of analysis
        # // positions = pd.DataFrame.from_dict(self._historical_positions, orient='index')
        holdings = pd.DataFrame.from_dict(self._historical_holdings,
                                          orient='index')
        return holdings
