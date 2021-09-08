import logging
from ljwtrader.broker.brokerage import Brokerage
from ljwtrader.events import Event, OrderEvent

logger = logging.getLogger(__name__)

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
        new_event = FillEvent(order_event.ticker, order_event.datetime, order_event.strategy_id, order_event.direction, order_event.price, order_event.quantity, commission=self.calculate_commission(order_event))
        new_event.slippage = self.calculate_slippage(order_event, new_event)
        self._queue.put(new_event)

    def calculate_slippage(self, order_event: OrderEvent, fill_event: FillEvent) -> float:
        order_value = order_event.quantity * order_event.price
        fill_value = fill_event.quantity * fill_event.price
        slippage = fill_value - order_value
        logger.info("Slippage: %f", slippage)
        return slippage

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
        logger.info("Broker commission: %f, Other fees: %f", broker_fees, other_fees)
        return broker_fees + other_fees
