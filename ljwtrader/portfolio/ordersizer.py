from abc import ABC, abstractmethod

class OrderSizer(ABC):

    @abstractmethod
    def size_order(self):
        raise NotImplementedError

class FixedDollarValue(OrderSizer):

    def __init__(self, portfolio, amount: float):
        self.portfolio = portfolio
        self.amount = amount

    def size_order(self, price: float) -> int:
        return self.amount // price



class PercentPortfolioValue:

    def __init__(self):
        pass


class KelleyCriterion:

    def __init__(self):
        pass
