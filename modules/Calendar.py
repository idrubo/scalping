'''
To check business days against the stock exchange calendar.
'''

from datetime import datetime, timedelta, date
from business.calendar import Calendar

# For the NYSE:
# Taken from: https://www.nyse.com/trade/hours-calendars

# Holiday                                   2026                    2027                    2028
# New Year’s Day                            Thursday, January 1     Friday, January 1       —
# Martin Luther King, Jr. Day               Monday, January 19      Monday, January 18      Monday, January 17
# Washington's Birthday                     Monday, February 16     Monday, February 15     Monday, February 21
# Good Friday                               Friday, April 3         Friday, March 26        Friday, April 14
# Memorial Day                              Monday, May 25          Monday, May 31          Monday, May 29
# Juneteenth National Independence Day      Friday, June 19         Friday, June 18         Monday, June 19
# Independence Day                          Friday, July 3          Monday, July 5          Tuesday, July 4
# Labor Day                                 Monday, September 7     Monday, September 6     Monday, September 4
# Thanksgiving Day                          Thursday, November 26   Thursday, November 25   Thursday, November 23
# Christmas Day                             Friday, December 25     Friday, December 24     Monday, December 25

# Written on python:

# For 2026
H2026 = [
'Thursday, January 1 2026',
'Monday, January 19 2026',
'Monday, February 16 2026',
'Friday, April 3 2026',
'Monday, May 25 2026',
'Friday, June 19 2026',
'Friday, July 3 2026',
'Monday, September 7 2026',
'Thursday, November 26 2026',
'Friday, December 25 2026' ]

# For 2027
H2027 = [
'Friday, January 1 2027',
'Monday, January 18 2027',
'Monday, February 15 2027',
'Friday, March 26 2027',
'Monday, May 31 2027',
'Friday, June 18 2027',
'Monday, July 5 2027',
'Monday, September 6 2027',
'Thursday, November 25 2027',
'Friday, December 24 2027' ]

# For 2028
H2028 = [
'Monday, January 17 2028',
'Monday, February 21 2028',
'Friday, April 14 2028',
'Monday, May 29 2028',
'Monday, June 19 2028',
'Tuesday, July 4 2028',
'Monday, September 4 2028',
'Thursday, November 23 2028',
'Monday, December 25 2028' ]

Holidays = []
Holidays.extend (H2026)
Holidays.extend (H2027)
Holidays.extend (H2028)

NYSEcal = Calendar (holidays = Holidays)

# Self-explanatory.
def isBusiness (date):
    try:
        ret = NYSEcal.is_business_day (date)
    except:
        return False

    return ret

# Same as above.
def lastBusiness (date):
    lastB = NYSEcal.previous_business_day (date)
    return date - (date.date () - lastB)

# Same as above.
def nextBusiness (date):
    nextB = NYSEcal.next_business_day (date)
    return date + (nextB - date.date ())

# Return n-th previous/next business day.
def addBusiness (date, n):
    changeDate = NYSEcal.add_business_days (date, n)
    return date + (changeDate - date.date ())

