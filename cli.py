import operator

import pyfolio as pf

from ljwtrader.strategy import XDayHigh
from ljwtrader.system import TradingSystem
from ljwtrader.data import Backtest

if __name__ == '__main__':
    strat = XDayHigh('AAPL', 10, operator.lt, 130.0)
    back = Backtest()
    sys = TradingSystem()
    sys.add_position(('AAPL', [strat]), 'long')
    sys.run_backtest(back)
