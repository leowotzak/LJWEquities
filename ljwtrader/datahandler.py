import logging
from .sql import get_data_from_alphavantage

logger = logging.getLogger(__name__)

class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, queue_, start_date, end_date, frequency, vendor):
        self._queue = queue_
        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency
        self._vendor = vendor

        self.data = ( (index, row) for index, row in get_data_from_alphavantage('AAPL').iterrows() )


    def get_next_bar_from_data_handler(self):
        print(next(self.data))