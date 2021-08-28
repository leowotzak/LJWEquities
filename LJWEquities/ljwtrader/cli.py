import argparse
import datetime

# * File that acts as input so that I dont have to edit the base files anymore

parser = argparse.ArgumentParser(description="LJWE quantitative trading system")


# * First day of analysis
parser.add_argument(
    'start',
    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
    nargs=1,
    ),

# * Last day of analysis
parser.add_argument(
    'end',
    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
    nargs=1,
    ),

# * Frequency of the data (i.e. 5min 5day etc...)
parser.add_argument(
    'frequency',
    type=str,
    nargs=1,
    choices=['1min', '5min', '15min', '30min', '60min']
    ),

# * Vendor of data 
# ? Is this necessary
# ? Or should be be determined later?
parser.add_argument(
    'vendor',
    type=str,
    nargs=1,
    choices=['av']
    )

