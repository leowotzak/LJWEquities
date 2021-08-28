from queue import Queue

import logging
logger = logging.getLogger(__name__)


class TradingSystem:
    """
    Trading system that serves to govern the entire trading logic process which it does by reading the event loop,
    pushing data from the data handler, and calculating trading signals.
    """
