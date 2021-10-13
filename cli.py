import operator

import pyfolio as pf

from ljwtrader.strategy import XDayHigh
from ljwtrader.system import TradingSystem
from ljwtrader.data import Backtest

if __name__ == '__main__':
    strat = XDayHigh('AAPL', 10, operator.lt, 130.0)
    back = Backtest()
    sys = TradingSystem()
    back.add_position_to_backtest(pos1, pos2, pos3, pos4)
    res = sys.run_backtest(back)


