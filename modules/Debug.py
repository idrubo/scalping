'''
To debug.
'''

import pandas as pd
import vectorbt as vbt

from modules.Portfolio import *
from modules.Graph     import *
from modules.Utils     import *
from modules.Dates     import *

# To activate/deactivate debug features.
btTest = True
rtTest = True

# Module data.
dbgPF    = None     # For the portfolio.
dbgOHLCV = None     # For ohlcv data.
dbgInd   = {}       # For indicator data.
dbgPivot = {}       # For Pivot Points.
dbgLast  = {}       # For Pivot Points ohlcv data.

# Nicely printing data.
def prnMsg (msg):
    print (Style.BRIGHT, end =""); print (msg, end ="")
    print (Style.RESET_ALL)

def prnError (msg):
    print (Style.BRIGHT + Fore.RED, end =""); print (msg, end ="")
    print (Style.RESET_ALL)

def prnSuccess (msg):
    print (Style.BRIGHT + Fore.GREEN, end =""); print (msg, end ="")
    print (Style.RESET_ALL)

def prnVar (name, fmt, value):
    prnVal (Fore.GREEN, name, fmt, value)

def prnDbg (name, fmt, value):
    prnVal (Style.BRIGHT + Fore.RED, name, fmt, value)

# Store the portfolio after a backtest.
def dbgSetPF (pf):

    global dbgPF

    dbgPF = pf

# Store backtest ohlcv data.
def dbgSetOHLCV (ohlcv):

    global dbgOHLCV

    dbgOHLCV = ohlcv

# Store indicators.
def dbgSetInd (name, ind):
    dbgInd [name] = ind

# Store ohlcv data used to compute pivot points.
def dbgSetLast (ohlcv):
    dbgLast ['ohlcv'] = ohlcv

# Store pivot points.
def dbgSetPivot (S, R):
    dbgPivot ['S'] = S
    dbgPivot ['R'] = R

# Check, prepare and plot data.
# We can just plot a single symbol.
# If a symbol is passed, it is plottted, if it is not, the most frequently
# traded symbol is chosen.
def dbgPlot (sym):

    global dbgPF, dbgOHLCV, dbgInd, dbgPivot

    # We get the most frequent traded symbol, if 'None' is passed.
    dbgTrades = getTrades (dbgPF)

    if dbgTrades.empty:
        prnError ('No trades to plot !!!')
        return

    if sym is None:
        symbol = dbgTrades ['Column'].mode ()[0]
    else:
        symbol = sym

    # To check pivot point values.
    if len (dbgLast):
        dbgLast ['ohlcv']['Open']  = dbgLast ['ohlcv']['Open'][symbol]
        dbgLast ['ohlcv']['High']  = dbgLast ['ohlcv']['High'][symbol]
        dbgLast ['ohlcv']['Low']   = dbgLast ['ohlcv']['Low'][symbol]
        dbgLast ['ohlcv']['Close'] = dbgLast ['ohlcv']['Close'][symbol]

    # Candlestick chart for a single period, useful to check pivot points.
    graphOHLCV (dbgLast)

    # To check an strategy.

    # For Close data.

    # The first two days are only needed to initialize indicator values.
    start = dbgOHLCV ['Open'][symbol].index [0]
    end   = dbgOHLCV ['Open'][symbol].index [-1]

    # We assume 'dbgOHLCV' spans for 'dtLag' business days.
    actual = start + getDtLag ()

    if dbgOHLCV is not None:
        dbgCS = {'symbol': symbol,
                 'x': dbgOHLCV ['Open' ][symbol][actual:end].index,
                 'O': dbgOHLCV ['Open' ][symbol][actual:end],
                 'H': dbgOHLCV ['High' ][symbol][actual:end],
                 'L': dbgOHLCV ['Low'  ][symbol][actual:end],
                 'C': dbgOHLCV ['Close'][symbol][actual:end]}

    # For Entry and Exit points.

    dbgTrades = dbgTrades [dbgTrades ['Column'] == symbol]

    dbgOrders = [{'x': dbgTrades ['Entry Timestamp'], 'y': dbgTrades ['Avg Entry Price'], 'name': 'Entry'},
                 {'x': dbgTrades ['Exit Timestamp'],  'y': dbgTrades ['Avg Exit Price'],  'name': 'Exit'}]

    # For Support and Resistance.

    dbgSR = None

    if len (dbgPivot):
        dbgSR = pd.DataFrame ({
            'S': dbgPivot ['S'][symbol],
            'R': dbgPivot ['R'][symbol]}, index = dbgCS ['x'])

    # For indicators.

    dbgSymInd = {}
    for ind in dbgInd.keys ():
        dbgSymInd [ind] = {}
        for name in dbgInd [ind].keys ():

            # The first day is only needed to initialize indicator values.
            start = dbgInd [ind][name][symbol].index [0]
            end   = dbgInd [ind][name][symbol].index [-1]

            # We assume 'dbgInd' spans for 'dtLag' business days.
            actual = start + getDtLag ()

            dbgSymInd [ind][name] = dbgInd [ind][name][symbol][actual:end]

    # Plot the strategy.
    graphStrategy (dbgCS, dbgOrders, dbgSymInd, dbgSR)

