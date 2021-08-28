import logging

logger = logging.getLogger(__name__)

class EventHandler:
    """Object that serves to route events to the proper system component based on their type"""

    def __init__(self, queue):
        self._queue = queue
    
    def _handle_market(event):
        pass
    
    EVENT_MAP = {
        'MARKET': _handle_market
    }