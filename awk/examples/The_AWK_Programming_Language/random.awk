#!/usr/bin/awk -f

# Description: generate random numbers between 0 and 100
# Input: positive integer `N`
# Output: `N` random numbers
BEGIN {
    n = ARGV[1]
    srand()
    for (i = 1; i <= n; ++i)
        print int(rand()*101)
    #                      │
    #                      └ if we multiply by 100, we couldnt randomly
    #                        generate 100 (ex: 0.9999 * 100 = 99.99, and
    #                        int(99.99) = 99)
}

