from .event import EventBaseClass

class MarketEvent(EventBaseClass):
    """Created in response to price changes in underlying assets"""
    def __init__(self, time):
        super().__init__('MARKET', time)
