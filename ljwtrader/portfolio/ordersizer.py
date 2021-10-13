from abc import ABC, abstractmethod

class OrderSizer(ABC):

    @abstractmethod
    def size_order(self):
        raise NotImplementedError

    def __init__(self):
        pass


class PercentPortfolioValue:

    def __init__(self):
        pass


class KelleyCriterion:

    def __init__(self):
        pass
