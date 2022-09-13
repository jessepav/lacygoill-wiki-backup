# Purpose: work with dates and times
# Reference: page 104

from datetime import date, datetime, timedelta, timezone
import time
import calendar as cal
from zoneinfo import ZoneInfo

# `date` is a class imported from the `datetime` module:
print(date)
#     <class 'datetime.date'>

# We instantiate an object form the `date` class:
today = date.today()
print(repr(today))
#     datetime.date(2022, 8, 31)

# current date {{{1
# `ctime()`, `isoformat()` {{{2

# The `ctime()` and `isoformat()` methods of the `today` object give the current
# date following resp. the C and ISO 8601 format standards:
print(today.ctime())
print(today.isoformat())
#
#                always set to 0 (not current time)
#                v------v
#     Wed Aug 31 00:00:00 2022
#     2022-08-31

# day of week {{{2

# There  are  2  syntaxes to  get  the  day  of  the week  (machine-readable  vs
# human-readable):
print(today.weekday())
print(cal.day_name[today.weekday()])
#     2
#     Wednesday
#
# In the first syntax, days are numbered from 0 (Monday) to 6 (Sunday).

# day, month, year {{{2

# The  `day`, `month`,  and `year`  attributes of  the `today`  object give  the
# current day, month, and year:
print((today.day, today.month, today.year))
#     (31, 8, 2022)

# numerical values {{{2

# The `timetuple()`  method of the  `today` object gives a  `struct_time` object
# containing numerical values about the current date:
print(today.timetuple())
#     time.struct_time(
#         tm_year=2022,
#         tm_mon=8,
#         tm_mday=31,
#         tm_hour=0,
#         tm_min=0,
#         tm_sec=0,
#         tm_wday=2,
#         tm_yday=243,
#         tm_isdst=-1
#     )
#
# All the  info about  time is  set to 0,  because we're  dealing with  a *date*
# object; not a *time* one.

# That object is subscriptable:
#                      vvv
print(today.timetuple()[:])
#     (2022, 8, 31, 0, 0, 0, 2, 243, -1)
# }}}1
# current time {{{1
# `ctime()` {{{2

# The `ctime()` function of the `time`  module gives the current date *and time*
# according to the C format standard:
print(time.ctime())
#     Wed Aug 31 15:32:48 2022
#
# Contrary  to `datetime.date.today().ctime()`,  the current  time is  given (as
# opposed to 0).

# daylight saving time {{{2

# The `daylight` attribute of the `time` module is 1 iff daylight saving time is
# in effect:
print(time.daylight)
#     1

# GMT / UTC {{{2

# The `gmtime()` function of the `time` module gives the current time in UTC:
print(time.gmtime())
#     time.struct_time(
#         tm_year=2022,
#         tm_mon=8,
#         tm_mday=31,
#         tm_hour=13,
#         tm_min=33,
#         tm_sec=7,
#         tm_wday=2,
#         tm_yday=243,
#         tm_isdst=0
#     )

# It accepts  an optional argument  to convert  an arbitrary time  (expressed in
# seconds since the epoch) into a `struct_time` object in UTC:
print(time.gmtime(0))
#     time.struct_time(
#         tm_year=1970,
#         tm_mon=1,
#         tm_mday=1,
#         tm_hour=0,
#         tm_min=0,
#         tm_sec=0,
#         tm_wday=3,
#         tm_yday=1,
#         tm_isdst=0
#     )

# local time {{{2

# The `localtime()` function  of the `time` module gives  a `struct_time` object
# containing numerical values about the current date *and time*:
print(time.localtime())
#     time.struct_time(
#         tm_year=2022,
#         tm_mon=8,
#         tm_mday=31,
#         tm_hour=15,
#         tm_min=34,
#         tm_sec=27,
#         tm_wday=2,
#         tm_yday=243,
#         tm_isdst=1
#     )

# epoch time {{{2

# The `time()` function of the `time` module  gives the current date and time in
# seconds since the epoch:
print(time.time())
#     1661952885.4306042
# }}}1
# current date and time {{{1

now = datetime.now()
utcnow = datetime.utcnow()

print(repr(now))
print(repr(utcnow))
print(repr(now.date()))
print(repr(now.time()))
#     datetime.datetime(2022, 8, 31, 17, 53, 4, 990778)
#     datetime.datetime(2022, 8, 31, 15, 53, 4, 990781)
#     datetime.date(2022, 8, 31)
#     datetime.time(17, 54, 36, 373308)

print(now.timetuple())
#     time.struct_time(
#         tm_year=2022,
#         tm_mon=8,
#         tm_mday=31,
#         tm_hour=17,
#         tm_min=55,
#         tm_sec=53,
#         tm_wday=2,
#         tm_yday=243,
#         tm_isdst=-1
#     )

print(now.date() == date.today())
#     True

print(now.weekday())
#     2

print((now.day, now.month, now.year))
print((now.hour, now.minute, now.second, now.microsecond))
#     (31, 8, 2022)
#     (17, 55, 3, 959452)

print(now.ctime())
print(now.isoformat())
#     Wed Aug 31 17:55:16 2022
#     2022-08-31T17:55:36.826833

print(now.tzinfo)
print(utcnow.tzinfo)
#     None
#     None
