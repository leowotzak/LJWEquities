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


class PercentPortfolioValue(OrderSizer):

    def __init__(self, portfolio, percent: float):
        self.portfolio = portfolio
        self.percent = percent

    # ? Can this be decoupled from the portfolio?

    def size_order(self, price: float) -> int:
        return self.portfolio.get_percent_of_cash_holdings(self.percent) // price


class KelleyCriterion:

    def __init__(self):
        pass
