#!/bin/bash

# Purpose: print  each state  once on a  line, then each  person living  in that
# state on another tab-indented line.
# Usage:{{{
#
#     $ ./nameState.sed list | ./byState.sh
#     California~
#             Amy Wilde~
#     Massachusetts~
#             Eric Adams~
#             John Daggett~
#             Sal Carpenter~
#     Oklahoma~
#             Orville Thomas~
#     Pennsylvania~
#             Terry Kalkas~
#     Virginia~
#             Alice Ford~
#             Hubert Sims~
#}}}

# Note the ingenious use of the first  awk program to make `sort` sort the lines
# according to an  arbitrary field (by temporarily duplicating  the fourth field
# at the start of each record).
awk -F, '{ print $4 ", " $0 }' "$@" \
  | sort \
  | awk -F, '$1 == lastState { print "\t" $2 }; $1 != lastState { lastState = $1; print $1; print "\t" $2 }'
# Note that the order of the statements in the last awk program is important.{{{
#
# `$1 == lastState ...` must come *before* `$1 != lastState ...`.
#
# Indeed, in  the reverse order,  when the first  test succeeds, the  second one
# always succeeds too.  So, the name of the first person living in a state would
# always be printed twice.
#}}}
