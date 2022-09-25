# Purpose: work with dates and times
# Reference: page 104

from datetime import date, datetime, timedelta, timezone
import time
import calendar
from zoneinfo import ZoneInfo

# `date` is a class imported from the `datetime` module:
print(date)
#     <class 'datetime.date'>

# We instantiate an object for the current date from the `date` class:
today = date.today()
print(repr(today))
#     datetime.date(2022, 8, 31)

# We instantiate objects for the current date *and time* from the `datetime` class:
now = datetime.now()
utcnow = datetime.utcnow()

# `date.today()` and `now.date()` are the same object:
print(id(date.today()) == id(now.date()))
#     True

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
print(calendar.day_name[today.weekday()])
#     2
#     Wednesday
#
# In the first syntax, days are numbered from 0 (Monday) to 6 (Sunday).

# `now` also implements the `weekday()` method:
print(now.weekday())
#     2

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
# opposed to be naively set to 0).

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

print(repr(now.date()))
print(repr(now.time()))
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

print((now.day, now.month, now.year))
print((now.hour, now.minute, now.second, now.microsecond))
#     (31, 8, 2022)
#     (17, 55, 3, 959452)

print(now.ctime())
print(now.isoformat())
#     Wed Aug 31 17:55:16 2022
#     2022-08-31T17:55:36.826833

# We can create a `datetime` object from an ISO-formatted string or a timestamp:
print(repr(datetime.fromisoformat('1977-11-24T19:30:13+01:00')))
print(repr(datetime.fromtimestamp(time.time())))
#     datetime.datetime(
#         1977, 11, 24, 19, 30, 13,
#         tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
#     )
#     datetime.datetime(2022, 9, 25, 17, 12, 18, 227417)

# time zone info and durations {{{1

# `now`  and `utcnow`  are "naive"  objects: they  contain time  quantities, but
# don't tell us which time zone those time quantities belong to.
print(now.tzinfo)
print(utcnow.tzinfo)
#     None
#     None

# Save the birthdays of Fabrizio and Heinrich in variables.{{{
#
# Notice that those objects are "aware", because they do tell us which time zone
# the times  belong to.  The first  one uses the `ZoneInfo()`  function from the
# `zoneinfo`  module,  which  requires  Python  3.9.  The  other  one  uses  the
# `timedelta()` function to represent a duration.
#}}}
f_bday = datetime(
    1975, 12, 29, 12, 50, tzinfo=ZoneInfo('Europe/Rome')
    #                     ^----------------------------^
)
h_bday = datetime(
    1981, 10, 7, 15, 30, 50, tzinfo=timezone(timedelta(hours=2))
    #                        ^---------------------------------^
)

# The difference between 2 dates is an instance of `timedelta`:
diff = h_bday - f_bday
print(type(diff))
#     <class 'datetime.timedelta'>

# We can  interrogate a `timedelta`  object to get the  duration as a  number of
# days or seconds:
print(diff.days)
print(diff.total_seconds())
#     2109
#     182223650.0

# Adding a duration to  a `date` or `datetime` object produces  the same type of
# object:
print(today + timedelta(days=49))
print(now + timedelta(weeks=7))
#     2022-11-13
#     2022-11-13 15:22:41.451705

# arrow third-party library {{{1

# The third-party `arrow`  module provides a wrapper around  the data structures
# of the standard library, as well as a  set of methods which makes it easier to
# deal with dates and times.  To install it:
#
#     # https://arrow.readthedocs.io/en/latest/
#     $ python3 -m pip install --user --upgrade arrow

import arrow

print(repr(arrow.utcnow()))
print(repr(arrow.now()))
#     <Arrow [2022-09-25T18:23:56.199170+00:00]>
#     <Arrow [2022-09-25T20:23:56.199235+02:00]>

# The `to()` method can convert the current time from a time zone to another:
local = arrow.now('Europe/Rome')
print(repr(local))
print(repr(local.to('utc')))
print(repr(local.to('Europe/Moscow')))
print(repr(local.to('Asia/Tokyo')))
#     <Arrow [2022-09-25T20:23:56.199624+02:00]>
#     <Arrow [2022-09-25T18:23:56.199624+00:00]>
#     <Arrow [2022-09-25T21:23:56.199624+03:00]>
#     <Arrow [2022-09-26T03:23:56.199624+09:00]>

# The `datetime` attribute gives the underlying `datetime` object:
print(repr(local.datetime))
#     datetime.datetime(
#         2022, 9, 25, 20, 23, 56, 199624,
#         tzinfo=tzfile('/usr/share/zoneinfo/Europe/Rome')
#     )

# The `isoformat()` method gives the  ISO-formatted representation of a date and
# time:
print(repr(local.isoformat()))
#     '2022-09-25T20:23:56.199624+02:00'
