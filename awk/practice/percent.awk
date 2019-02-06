#!/usr/bin/awk -f

# input:  a column of non-negative numbers
# output: each number and its percentage of the total
#
# input example:
#
#         12
#         34
#         56
#         78
#         90
#
# output example:
#
#         12.00      4.4  %
#         34.00      12.6 %
#         56.00      20.7 %
#         78.00      28.9 %
#         90.00      33.3 %

{
    sum += $1
    x[NR] = $1
}

END {
    # check that the total sum is not zero, because dividing by zero is
    # forbidden
    if (sum != 0)
        for (i in x)
            printf "%-10.2f %-5.1f%%\n", x[i], x[i] / sum * 100
}

