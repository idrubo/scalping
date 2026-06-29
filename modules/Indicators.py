'''
To compute indicators.
'''

from enum import Enum

import pandas as pd
import talib
import vectorbt as vbt

from modules.Dates      import *
from modules.Collect    import *
from modules.Utils      import *
from modules.Results    import *

# To debug.
from modules.Debug      import *

Trend = Enum ('Trend', [('uptrend', 1), ('downtrend', 2), ('sideways', 3), ('reversal', 4)])

SRdate = None
Support = {}
Resistance = {}

#
# To download ohlcv data to compute the pivot points for the last business
# day.
# 
def lastSR (symbols, start):

    global SRdate

    # If we have the pivot points already computed, return them.
    if Support:
        if SRdate == last:
            S = pd.Series (Support)
            R = pd.Series (Resistance)
            return S, R

    end = start + timedelta (days = 1)

    # We choose '1d' as the pivot time frame, for now.
    ohlcvLast = collect (symbols, '1d', start, end)

    # Only plot the chart if we are on testing.
    if btTest: dbgSetLast (ohlcvLast)

    SRdate = start

    return SR (ohlcvLast, start)

#
# To compute pivot points for a single period with its 'ohlcv' data.
#
# Pivot points are computed as:
#
#      High + Low + Close
# P = --------------------
#              3
#
# R1 = (P × 2) − Low
# R2 = P + (High − Low)
#
# S1 = (P × 2) − High
# S2 = P − (High − Low)
#
# where:
# P = Pivot point
# R1 = Resistance 1, R2 = Resistance 2
# S1 = Support 1, S2 = Support 2
#
# We will take S2, R2 as support and resistance levels.
#
def SR (ohlcvLast, start):

    Support = {}
    Resistance = {}

    for symbol in ohlcvLast ['High']:

        H = ohlcvLast ['High' ].loc [start, symbol]
        L = ohlcvLast ['Low'  ].loc [start, symbol]
        C = ohlcvLast ['Close'].loc [start, symbol]

        P  = (H + L + C) / 3

        R1 = (P * 2) - L
        R2 = P + (H - L)

        S1 = (P * 2) - H
        S2 = P - (H - L)

        Support    [symbol] = S2
        Resistance [symbol] = R2

    S = pd.Series (Support)
    R = pd.Series (Resistance)

    # Only plot the chart if we are on testing.
    if btTest: dbgSetPivot (S, R)

    return S, R

# We return a list of symbols moving uptrending or sideways, from an input symbol list.
def trendList (ohlcv, symbols, target, timeFrame):

    start, end = targetPeriod (target, timeFrame, 45)

    ohlcv = ohlcv.get (['High', 'Low', 'Close'])

    for point in ohlcv:
        try:
            point.index = point.index.tz_convert (marketTZ)
        except TypeError:
            print ("ERROR: signals: Can't convert data frame index timezone.")
            exit ()

    ohlcv0 = ohlcv [0].loc [start:end]
    ohlcv1 = ohlcv [1].loc [start:end]
    ohlcv2 = ohlcv [2].loc [start:end]

    uptrend = []
    sideways = []

    for sym in symbols:
        trend = checkTrend (ohlcv0 [sym], ohlcv1 [sym], ohlcv2 [sym])
        if trend == Trend.uptrend: uptrend.append (sym)
        if trend == Trend.sideways: sideways.append (sym)

    return uptrend, sideways

# To check the number of records with a NaN value, before any output is generated.
def nNaNs (i):
    NaNs = i.isna ().sum ()
    print ('NaNs: ', NaNs)
    print ('i.iloc [0]: ', i.iloc [0])
    print ('i.iloc [NaNs - 1]: ', i.iloc [NaNs - 1])
    print ('i.iloc [NaNs]: ', i.iloc [NaNs])

# Return:
# "uptrend"   if ADX is bigger than 25 and +DI is greater than -DI.
# "downtrend" if ADX is bigger than 25 and +DI is smaller than -DI.
# "sideways"  if ADX is smaller than 20.
# "reversal"  if ADX is smaller than 20.
# The library seems to need more than 29 periods for ADX, 15 periods for +DI
# and 15 periods for -DI.
def checkTrend (High, Low, Close):

    period = 15

    adx      = talib.ADX      (High, Low, Close, timeperiod = period)
    plus_di  = talib.PLUS_DI  (High, Low, Close, timeperiod = period)
    minus_di = talib.MINUS_DI (High, Low, Close, timeperiod = period)

    lastADX = adx.iloc [-1]
    lastPDI = plus_di.iloc [-1]
    lastMDI = minus_di.iloc [-1]

    # To account for the number of periods without data.
    # nNaNs (adx)
    # nNaNs (plus_di)
    # nNaNs (minus_di)

    if (lastADX > 25) and (lastPDI > lastMDI):
        return Trend.uptrend

    if (lastADX) > 25 and (lastPDI < lastMDI):
        return Trend.downtrend

    if lastADX < 20:
        return Trend.sideways

    if (lastADX >= 20) and (lastADX <= 25):
        return Trend.reversal

    if lastPDI == lastMDI:
        return Trend.reversal

# Chaikin A/D Oscillator.
def ADOSCfilters (high, low, close, volume):

    values = talib.ADOSC (high, low, close, volume, fastperiod=3, slowperiod=10)

    entryFilter = values > 0
    exitFilter = values <= 0

    return entryFilter, exitFilter

# Bollinger Bands.
def BBfilters (point):

    values = vbt.BBANDS.run (point)

    # Only plot the chart if we are on testing.
    if btTest: dbgSetInd ('Bollinger Bands', {'Upper': values.upper, 'Lower': values.lower})

    entryFilter = values.lower_above (point)
    exitFilter = values.upper_below (point)

    return entryFilter, exitFilter

# Relative Strength Index.
def RSIfilters (point, upper, lower):

    values = vbt.RSI.run (point)

    # Only plot the chart if we are on testing.
    if btTest: dbgSetInd ('RSI', {'RSI': values.rsi})

    # Standard values.
    entryFilter = values.rsi_crossed_above (lower)
    exitFilter  = values.rsi_crossed_below (upper)

    return entryFilter, exitFilter

# Simple Moving Averages.
def SMAfilters (point, sPeriod, fPeriod):

    slow_ma = vbt.MA.run (point, sPeriod, short_name='slow')
    fast_ma = vbt.MA.run (point, fPeriod, short_name='fast')

    # Only plot the chart if we are on testing.
    if btTest: dbgSetInd ('SMA', {'Slow': slow_ma, 'Fast': fast_ma})
    
    entryFilter = fast_ma.ma_crossed_above (slow_ma)
    exitFilter  = fast_ma.ma_crossed_below (slow_ma)

    return entryFilter, exitFilter

# Moving Average Convergence Divergence.
def MACDfilters (point, slowPeriod, fastPeriod, sgnPeriod):

    MACD = vbt.MACD.run (
            point,
            fast_window = fastPeriod,
            slow_window = slowPeriod,
            signal_window = sgnPeriod,
            hide_params = ['fast_window', 'slow_window', 'signal_window'])

    # Only plot the chart if we are on testing.
    if btTest: dbgSetInd ('MACD', {'Histogram': MACD.hist})

    entryFilter = MACD.macd_above (MACD.signal)
    exitFilter  = MACD.macd_below (MACD.signal)

    entryFilter.columns = entryFilter.columns.to_flat_index ()

    return entryFilter, exitFilter

# Stochastic Oscilator.
def SOfilters (High, Low, Close, lower, upper):

    values = vbt.STOCH.run (High, Low, Close)

    # Only plot the chart if we are on testing.
    if btTest: dbgSetInd ('Stochastic Oscillator', {'Percent D': values.percent_d})

    # Standard values.
    entryFilter = values.percent_d_crossed_above (lower)
    exitFilter = values.percent_d_crossed_below (upper)

    return entryFilter, exitFilter

# We need to get support and resistance levels from the past day.
def PivotFilters (High, Low, Close):

    # We may need additional data for the pivot points.
    # We need to extract the symbols and the target date from the proper data.
    Symbols = Close.columns.tolist ()

    l = lastBusiness (Close.index [-1])
    last = lastBusiness (Close.index [-1] - timedelta (hours = l.hour, minutes = l.minute))

    S, R = lastSR (Symbols, last)

    entryFilter = Close.apply (lambda Close: Close < S, axis = 1)
    exitFilter  = Close.apply (lambda Close: Close > R, axis = 1)

    return entryFilter, exitFilter

