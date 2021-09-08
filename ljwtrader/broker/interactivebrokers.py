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
