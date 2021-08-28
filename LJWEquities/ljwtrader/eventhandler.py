import logging

logger = logging.getLogger(__name__)

class EventHandler:
    """Object that serves to route events to the proper system component based on their type"""

    def __init__(self, queue, data_handler):
        self._queue = queue
        self._data_handler = data_handler
    
    def _handle_market(self, event):
        pass

    def run_backtest(self):
        """Initiates and continues to execute backtest until there are no more bars in the datahandler"""
        EVENT_MAP = {
            'MARKET': _handle_market
        }

        self._data_handler.get_next_bar_from_data_handler()

        while not self._queue.empty():
            event = self._queue.get()
    
            try:
                handler = EVENT_MAP[event.type]
            except Exception as e:
                raise e
            else:
                handler()