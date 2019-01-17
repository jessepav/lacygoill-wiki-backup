#!/usr/bin/env bash

# Description: generate random numbers between 0 and 100
# Usage:
#     ./random.sh 42    will generate 42 random numbers
awk '
BEGIN {
    n = ARGV[1]
    srand()
    for (i = 1; i <= n; ++i)
        print int(rand()*101)
#                          │
#                          └── if we multiply by 100, we couldnt randomly
#                              generate 100 (ex: 0.9999 * 100 = 99.99, and
#                              int(99.99) = 99)
}
' "$@"
