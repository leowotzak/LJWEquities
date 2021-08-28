import logging

logger = logging.getLogger(__name__)

class EventHandler:
    """Object that serves to route events to the proper system component based on their type"""

    def __init__(self, queue, data_handler):
        self._queue = queue
        self._data_handler = data_handler
    
    def _handle_market(self, event):
        pass

    EVENT_MAP = {
        'MARKET': _handle_market
    }