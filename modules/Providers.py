'''
To fetch time series from different providers.
'''

import vectorbt as vbt

import modules.Collect

from modules.Dates  import *
from modules.AData  import *
from modules.Debug  import *

# We can save any data provider credentials here.
from modules.Credentials import *

# Callables to general, abstract fucntions.
Download = None
Update   = None
Load     = None

# We must call it to select a data provider, before we start downloading data.
def setProvider (pr):

    global Download, Update, Load

    match pr:
        case 'YF':
            Download = YFfetch 
            Update   = YFUpdate
            Load     = YFLoad 

            prnMsg ('Using Yahoo Finance as data provider.')

        case 'Alpaca':

            vbt.settings.data ['alpaca']['api_key'] = ALPACA_API_KEY
            vbt.settings.data ['alpaca']['secret_key'] = ALPACA_SECRET_KEY 

            Download = AlpFetch
            Update   = AlpUpdate
            Load     = AlpLoad

            prnMsg ('Using Alpaca as data provider.')

        case _:
            print ("ERROR: setDownload: Not a valid provider.")
            exit (-1)

#
# Yahoo finance doesn't return the 'end' parameter nor it returns premarket data.
# 
def YFfetch (symbols, timeFrame, first, last):

    prnMsg ('Downloading ...')

    Success = False; i = 0

    while ((not Success) and (i < 5)):
    
        try:
            vbtOhlcv = vbt.YFData.download (symbols, interval = timeFrame, start = first, end = last)
        except:
            prnError ('Error dowloading data.')
            if i < 4: prnError ('Retrying ...')
        else:
            Success = True
            prnSuccess ('SUCESS !!!')
    
        i += 1

        return vbtOhlcv

# Just to drop unneeded data.
def prDrop (ohlcv, first, last):

    for df in ohlcv:
        low  = first + getSEopenDelta ()
        high = nextBusiness (first)

        while (low.date () < last.date ()):
            df.drop (df [(df.index > low) & (df.index < high)].index, inplace = True)
            low  = nextBusiness (low)
            high = nextBusiness (high)

    return ohlcv

#
# Alpaca returns the 'end' parameter and premarket data.
# 
def AlpFetch (symbols, timeFrame, first, last):

    prnMsg ('Downloading ...')


    Success = False; i = 0
    while ((not Success) and (i < 5)):

        try:
            vbtOhlcv = AData.download (symbols, timeframe = timeFrame, start = first, end = last)
        except:
            prnError ('Error dowloading data.')
            if i < 4: prnError ('Retrying ...')
        else:
            prnSuccess ('SUCESS !!!')
            Success = True

        i += 1

    # Just to drop unneeded data.
    ohlcv = prDrop (vbtOhlcv.get (), first, last)

    prnSuccess ('SUCESS !!!')

    return vbtOhlcv

def YFLoad (dataPath):
    return vbt.YFData.load (dataPath)

def AlpLoad (dataPath):
    return vbt.AlpacaData.load (dataPath)

# Updates yahoo 'ohlcv' data from the last index to 'end'.
def YFUpdate (end):

    prnMsg ('Downloading ...')

    tf = modules.Collect.vbtOhlcv.download_kwargs ['interval']
    d, h, m = tDelta (tf)
    end = end + timedelta (minutes = 60 * h + m)

    Success = False; i = 0
    while ((not Success) and (i < 5)):

        try:
            modules.Collect.vbtOhlcv = modules.Collect.vbtOhlcv.update (end = end)
        except:
            prnError ('Error dowloading data.')
            if i < 4: prnError ('Retrying ...')
        else:
            prnSuccess ('SUCESS !!!')
            Success = True

        i += 1

# Updates alpaca 'ohlcv' data from the last index to 'end'.
def AlpUpdate (end):

    prnMsg ('Downloading ...')

    Success = False; i = 0
    while ((not Success) and (i < 5)):

        try:
            modules.Collect.vbtOhlcv = modules.Collect.vbtOhlcv.update (end = end)
        except:
            prnError ('Error dowloading data.')
            if i < 4: prnError ('Retrying ...')
        else:
            prnSuccess ('SUCESS !!!')
            Success = True

        i += 1

    ohlcv = modules.Collect.vbtOhlcv.get ()

    first = ohlcv [0].index [0]
    last  = ohlcv [0].index [-1]

    # Just to drop unneeded data.
    prDrop (ohlcv, first, end)

