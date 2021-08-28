import logging

logger = logging.getLogger(__name__)

class DataHandler:
    """Object that handles all data access for other system components"""
    def __init__(self, queue_, start_date, end_date, frequency, vendor):
        self._queue = queue_
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.vendor = vendor
