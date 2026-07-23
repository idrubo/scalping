
# Copyright (c) 2026 Lluis Sala Masdemont. All Rights Reserved.

'''
To implement scalping strategies.
'''

from datetime import datetime, timedelta
from dateutil import tz

import pandas as pd
import vectorbt as vbt

from modules.Dates      import *
from modules.Strategies import *
from modules.Portfolio  import *
from modules.Results    import *

# To debug.
from modules.Debug      import *

# Capital variable loaded from a python module as a config file.
from modules.loadConfig import *

# To choose a data provider.
from modules.Providers  import setProvider

# Fetch historical data.
def dailyData (symbols, target):

    # Compute start and end backtesting times.
    start, end = targetDate (target, marketTZ)

    return collect (symbols, signalTF, start, end)

# Run the backtester.
def runBT (strategy, symbols, target):

    global capital, sLoss

    # Load data.
    ohlcv = dailyData (symbols, target)

    if btTest: dbgSetOHLCV (ohlcv)

    # Generate signals.
    entrySgn, exitSgn = signals (strategy, ohlcv ['High'], ohlcv ['Low'], ohlcv ['Close'])

    # Create a portfolio.

    # The first day is only needed to initialize indicator values.
    start  = ohlcv ['Close'].index [0]
    end    = ohlcv ['Close'].index [-1]
    actual = start + getDtLag ()
    price  = ohlcv ['Close'] [actual:end]

    portfolio = runPortfolio (capital, size, signalTF, price, entrySgn, exitSgn, sLoss)

    return portfolio

###
# Main:
#

# Portfolio initial capital. You can set 'capital' from the file 'config.py'.
# If you delete that file a value of $100,000 is taken as 'capital'.
initialC = capital

# Position size.
# We allocate 20% of the capital per trade.
slot = 0.2
# For volatile markets we could reduce allocation size:
# slot = 0.125
size = capital * slot

# Stop loss:
# Typical:
sLoss = 0.01 # 1%
# sLoss = 0.0025 # 0.25%
# For volatile markets we could loosen stop losses:
# sLoss = 0.02 # 2.0%

# Choose a target date range and the stocks to trade.
# Start and end dates to backtest. Both dates will be backtested.
first = '2026-06-01'
last  = '2026-06-05'

# Make sure we have selected proper business days.
if (not isBusiness (first) or (not isBusiness (last))):
    prnError ('Not a Business day !!!')
    exit (1)

# The symbols are taken from an screener as to choose the symbols with more chances to
# move uptrending or sideways.
# We select our symbols from the following list:
# For momentum trading:
symbols = [ 'BAC', 'WFC', 'NVO', 'NEE', 'VZ', 'T', 'SCHW', 'PFE', 'BMY', 'CMCSA', 'CSX', 'USB', 'KMI', 'CVNA', 'VALE', 'HOOD', 'WBD', 'NKE', 'OXY', 'DVN', 'F', 'HPE', 'CMG', 'PYPL', 'RKT', 'VG', 'KVUE', 'HBAN', 'RBLX', 'KHC', 'KEY', 'RF', 'SOFI', 'HPQ', 'IREN', 'SMCI', 'RIVN', 'GIS', 'PR', 'HST', 'DOC', 'TOST', 'CSGP', 'FIG', 'AGNC', 'U', 'PINS', 'TTD', 'AAL', 'LUNR', 'NCLH', 'ENPH', 'CAG', 'CLF', 'HIMS', 'KLAR', 'PATH', 'LYFT', 'MARA', 'SMR', 'FLNC', 'SEDG', 'DOCS', 'RUN', 'NTLA']

# For range trading:
# symbols = [ 'NFLX', 'NVO', 'T', 'PFE', 'PDD', 'PBR', 'CMCSA', 'NOK', 'CVNA', 'VALE', 'B', 'HOOD', 'NKE', 'F', 'MDLN', 'INFY', 'HPE', 'GFS', 'CMG', 'RKT', 'CCL', 'CPRT', 'EL', 'FISV', 'CPNG', 'HPQ', 'SMCI', 'IREN', 'SOFI', 'RIVN', 'CDE', 'LI', 'OWL', 'PL', 'XPEV', 'SMMT', 'FIG', 'OKLO', 'JOBY', 'PINS', 'TTD', 'RIOT', 'AAL', 'RGTI', 'ENPH', 'NCLH', 'PATH', 'HIMS', 'LYFT', 'MARA', 'SMR', 'RDW' ]

# Choose a data provider:
# Only alpaca and yahoo finance are allowed, for now.
# If we choose 'Alpaca' we need to set proper API keys on 'modules/Credentials.py'
# setProvider ('Alpaca')
setProvider ('YF')

# Remove past data.
rmDir (getDataDir ())

# Get trend data.
start = datetime.strptime (first, '%Y-%m-%d')
end   = datetime.strptime (last, '%Y-%m-%d')

ohlcv = loadTrend (symbols, start, end, trendTF)

# Generate target business days.
tgtIdx = pd.bdate_range (start = first, end = last)

if (tgtIdx.empty):
    print ("Not a business date !!!")
    exit (-1)

# Iterating over the date range:
for tgt in tgtIdx:

    # If a target date is NOT a business day, skip it.
    if not isBusiness (tgt): continue

    target = tgt.to_pydatetime ()

    prnVar ("\nTarget date", '%s', target)
    prnVar ("Trend time frame", '%s', trendTF)
    prnVar ("Signal time frame", '%s', signalTF)

    # We get a list of uptrending symbols using ADX.
    uptrending, sideways = trendList (ohlcv, symbols, target, trendTF)
    prnVar ("Uptrending symbols", '%s', uptrending)
    prnVar ("Sideways symbols", '%s\n', sideways)

    # Run the backtest for an specific date on all symbols.
    # We will have to run a single strategy either a momentum or a ranging strategy.
    portfolio = runBT (ST_MOMENTUM, uptrending, target)
    # portfolio = runBT (ST_RANGING, sideways, target)

    # A portfolio is computed over a single day, so
    # we must compute stats between dates.
    accPnL (portfolio)

    # Show backtesting results.
    prnTrades (portfolio)
    prnPnL    (portfolio)
    prnExpect (portfolio)

    if btTest: dbgSetPF (portfolio)

    # Save all daily trades to compute a summary later.
    saveTrades (portfolio)

    # Update 'capital' value to be used across daily sessions.
    capital = updtCapital (portfolio, capital)
    size = capital * slot

# A result summary for the whole date range.
trades = loadTrades ()
expect = comptExpect (trades)

saveCapital (capital)

# The metrics, at the end, we are interested in.
prnMsg ('\nTotals:')
prnAmount ('Total Expectancy: ', expect)
prnAmount ('Initial Capital: ', initialC)
prnAmount ('Total Capital: ', capital)

# For debugging:
# If we send 'None' to 'dbgPlot', we will get charts for the most traded symbol.
# If we pass a symbol it will plot charts for that symbol, provided it has been
# traded.
if btTest: dbgPlot (None)

