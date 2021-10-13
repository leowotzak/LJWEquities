import logging
from datetime import datetime
from queue import Queue
from typing import NoReturn

from ljwtrader.data import DataHandler
from ljwtrader.events import Event, FillEvent, OrderEvent, StrategyEvent

logger = logging.getLogger(__name__)


class Portfolio:
    """
    Responsible for handling and implementing all portfolio logic for the trading system. 

    At a high level, the portfolio receives signals from all of the strategies that constitute
    it. The portfolio can then decide whether to follow through with these strategies, or it can 
    ignore them in favor of some other over-arching portfolio strategy. The portfolio should also 
    keep track of any rebalancing and issue orders to achieve certain targets.
    """

    def __init__(self, queue: Queue, data_handler: DataHandler):
        """
        Arguments:
            queue {Queue} -- System queue to place events on
            data_handler {DataHandler} -- System data handler to source data from
        """

        # TODO: Properly document using sphinx

        self._queue = queue
        self.data_handler = data_handler
        self._positions = {}
        self._holdings = {'cash': 100000, 'commission': 0, 'slippage': 0}
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

    def update_holdings_after_bar(self, dt: datetime):
        """Updates the dollar amounts of the portfolio in response to a change in market prices"""
        self._historical_positions[dt] = self._positions.copy()
        self._historical_holdings[dt] = self._holdings.copy()

    def generate_historical_portfolio_df(self) -> pd.DataFrame:
        """
        Produces a dataframe containing the historical portfolio values

        Called at the end of a backtest or live trading session so that 
        results can be summarized and visualized

        :return: Historical quantities, holdings, cash, commission, and slippage 
        for the trading session duration
        :rtype: pd.DataFrame
        """
        # TODO Align the lengths of the positions and holdings dataframes
        # + The positions frame is longer than the holdings b/c of the incomplete lookback periods
        # + at the start of analysis
        # // positions = pd.DataFrame.from_dict(self._historical_positions, orient='index')
        holdings = pd.DataFrame.from_dict(self._historical_holdings,
                                          orient='index')
        return holdings
