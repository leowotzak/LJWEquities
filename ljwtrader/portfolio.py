import logging
from typing import NoReturn

from ljwtrader.events import Event, StrategyEvent, OrderEvent

logger = logging.getLogger(__name__)

class Portfolio:
    """
    Responsible for handling and implementing all portfolio logic for the trading system. 
    At a high level, the portfolio receives signals from all of the strategies that constitute
    it. The portfolio can then decide whether to follow through with these strategies, or it can 
    ignore them in favor of some other over-arching portfolio strategy. The portfolio should also 
    keep track of any rebalancing and issue orders to achieve certain targets.
    """
    def __init__(self, queue):
        self._queue = queue
        self._holdings = {'cash': 100000, 'commission': 0, 'fill_cost': 0}

        #? Is the status of each strategy (in or out...) decided here?

    def trigger_order(self, event: StrategyEvent) -> NoReturn:
        """Takes a signal event and applies portfolio logic

        Args:
            event (Event): SignalEvent containing information on trades to place

        Returns:
            NoReturn:
        """
        self.place_order(event)


    
    def place_order(self, event: StrategyEvent) -> NoReturn:
        """Generates an OrderEvent and places it on the queue

        Args:
            event (Event): Contains details regarding what to purchase #? and how much?

        Returns:
            NoReturn: 
        """
        new_event = OrderEvent(event.ticker, event.datetime, event.strategy_id, 1.0, 1)
        self._queue.put(new_event)


    def update_holdings_from_fill(self, event: Event) -> NoReturn:
        """Takes an FillEvent and updates the share/contract amounts & dollar amounts of the portfolio

        Args:
            event (Event): FillEvent containing all the details of the completed transaction

        Returns:
            NoReturn: 
        """

    def update_holdings_from_market(self, event: Event) -> NoReturn:
        """Updates the dollar amounts of the portfolio in response to a change in market prices

        Args:
            event (Event): MarketEvent pertaining to the updated asset

        Returns:
            NoReturn: 
        """

