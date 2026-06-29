Day Trading Backtesting Program:

1.- Introduction.
It is a Python program to backtest historic trading data. It is focussed on day trading.
It is able to test different strategies and to download ohlcv data from multiple providers.
It can backtest a range of dates, like a week or a month, and simulate day trading operations,
a day at a time. It uses python 'vectorBT' library to run the simulations.
Below there's a link to vectorBT. 

Please understand that day trading holds high risks. It can easily drive to financial losses.
The program is NOT intended for live trading. It deals with historic data and backtesting ONLY.

2.- Brief description.
The core of the program is the function 'runBT'. It takes as parameters an strategy, a list of symbols and
a 'target' date and it returns a vectorBT 'portfolio' with the results of backtesting.
You can pass to it 'ST_MOMENTUM' or 'ST_RANGING' as strategies, those are symbolic constants defined on
the module 'modules/Strategies.py'. The strategies themselves are defined on that module, too.

You can select a data provider by passing 'Alpaca' or 'YF' to 'setProvider', on the main section of the program.
Pleas note that if you choose Alpaca, you have to set 'ALPACA_API_KEY' and 'ALPACA_SECRET_KEY' on the module 'modules/Credentials.py',
with valid keys. 'YF' represents 'Yahoo Finance' python API.

After running the backtest it shows a brief summary with 'PnL' and mathematical expectancy, for every day.
After the dates range is run, it will show a brief summary with the same metrics and the remaining capital.
If the variable 'btTest' is set to 'True' the function 'dbgPlot' will show a series of charts with the most traded symbol,
its entry and exit points and the computed indicators. You can pass any symbol to 'dbgPlot', provided it has been traded.

3.- Running.
To run the program just update the variables 'first' and 'last' on the main section of 'mScalp.py'.
This variables contain the first and last dates to be backtested.
The variable 'symbols' contains a list of symbols that are most likely to move uptrending or ranging,
to test one of both strategies. You have to load it with any symbols read from an screener, for example.
You could also wish to modify 'sLoss' and 'slot'.
'sLoss' defines an stop loss passed to vectorBT 'portfolio' class, it is a per unit amount.
'slot' defines the fraction of cash to be spent per trade from 'capital', also a per unit amount.
The 'capital' variable is taken by default as $100,000. After the first run it is stored on the file 'config.py',
so the program can keep its value between runs. The file can be edited by hand to any value you want.
It is safe to delete the file and the 'capital' variable will be reset to $100,000.

The program will create two additional files 'data/trades.data' and 'data/trend.data'.
The first one just accounts for all trades completed on a program run, its just used to
compute the summaries, it contains internal data. It can be safely deleted between program runs.
The second one holds ohlcv data needed to compute the ADX indicator. If you change the 'symbols'
variable you have to delete it. It is safe to be deleted between program runs.

4.- Libraries used.

We list the python libraries used along with the websites to learn more about them:

1.- vectorBT - https://vectorbt.dev/
2.- Pandas - https://pandas.pydata.org/
3.- Yahoo Finance for python - https://pypi.org/project/yfinance/
4.- Alpaca for python - https://alpaca.markets/sdks/python/
5.- business-calendar - https://pypi.org/project/business-python/
6.- colorama - https://pypi.org/project/colorama/

5.- Assumptions.

The program has been written and tested on a Linux box. If we try to run it
on other operating systems we may need to adapt PATH-like variables as for example:

DataDir = './data/'

placed on the module 'modules/Collect.py'.

