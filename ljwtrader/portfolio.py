import logging
from typing import NoReturn

from ljwtrader.events import Event

logger = logging.getLogger(__name__)

class Portfolio:
    """
    Responsible for handling and implementing all portfolio logic for the trading system. 
    At a high level, the portfolio receives signals from all of the strategies that constitute
    it. The portfolio can then decide whether to follow through with these strategies, or it can 
    ignore them in favor of some other over-arching portfolio strategy. The portfolio should also 
    keep track of any rebalancing and issue orders to achieve certain targets.
    """
    def place_order(self, event: Event) -> NoReturn:
        """Generates an OrderEvent and places it on the queue

        Args:
            event (Event): Contains details regarding what to purchase #? and how much?

        Returns:
            NoReturn: 
        """

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

