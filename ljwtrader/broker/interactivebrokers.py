from ljwtrader.broker.brokerage import Brokerage
from ljwtrader.events import Event, OrderEvent

from typing import Sequence, NoReturn


class InteractiveBrokers(Brokerage):
    def __init__(self, queue: Sequence[Event]):
        self._queue = queue
        self.COMMISSION_PER_SHARE_FEE = .0075
        self.MIN_TRADE_VALUE = 1.0
        self.MAX_TRADE_VALUE = .01  # 1% of total trade value
        self.TXN_FEE = .0000051 # Transaction fees
        self.FINRA_PER_SHARE_FEE = .000119 # FINRA fees
        self.MAX_FINRA_FEE = 5.95

    def generate_fill_order(self, order_event: OrderEvent) -> NoReturn:
        pass

    def calculate_slippage(self, order_event: OrderEvent, fill_event) -> float:
        pass

    def calculate_commission(self, order_event: OrderEvent) -> float:
        """Calculates the commission for the order using the Interactive Brokers commission structure as a reference

        Args:
            order_event (OrderEvent): Event to calculate commission for

        Returns:
            float: Total commissions and fees for the given order
        """
        per_share_commission = order_event.quantity * self.COMMISSION_PER_SHARE_FEE
        trade_value = order_event.quantity * order_event.price

        broker_fees = min(max(self.MIN_TRADE_VALUE, per_share_commission), self.MAX_TRADE_VALUE * trade_value)
        other_fees = self.TXN_FEE * trade_value + min(order_event.quantity * self.FINRA_PER_SHARE_FEE, MAX_FINRA_FEE)
        return broker_fees + other_fees