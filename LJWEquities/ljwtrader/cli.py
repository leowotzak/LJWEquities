import argparse

# * File that acts as input so that I dont have to edit the base files anymore

parser = argparse.ArgumentParser(description="LJWE quantitative trading system")


# * First day of analysis
parser.add_argument('start'),

# * Last day of analysis
parser.add_argument('end'),

# * Frequency of the data (i.e. 5min 5day etc...)
parser.add_argument('frequency'),

# * Vendor of data 
# ? Is this necessary
# ? Or should be be determined later?
parser.add_argument('vendor')

# * Action to perform, starts backtest
parser.add_argument('--backtest')

