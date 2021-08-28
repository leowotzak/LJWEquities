class EventBaseClass:
    """
    Event is base class providing an interface for all subsequent (inherited) events, that will trigger further
    events in the trading infrastructure.
    """
    def __init__(self, event_type, datetime, symbol):
        self.event_type = event_type
        self.datetime = datetime

    def __str__(self):
        return f'{self.event_type} -- {self.datetime}'

    def __repr__(self):
        repr = ' -- '.join([
            f'{key}: {value}' for key, value in self.__dict__.items()
        ])