from enum import Enum

class DataVendor(Enum):
    AV = 1
    IB = 2
    SQL = 3

class BarFrequency(Enum):
    M_1 = 1
    M_5 = 2
    M_15 = 3
    M_30 = 4
    M_60 = 5
    D = 6
    W = 7
    M = 8
