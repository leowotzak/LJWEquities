
# LJWE: an algorithmic and quantitative analysis library

## What is it?

---

## How to install

---

Clone the repository or download the project and navigate to the project directory

For organizational purposes, it is recommended that one create a virtual environment to hold the project's dependencies by running the command:

### MacOS

```bash
python -m venv venv

source venv/bin/activate

python -m setup.py install
```

### Windows 
```bash
python -m venv venv

.\venv\Scripts\activate

python -m setup.py install
```

After setting up the environment, installing the library is as easy as running the `setup.py` file


After the installation is complete, all of the project's required dependencies should be installed!

## How to Use

---

The library functions as any typical python library. The primary trading system interface class is the `TradingSystem`, through which all other library functions flow. This can be done by running the following commands:

```python
from ljwtrader.system import TradingSystem

sys = TradingSystem()
```

To use the system, one can create a default backtest with the following:

```python
from ljwtrader.data import Backtest

bt = Backtest()
```

**LJWE** functions through indicators, which can be imported from the `strategy` module and initialized by supplying a ticker (to track, see below), number of days for the indicator, a comparison, and a value to compare to. When adding a position to the system, it is required that you supply a ticker to (act upon, see below) and a direction for the indicator, in this case, 'long'.

```python
from ljwtrader.strategy import XDayHigh

strategy = XDayHigh('AAPL', 10, operator.lt, 130.0)
sys.add_position(('AAPL', [strategy]), 'long')
```

The tickers supplied to the indicator and the tickers supplied to the position are not necessarily the same. The ticker supplied to the indicator is what is tracked and what triggers the indicator. What is supplied to the position which is actually transacted, which means, one can place trades on different assets than what is being tracked.

To run a backtest, all that needs to be done is to run the `TradingSystem.run_backtest()` method with the desired `Backtest` object, like below:

```python
results = sys.run_backtest(bt)
```

The `run_backtest()` method returns the results of the backtest as a dataframe

## Dependencies

---

* NumPy -- ([Link](https://numpy.org/))
* pandas -- ([Link](https://pandas.pydata.org/))
* SQLAlchemy -- ([Link](https://www.sqlalchemy.org/))
* Alembic -- ([Link](https://alembic.sqlalchemy.org/en/latest/))
* pyfolio -- ([Link](https://github.com/quantopian/pyfolio))
* alpha_vantage -- ([Link](https://github.com/RomelTorres/alpha_vantage))
  
## License

[MIT](https://github.com/leowotzak/LJWEquities/blob/8033a1e36a4138ef5d76099caa45bfa8fd70fdb2/LICENSE)
