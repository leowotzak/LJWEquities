import datetime.datetime

from ljwtrader.strategy.indicator import Indicator, High
from ljwtrader.strategy.position import Position, HighPosition
from ljwtrader.strategy.strategy import Strategy
from ljwtrader.system import TradingSystem

import operator

pos1 = Position(Indicator(30), operator.gt, 5.0)

TradingSystem(pos1)


