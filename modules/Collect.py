'''
To fetch, save and recover time series.
'''

import os

import vectorbt as vbt

import modules.Providers

from modules.AData      import *
from modules.Dates      import *
from modules.Utils      import *
from modules.Debug      import *

# Depending on our operating system we may adapt the path.
DataDir = './data/'
TrendFile = 'trend.data'
dataPath = DataDir + TrendFile

vbtOhlcv = None

def getDataDir (): return DataDir

# Download and save the data to "trend.data".
def saveTrend (symbols, start, end, timeFrame):

    # ADX may need up to 45 periods to fill lagging data.
    first, l = targetPeriod (start, timeFrame, 45)
    f, last = targetPeriod (end, timeFrame, 45)

    ohlcv = modules.Providers.Download (symbols, timeFrame, first, last)

    createDir (DataDir)

    ohlcv.save (dataPath)

    return ohlcv

# Load the data from "trend.data" or create it, if it is not present.
def loadTrend (symbols, start, end, timeFrame):

    if not os.path.exists (dataPath):
        return saveTrend (symbols, start, end, timeFrame)

    return modules.Providers.Load (dataPath)

# General funtion to download 'ohlcv' data.
# Note that the module 'Providers.py' contents data provider specific code.
# And so, 'Collect.py' is, in effect, an abstraction for downloading data.
def collect (symbols, interval, start, end):

    global vbtOhlcv

    vbtOhlcv = modules.Providers.Download (symbols, interval, start, end)

    ohlcv = {}
    ohlcv ['Open']  = vbtOhlcv.get ('Open')
    ohlcv ['High']  = vbtOhlcv.get ('High')
    ohlcv ['Low']   = vbtOhlcv.get ('Low')
    ohlcv ['Close'] = vbtOhlcv.get ('Close')

    try:
        ohlcv ['Open' ].index = ohlcv ['Open' ].index.tz_convert (marketTZ)
        ohlcv ['High' ].index = ohlcv ['High' ].index.tz_convert (marketTZ)
        ohlcv ['Low'  ].index = ohlcv ['Low'  ].index.tz_convert (marketTZ)
        ohlcv ['Close'].index = ohlcv ['Close'].index.tz_convert (marketTZ)
    except TypeError:
        print ("ERROR: dailyData: Can't convert data frame index timezone.")
        exit ()

    return ohlcv

# General funtion to update 'ohlcv' data.
# Note that the module 'Providers.py' contents data provider specific code.
# It updates a vectorBT 'ohlcv' data structrure from its own last index to 'end'.
def rtUpdate (end):

    global vbtOhlcv

    modules.Providers.Update (end)

    ohlcv = {}
    ohlcv ['Close'] = vbtOhlcv.get ('Close')

    try:
        ohlcv ['Close'].index = ohlcv ['Close'].index.tz_convert (marketTZ)
    except TypeError:
        print ("ERROR: dailyData: Can't convert data frame index timezone.")
        exit ()
    
    return ohlcv ['Close']

