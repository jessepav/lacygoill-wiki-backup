#!/usr/bin/awk -f

# sum1 - print column sums {{{1
#
#   input:  rows of numbers
#   output: sum of each column

# missing entries are treated as zeroes

#     {
#         for (i = 1; i <= NF; ++i)
#             sums[i] += $i
#         if (NF > maxfld)
#             maxfld = NF
#     }
#
#     END {
#         for (i in sums)
#             printf "%g%s", sums[i], (i != maxfld ? "\t" : "\n")
#     }

# sum2 - print column sums (check same number of fields) {{{1
#
#   check that each line has the same number of fields as line one

#     NR == 1 { nfld = NF }
#
#     {
#         for (i = 1; i <= NF; ++i)
#             sums[i] += $i
#         if (NF != nfld)
#             print "line", NR, "has", NF, "entries, not", nfld
#     }
#
#     END {
#         for (i = 1; i <= nfld; ++i)
#             printf "%g%s", sums[i], (i < nfld ? "\t" : "\n")
#     }

# sum3 - print column sums (discard strings) {{{1
#
# Input:  rows of integers and strings
# Output: sums of numeric columns
#
# assumes every line has same layout:
#   if a field is numeric on the first line, assumes that all fields in the same
#   column are numeric (same thing if it's a string)
#
# if a field on the first line is '123abc', should ignore all the column
#
# assumes every number is an integer

#     nfld == 0 && NF > 0 {
#       │          │
#       │          └ and the line is not empty
#       └ the variable has been set up yet
#
#     # If we simply used the pattern `NR  == 1`, the code would fail when the
#     # first line(s) is/are empty.
#
#     # We need the second condition to make sure that the line is not empty.
#     # We need the first condition to execute the action only once.
#     # As soon as `nfld` has been set up, there's no need to reset it.
#
#         nfld = NF
#         for (i = 1; i <= NF; ++i)
#             # `numcol` is an array which contains `0`s and `1`s.
#             # `numcol[2] = 0` means that the second column contains strings
#             # `numcol[3] = 1` means that the third column contains numbers
#             numcol[i] = isnum($i)
#     }
#
#     {
#         for (i = 1; i <= NF; ++i)
#             # if the i-th column contains strings, increment the i-th element of the `sums` array
#             if (numcol[i])
#                 # we don't need the test, because we don't print the sums of strings
#                 # column in the END statement,
#                 # but letting unwanted computations occur could lead to bugs like
#                 # overflow (imagine lots of strings like "999999foo")
#
#                 # Zen: Avoid unwanted computations
#                 sums[i] += $i
#     }
#
#     END {
#         for (i = 1; i <= nfld; ++i) {
#             # if the i-th column contains numbers, print the sum
#             if (numcol[i])
#                 printf "%g", sums[i]
#             else
#                 # if it contains strings, print "--" to signify that
#                 # there's no numbers in it
#                 printf "--"
#             printf (i < nfld ? "\t" : "\n")
#         }
#     }
#
#     function isnum(n) {
#         # this regex only recognizes signed integers
#         return n ~ /^[+-]?[0-9]+$/
#
#         # this regex should recognize all kinds of numbers
#         sign     = "[-+]?"
#         decimal  = "[0-9]+[.]?[0-9]*"
#         fraction = "[.][0-9]+"
#         exponent = "[eE]" sign "[0-9]+"
#         number   = "^" sign "(" decimal "|" fraction ")(" exponent ")?$"
#
#         return n ~ number
#
#         # A more complex regex has an impact performance-wise.
#         # Execution time can increase significantly.
#         # To see it:
#         #
#         #   1. create a very big data file:
#         #
#         #         1 2 3
#         #         4 5 6
#         #         7 8 9
#         #
#         #     ... then `:%t$` to duplicate it as many times as wanted
#         #
#         #   2. time the execution of the program:
#         #
#         #         awk -f sum.awk data
#         #
#         # Zen: Perfect is the enemy of good
#     }

