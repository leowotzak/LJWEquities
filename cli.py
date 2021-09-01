import argparse
import datetime
import operator

from ljwtrader.strategy.indicator import XDayHigh
from ljwtrader.strategy.strategy import Strategy
from ljwtrader.system import TradingSystem

parser = argparse.ArgumentParser(
    description="LJWE quantitative trading system",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# parser.add_argument('symbols',
#                     type=str,
#                     nargs='+',
#                     help='Symbols for system to analyze')

parser.add_argument('-l',
                    '--lookup',
                    nargs='?',
                    const=print,
                    help='Display summary statistics')

parser.add_argument('-s',
                    '--start',
                    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                    nargs='?',
                    default='2021-01-01',
                    help='First day of analysis'),

parser.add_argument('-e',
                    '--end',
                    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                    nargs='?',
                    default='2020-01-01',
                    help='Last day of analysis'),

parser.add_argument(
    '-f',
    '--frequency',
    type=str,
    nargs='?',
    choices=['1min', '5min', '15min', '30min', '60min', '1d', '1w', '1m'],
    default='1d',
    help='Frequency of the data'),

parser.add_argument('-v',
                    '--vendor',
                    type=str,
                    nargs='?',
                    choices=['av'],
                    default='av',
                    help='Data vendor')

parser.add_argument('-b',
                    '--backtest',
                    nargs='?',
                    const=True,
                    default=False,
                    help='Initiate a backtest')

if __name__ == '__main__':
    args = parser.parse_args()
    sys = TradingSystem(['AAPL'], args.start, args.end, args.frequency, args.vendor)
    sys.run_backtest()
