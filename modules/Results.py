'''
To plot graphics and print results.
'''

import pandas as pd
import vectorbt as vbt

# Plotting nice charts.
import plotly.graph_objs as go

from modules.Utils      import *
from modules.Collect    import DataDir
from modules.Portfolio  import *

tradesFile = 'trades.data'
tradesPath = DataDir + tradesFile

# Load a series of trades from a file.
def loadTrades ():
    return pd.read_pickle (tradesPath)

# Save a series of trades to a file. The trades are accumulated from a series
# of portfolios.
def saveTrades (portfolio):

    trades = getTrades (portfolio)

    if os.path.exists (tradesPath):
        lTrades = pd.read_pickle (tradesPath)
        trades = pd.concat ([lTrades, trades], ignore_index = True)

    createDir (DataDir)

    trades.to_pickle (tradesPath)

# To print mathematical expectancy.
def prnExpect (portfolio):

    global TotalExp

    expect = comptExpect (getTrades (portfolio))

    prnAmount ('Expectancy', expect)

# To print total porfolio's 'PnL'.
def prnPnL (portfolio):

    global TotalPnL

    PnL = getPnL (portfolio)
    TotalPnL = getTotalPnL ()

    prnAmount ('PnL', PnL)
    prnTotal ('Acc. PnL', TotalPnL)

# Nicely printing trades header.
def prnTrRow (t):
    print (f"{t ['Column']:6} | ", end = '')
    print (t ['Entry Timestamp'].strftime ('%H:%M'), ' | ', end = '')
    print (t ['Exit Timestamp'].strftime ('%H:%M'), ' | ', end = '')
    print ('%6.0f | '% t ['Size'], end = '')
    print ('%10.3f | '% t ['Avg Entry Price'], end = '')
    print ('%10.3f | '% t ['Avg Exit Price'], end = '')
    print ('%10.3f | '% t ['PnL'], end = '')
    print ()

# Nicely printing trades.
#
# Trades have the following structure:
#
# #   Column           Non-Null Count  Dtype
# ---  ------           --------------  -----
#  0   Exit Trade Id    5 non-null      int64
#  1   Column           5 non-null      object
#  2   Size             5 non-null      float64
#  3   Entry Timestamp  5 non-null      datetime64[ns, America/New_York]
#  4   Avg Entry Price  5 non-null      float64
#  5   Entry Fees       5 non-null      float64
#  6   Exit Timestamp   5 non-null      datetime64[ns, America/New_York]
#  7   Avg Exit Price   5 non-null      float64
#  8   Exit Fees        5 non-null      float64
#  9   PnL              5 non-null      float64
#  10  Return           5 non-null      float64
#  11  Direction        5 non-null      object
#  12  Status           5 non-null      object
#  13  Position Id      5 non-null      int64
#
def prnTrades (portfolio):

    trades = getTrades (portfolio)

    if len (trades):

        print("\nTrades:")
        print ("{:<5}".format ('Symbol'), '| ', end = '')
        print ("{:<5}".format ('Entry'), ' | ', end = '')
        print ("{:<5}".format ('Exit'), ' | ', end = '')
        print ("{:<4}".format (' Size'), ' | ', end = '')
        print ("{:<9}".format ('  Buy'), ' | ', end = '')
        print ("{:<9}".format ('  Sell'), ' | ', end = '')
        print ("{:<9}".format ('  PnL'), ' | ', end = '')
        print ()

        trades.apply (prnTrRow, axis = 1)

def prnStats (portfolio):

    # Show backtesting results.
    stats = portfolio.stats ()
    
    # print ("\nBacktesting Stats:")
    print (stats)
# 
# def plotResults (portfolio, sym):
#     
#     # Plotting nice charts.
#     
#     # Extracting equity and drawdown data
#     equity_data = portfolio.value ()
#     drawdown_data = portfolio.drawdown () * 100
#     
#     # Plotting the equity curve with Plotly
#     equity_trace = go.Scatter (x=equity_data.index, y=equity_data, mode='lines', name='Equity Curve')
#     equity_layout = go.Layout (title='Equity Curve', xaxis_title='Date', yaxis_title='Equity')
# 
#     try:    
#         equity_fig = go.Figure (data=[equity_trace], layout=equity_layout)
#     except ValueError:
#         print ("ERROR: plotResults: Can't plot the figure.")
#         exit ()
#     
#     equity_fig.show ()
#     
#     # Plotting the drawdown curve as a reddish-brown area plot with Plotly
#     drawdown_trace = go.Scatter (
#         x=drawdown_data.index,
#         y=drawdown_data,
#         mode='lines',
#         name='Drawdown Curve',
#         fill='tozeroy',
#         line=dict(color='brown'))
#     
#     drawdown_layout = go.Layout(
#         title='Drawdown Curve',
#         xaxis_title='Date',
#         yaxis_title='Drawdown %',
#         template='plotly_white')
#     
#     try:    
#         drawdown_fig = go.Figure (data = [drawdown_trace], layout = drawdown_layout)
#     except ValueError:
#         print ("ERROR: showResults: Can't plot the figure.")
#         exit ()
#     
#     drawdown_fig.show ()
#     
#     # Trading strategy’s performance.
#     portfolio.plot ().show ()
# 
