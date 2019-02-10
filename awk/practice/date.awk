#!/usr/bin/awk -f

# Exo 1: {{{1
#
# date convert - convert mmddyy into yymmdd in $1
#
# input example:
#
#     ┌ 01 = month
#     │ ┌ 30 = day
#     │ │ ┌ 42 = year
#     │ │ │
#     013042 mary's birthday~
#     032772 mark's birthday~
#     052470 anniversary~
#     061209 mother's birthday~
#     110175 elizabeth's birthday~
#
# output example:
#
#     423001 mary's birthday~
#     722703 mark's birthday~
#     702405 anniversary~
#     091206 mother's birthday~
#     750111 elizabeth's birthday~

#     { $1 = substr($1, 5, 2) substr($1, 3, 2) substr($1, 1, 2) ; print }

# Exo 2: {{{1
#
# input:  dates written as “year month day“.
# output: number of days between 01/01/1900 and the dates.
#
# Input example:
#
#     2017 5  18~
#     1949 2  15~
#     1992 9  24~
#     2008 5  30~
#     2011 11 4~
#
# Output example:
#
#     2017 5  18                42872~
#     1949 2  15                17943~
#     1992 9  24                33870~
#     2008 5  30                39597~
#     2011 11 4                 40850~


# A leap year has 29 days in February instead of 28.
# A leap year is divisible by 4, except if it's divisible by 100 but not by 400.
# Let's call (P1) and (P2) the following propositions:
#
#   (P1):    4 divides y
#   (P2):    100 divides y, but not 400
#
# We can rewrite the definition of a leap year like this:
#
# y is a leap year
# ⇔ (P1) except if (P2)
# ⇔ (P1)  ∧  ¬(P2)                         *1
# ⇔ 4|y   ∧  ¬(100|y  ∧  ¬(400|y))
# ⇔ 4|y   ∧  (¬100|y  ∨  400|y)
# ⇔ (4|y  ∧  ¬100|y)  ∨  (4|y  ∧  400|y)
#
# *1: “except if“
# =  “but it's not enough, sth else must also be false“
# =   ∧                    ¬
#
# Summary:
#
# A year is a leap year, iff, it's  divisible by 4 but not by 100 (e.g. `2020`),
# or it's divisible by 4 and by 400 (e.g. `2000`).


{ printf("%-10s %20s\n", $0, how_many_days($1, $2, $3)) }

function how_many_days(y, m, d,   a, n, i) {

    split("31 28 31 30 31 30 31 31 30 31 30 31", a)

    # convert whole years into days
    n = (y - 1900) * 365

    # add leap days for past years
    for (i = 1900; i < y; ++i) {
        if (is_leap(i))
            n++
    }

    # add leap day for current year, if the date is beyond march or if it's the
    # 29th February
    if (is_leap(y) && (m > 2 || (m == 2 && d == 29) )) {
        n++
    }

    # add days from the last year
    for (i = 1; i < m; ++i)
        n += a[i]

    # add days from the last month
    n += d

    return n
}

function is_leap(y) {
    if (y % 4 == 0 && (y % 100 != 0 || y % 400 == 0))
        return 1
    return 0
}

