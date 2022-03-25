#!/usr/bin/awk -f

# Input:  pairs of item and quantity{{{
#
#     mandarine 90
#     pomme     90
#     banane    34
#     kiwi      78
#     fraise    12
#     pomme     34
#     banane    56
#     mandarine 78
#     kiwi      56
#     fraise    12
#}}}
# Output: accumulate the total quantity for each item,{{{
# and print the result after sorting it alphabetically
#
#     banane    90
#     fraise    24
#     kiwi      134
#     mandarine 168
#     pomme     124
#}}}

{ total[$1] += $2 }

END {
    for (i in total)
        printf "%-10s%-10d\n", i, total[i] | "sort"
    close("sort")
}
