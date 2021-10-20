import operator

import pyfolio as pf

from ljwtrader.strategy import ZScore
from ljwtrader.strategy import Position
from ljwtrader.system import TradingSystem
from ljwtrader.data import Backtest

if __name__ == '__main__':

    indicator1 = ZScore('AAPL', 'A', N_short=5, N_long=60, operator=operator.gt, value=1.0)
    indicator2 = ZScore('AAPL', 'A', N_short=5, N_long=60, operator=operator.lt, value=-1.0)
    
    sys = TradingSystem()


    pos1 = Position('AAPL', indicator1, 'LONG')
    pos2 = Position('A', indicator1, 'SHORT')
    pos3 = Position('AAPL', indicator2, 'SHORT')
    pos4 = Position('A', indicator2, 'LONG')
    back = Backtest(pos1, pos2, pos3, pos4)

    sys.run(back)
    res = sys._portfolio.generate_historical_portfolio_df()
    pf.create_returns_tear_sheet(res)

