#!/usr/bin/awk -f

# Part 1 {{{1
#
# add up numbers containing commas, getting rid of commas

# This program doesn't check  that the commas are in the  right places, nor does
# it print commas in its answer.

#     {
#         gsub(/,/, "")
#         sum += $0
#     }
#     END { print sum }

# Part 2 {{{1
#
# input:  a number per line
# output: the input  number followed by its formatted version  (i.e. with commas
# and two decimal places)

# This program  formats numbers  with commas  and two  digits after  the decimal
# point.
#
# The  algorithm uses  recursion to  handle negative  numbers: if  the input  is
# negative, `addcomma()` calls itself with  the positive value, prepends a minus
# sign, and returns the result.

#     { printf("%-12s %20s\n", $0, addcomma($0)) }
#
#     function addcomma(x,   num) {
#         if (x < 0)
#             return "-" addcomma(-x)
#         num = sprintf("%.2f", x)
#
#         # as long as you can find 4 consecutive digits
#         # we must add a comma somewhere
#
#         while (num ~ /[0-9][0-9][0-9][0-9]/)
#
#             # find 3 digits followed by a comma or a point
#             # and prepend a comma in front of them
#
#             sub(/[0-9][0-9][0-9][,.]/, ",&", num)
#
#         # The basic idea is to insert commas from the decimal point to the left in a
#         # loop; each  iteration puts a comma  in front of the  leftmost three digits
#         # that are followed by a comma or decimal point.
#         # It won't do the following substitution:
#         #
#         #     123,456    →    ,123,456
#         #
#         # ... because the condition to stay in the loop is to find 4 consecutive digits.
#         #
#         # e.g.:
#         #            1234567890.00    initial value of `num`
#         #                             it has 2 digits after the point because of `sprintf()`
#         #
#         #           1234567,890.00    end of 1st iteration
#         #          1234,567,890.00    "      2nd "
#         #         1,234,567,890.00    "      3rd "
#
#     return num
# }

# Part 3 {{{1

#     BEGIN {
#         sign               = "[-+]?"
#         no_comma           = "[0-9]*"
#         before_first_comma = "[0-9][0-9]?[0-9]?"
#         after_commas       = "(,[0-9][0-9][0-9])*"
#         fraction           = "[.][0-9]*"
#
#         pattern            = "^" sign "(" no_comma "|" before_first_comma after_commas ")" \
#                              "(" fraction ")?$"
#     }
#
#     $0 ~ pattern {
#         gsub(/,/, "")
#         sum += $0
#         next
#     }
#
#     { print "bad format:", $0 }
#     END { print sum }

