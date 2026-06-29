'''
Managing dates and time zones.
'''

import re

from datetime import datetime, timedelta
from dateutil import tz

from modules.Calendar   import *

# We operate on NYSE.
marketTZ = 'America/New_York'

# Stock exchange schedule.
SEstart = '09:30'
SEclose = '16:00'

def getSEstart ():
    global SEstart
    return SEstart

def getSEclose ():
    global SEclose
    return SEclose

# Convenience variables to hold time deltas.
SEstartDelta = timedelta (hours = 9,  minutes = 30)
SEcloseDelta = timedelta (hours = 16)
SEopenDelta  = SEcloseDelta - SEstartDelta

def getSEstartDelta ():
    global SEstartDelta
    return SEstartDelta

def getSEcloseDelta ():
    global SEcloseDelta
    return SEcloseDelta

def getSEopenDelta ():
    global SEopenDelta
    return SEopenDelta

# Lagging period to properly compute indicators.
dtLag = None

def getDtLag ():
    global dtLag
    return dtLag

# Returns the time for the last period of the target day.
# If we operate on market hours, we can't place a trade at '16:00'
# Considered periods are:
# "1m", "2m",  "5m",  "15m" and "1h".
# Last period times are:
# '15:59', '15:58', '15:55', '15:45', '15:30'.
def lastPeriod (signalTF):

    match signalTF:
        case '1m':
            return '15:59'
        case '2m':
            return '15:58'
        case '5m':
            return '15:55'
        case '15m':
            return '15:45'
        case '1h':
            return '15:30'
        case _:
            print ("ERROR: lastPeriod: Couldn't get last period time.")
            exit (-1)

# From a time frame string, returns the parameters suitable for "timedelta".
def tDelta (s):

    m = re.compile ('^\d{1,2}')
    p = re.compile ('m$|h$|d$|wk$|mo$')

    mult = int (m.search (s).group (0))

    period = p.search (s).group (0)

    match period:
        case 'm':
            days = 0; hours = 0; minutes = mult
            return days, hours, minutes
        case 'h':
            days = 0; hours = mult; minutes = 0
            return days, hours, minutes
        case 'd':
            days = mult; hours = 0; minutes = 0
            return days, hours, minutes
        case 'wk':
            days = mult * 7; hours = 0; minutes = 0
            return days, hours, minutes
        case 'mo':
            days = mult * 30; hours = 0; minutes = 0
            return days, hours, minutes
        case _:
            print ("ERROR: tDelta: Couldn't parse the time frame.")
            exit ()

# Interval, in days, for which ADX will return no data.
def intDays (tf, n):

    match tf:
        case '1m':
            return int (n / (6 * 60 + 30)) + 3
        case '2m':
            return int ((2 * n) / (6 * 60 + 30)) + 3
        case '5m':
            return int ((5 * n) / (6 * 60 + 30)) + 3
        case '15m':
            return int ((15 * n) / (6 * 60 + 30)) + 3
        case '1h':
            return int ((60 * n) / (6 * 60 + 30)) + 3
        case '1d':
            return 47
        case _:
            print ("ERROR: intDays: Not a valid time frame.")
            exit ()

# DST is active.
def DSTactive (date):

    if (date.dst () == timedelta (0)):
        return True
    else:
        return False

# Computes the time difference between a foreign time zone and that of the system.
def TZdiff (foreignTZ, date):

    # TZ aware local and foreign dates.
    localDate = date.astimezone ()
    foreignDate = date.astimezone (foreignTZ)

    # Extracting difference between timezones.
    try:
        foreignDiff = (int (foreignDate.strftime ('%z'))) / 100
    except Exception:
        print ("ERROR: TZdiff: Can't parse the time zone.")
        exit ()

    try:
        localDiff = (int (localDate.strftime ('%z'))) / 100
    except Exception:
        print ("ERROR: TZdiff: Can't parse the time zone.")
        exit ()

    return (foreignDiff - localDiff)

# Converts to a foreign time zone, keeping the same local time.
# We need it, for example, to set stock exchange opening time (like '9:30'),
# with disregard of the time zone we are in.
#
# So, if we set 'local' as:
#
# '2026-06-16 09:30:00+02:00'
#
# and 'foreignTZ' as 'America/New_York'
#
# 'toForeign' will return:
#
# '2026-06-16 09:30:00-04:00'
#
def toForeign (foreignTZ, local):

    TZ = tz.gettz (foreignTZ)

    foreign = local.astimezone (TZ)

    hDiff = TZdiff (TZ, foreign)

    return (foreign - timedelta (hours = hDiff))

# Returns proper start and end time for a single day backtesting.
def targetDate (date, TZstr):

    global dtLag, SEstartDelta, SEcloseDelta

    target = toForeign (TZstr, date)

    # At least one day is discounted from "start" on "lastBusiness".

    # To compute MACD we need at least three business days.
    start = addBusiness (target, -2)

    dtLag = target - start

    start = start  + SEstartDelta
    end   = target + SEcloseDelta

    return start, end

# With a date target return a start and end date for an specified number of periods.
# If 'end' or 'start' are  not business days, check the last one.
def targetPeriod (date, timeFrame, n):

    global SEstartDelta, SEcloseDelta

    end = date - timedelta (days = 1)

    if (not isBusiness (end)): end = lastBusiness (end)

    d = intDays (timeFrame, n)
    start = end - timedelta (days = d)

    if (not isBusiness (start)): start = lastBusiness (start)

    start = toForeign (marketTZ, start)
    end   = toForeign (marketTZ, end)

    start = start + SEstartDelta
    end   = end   + SEcloseDelta

    return start, end

