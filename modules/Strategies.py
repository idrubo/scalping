'''
To apply strategies to market data.
'''

from modules.Dates      import *
from modules.Indicators import *

# Symbolic constants for strategies
ST_MOMENTUM = 0
ST_RANGING  = 1

# Define timeframes.
trendTF  =  '1h'
signalTF = '15m'

#
# Strategy - Momentum Scalping
#
# Trending Markets - Bullish - Long positions.
#
# Time Frame - 15m
# 
# RSI  -> Momentum
# MACD -> Momentum
# 
# Signal Type   MACD Condition          RSI Condition
# Buy           MACD above signal line  RSI crosses above 40
# Sell          MACD below signal line  RSI crosses below 60
#
def stMomentum (price):
    
    # Compute indicator values and filters.
    # Our strategy is based on MACD and RSI.

    # On MACD.
    entryFilterMACD, exitFilterMACD = MACDfilters (price, 26, 12, 9)

    # On RSI.
    entryFilterRSI, exitFilterRSI = RSIfilters (price, 60, 40)

    # Generate signals.

    # The first day is only needed to initialize indicator values.
    start = price.index [0]
    end   = price.index [-1]

    # We assume 'price' spans for 'dtLag' business days.
    actual = start + getDtLag ()

    # Close all positions at the end of the day.
    lastRow = price.index [-1]
    lastPer = lastPeriod (signalTF)

    if lastPer == lastRow.strftime ('%H:%M'):
        entryFilterRSI [lastRow : ] = False
        exitFilterRSI  [lastRow : ] = True

    entrySgn = entryFilterMACD [actual:end] & entryFilterRSI [actual:end]
    exitSgn  = exitFilterMACD  [actual:end] | exitFilterRSI  [actual:end]

    return entrySgn, exitSgn

#
# Strategy - Ranging with Pivot points and Stochastic Oscillator.
#
# Ranging Markets - Long positions.
#
# Time Frame - 15m
# 
# Pivot points          -> Support / Resistance
# Stochastic Oscillator -> Momentum
# 
# Signal Type   Pivot point Condition   Stoch. Osc. Condition
# Buy           Price near support      SO crosses above 20
# Sell          Price near resistance   SO crosses below 80
#
def stRanging (high, low, close):

    # Compute indicator values and filters.
    # Our strategy is based on the Stochastic Oscillator and pivot points.

    # On Stochastic Oscillator.
    entryFilterSO, exitFilterSO = SOfilters (high, low, close, 20, 80)

    # On pivot points.
    entryFilterPivot, exitFilterPivot = PivotFilters (high, low, close)

    # Generate signals.

    # The first day is only needed to initialize indicator values.
    start = close.index [0]
    end   = close.index [-1]

    # We assume 'close' spans for 'dtLag' business days.
    actual = start + getDtLag ()

    # Close all positions at the end of the day.
    lastRow = close.index [-1]
    lastPer = lastPeriod (signalTF)
    if lastPer == lastRow.strftime ('%H:%M'):
        entryFilterSO   [lastRow : ] = False
        exitFilterSO    [lastRow : ] = True

    entrySgn = entryFilterSO [actual:end] & entryFilterPivot [actual:end]
    exitSgn  = exitFilterSO  [actual:end] | exitFilterPivot  [actual:end]

    return entrySgn, exitSgn

def signals (strategy, high, low, close):

    match strategy:
        case 0: # ST_MOMENTUM
            entrySgn, exitSgn = stMomentum (close)
        case 1: # ST_RANGING
            entrySgn, exitSgn = stRanging (high, low, close)
        case _:
            print ("ERROR: signals: Not a valid strategy.")
            exit (-1)

    return entrySgn, exitSgn

