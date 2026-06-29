'''
To plot charts.
'''

import plotly.graph_objects as go

from plotly.subplots import make_subplots

# Just plotting charts using 'plotly'.
# 'plotly' offers a convenient user interface on the internet browser.
# Documentation at: 'https://docs.plotly.com/'
def graphStrategy (graphCS, graphOrders, graphInd, graphSR):

    nRows = 1 + len (graphInd)

    graphStrategy = make_subplots (rows = nRows, cols = 1, shared_xaxes = True)

    # Close
    if len (graphCS):
        graphClose = graphStrategy.add_scatter (x = graphCS ['x'], y = graphCS ['C'], mode = 'lines', name = 'Close',
                                                row = 1, col = 1)
        graphClose.update_layout (title = 'Symbol - ' + graphCS ['symbol'])

    # Support and resistance.
    if graphSR is not None:
        graphStrategy.add_scatter (x = graphSR ['R'].index, y = graphSR ['S'], mode = 'lines', name = 'Support',
                                   row = 1, col = 1)
        graphStrategy.add_scatter (x = graphSR ['R'].index, y = graphSR ['R'], mode = 'lines', name = 'Resistance',
                                   row = 1, col = 1)

    # Entry and exit points.
    if len (graphOrders):
        for trade in graphOrders:
            graphStrategy.add_scatter (x = trade ['x'], y = trade ['y'], mode = 'markers', name = trade ['name'],
                                       row = 1, col = 1)

    # Indicators.
    R = 2
    if len (graphInd):
        for ind in graphInd.keys ():
            for name in graphInd [ind].keys ():
                graphStrategy.add_scatter (x = graphInd [ind][name].index,
                                           y = graphInd [ind][name],
                                           mode = 'lines', name = name,
                                           row = R, col = 1)
            R += 1

    graphStrategy.show ()

# Candlestick chart for a period.
def graphOHLCV (graphCS):

    if len (graphCS):
        graphCScheck = go.Figure (data = [go.Candlestick (
            x = graphCS ['ohlcv']['Open'].index,
            open  = graphCS ['ohlcv']['Open'],
            high  = graphCS ['ohlcv']['High'],
            low   = graphCS ['ohlcv']['Low'],
            close = graphCS ['ohlcv']['Close']) ])

        graphCScheck.show ()

