#!/bin/bash

# Purpose: format database of addresses; group people by state
# Test: `$ ./nameState.sed ./input/addresses | ./byState.sh`
# Reference: page 16 (paper) / 40 (ebook)


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
# Alternatively, you could have used a single pattern-action statement:{{{
#
#     $1 == lastState { print "\t" $2 }
#     $1 != lastState { lastState = $1; print $1; print "\t" $2 }
#
#     ⇔
#
#     {
#         if ($1 == lastState)
#             { print "\t" $2 }
#         else
#             { lastState = $1; print $1; print "\t" $2 }
#     }
#}}}
