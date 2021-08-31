import logging

logger = logging.getLogger(__name__)
class EventHandler:
    """Object that serves to route events to the proper system component based on their type"""

    def __init__(self, queue):
        self._queue = queue
    
    def _handle_market(self, event):
        pass

    def process_events(self):
        """Initiates and continues to execute backtest until there are no more bars in the datahandler"""
        EVENT_MAP = {
            'MARKET': self._handle_market
        }

        while not self._queue.empty():
            event = self._queue.get()
    
            try:
                handler = EVENT_MAP[event.type]
            except Exception as e:
                raise e
            else:
                handler(event)