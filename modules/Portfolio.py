'''
 To run a portfolio and make some related computations.
'''

import vectorbt as vbt

from modules.Utils      import *

# Total PnL across different portfolios.
TotalPnL = 0

# Create and run the portfolio
def runPortfolio (capital, size, interval, price, entrySgn, exitSgn, sl):
    return vbt.Portfolio.from_signals (
        price,
        entries = entrySgn,
        exits   = exitSgn,
        direction = 'longonly',
        size = size,
        size_type = 'value',
        init_cash = capital,
        size_granularity = 1,
        group_by = True,
        cash_sharing = True,
        freq = interval,
        sl_stop = sl)

# Get the trades of a portfolio.
def getTrades (portfolio):
    return portfolio.trades.records_readable

# Summation of all PnL values on a portfolio.
def getPnL (portfolio):

    trades = getTrades (portfolio)
    PnL = trades ['PnL'].sum ()

    return PnL

def getTotalPnL ():
    global TotalPnL
    return TotalPnL

def zeroPnL ():
    global TotalPnL
    TotalPnL = 0

# Accumulates PnL across different portfolios.
def accPnL (portfolio):

    global TotalPnL

    PnL = getPnL (portfolio)

    TotalPnL += PnL

    return PnL, TotalPnL

# Computes expectancy from a series of trades.
def comptExpect (trades):

    N = trades ['PnL'].count ()

    # No trades to compute the expectancy with.
    if N == 0: return 0

    Nw = (trades ['PnL'] >= 0).sum ()
    Nl = (trades ['PnL'] < 0).sum ()

    Pw = Nw / N
    Pl = Nl / N

    pTrades = trades.loc [trades ['PnL'] >= 0]
    profit = pTrades ['PnL'].sum ()

    lTrades = trades.loc [trades ['PnL'] < 0]
    loss = lTrades ['PnL'].sum ()

    return (Pw * profit) + (Pl * loss)

# Updates capital profits or losses.
def updtCapital (portfolio, capital):
    
    trades = getTrades (portfolio)
    capital += trades ['PnL'].sum ()

    return capital

