import logging
from typing import NoReturn, Sequence

from ljwtrader.broker.brokerage import Brokerage
from ljwtrader.events import Event, FillEvent, OrderEvent

logger = logging.getLogger(__name__)


class InteractiveBrokers(Brokerage):

    def __init__(self, queue: Sequence[Event]):
        self._queue = queue
        self.COMMISSION_PER_SHARE_FEE = .0075
        self.MIN_TRADE_VALUE = 1.0
        self.MAX_TRADE_VALUE = .01     # 1% of total trade value
        self.TXN_FEE = .0000051     # Transaction fees
        self.FINRA_PER_SHARE_FEE = .000119     # FINRA fees
        self.MAX_FINRA_FEE = 5.95

    def generate_fill_order(self, order_event: OrderEvent) -> NoReturn:

        # TODO make functions that generate all events/orders have consistent naming

        new_event = FillEvent(order_event.ticker,
                              order_event.datetime,
                              order_event.strategy_id,
                              order_event.direction,
                              order_event.price,
                              order_event.quantity,
                              commission=self.calculate_commission(order_event))
        new_event.slippage = self.calculate_slippage(order_event, new_event)
        self._queue.put(new_event)

    def calculate_slippage(
        # TODO: Shouldn't this be in portfolio? broker doesn't calc slippage does portfolio does

            self, order_event: OrderEvent,
            fill_event: FillEvent) -> float:     # * This is a static method

        order_value = order_event.quantity * order_event.price
        fill_value = fill_event.quantity * fill_event.price
        slippage = fill_value - order_value
        logger.info("Slippage: %f", slippage)
        return slippage

    def calculate_commission(self, order_event: OrderEvent) -> float:
        per_share_commission = order_event.quantity * self.COMMISSION_PER_SHARE_FEE
        trade_value = order_event.quantity * order_event.price

        broker_fees = min(max(self.MIN_TRADE_VALUE, per_share_commission),
                          self.MAX_TRADE_VALUE * trade_value)
        other_fees = self.TXN_FEE * trade_value + min(
            order_event.quantity * self.FINRA_PER_SHARE_FEE, self.MAX_FINRA_FEE)
        logger.info("Broker commission: %f, Other fees: %f", broker_fees,
                    other_fees)
        return broker_fees + other_fees
