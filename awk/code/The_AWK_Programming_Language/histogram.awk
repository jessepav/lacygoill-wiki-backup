#!/usr/bin/awk -f

# Version 1 {{{1
# Voca: {{{

# En statistiques, un histogramme est un graphique permettant de représenter
# la répartition d'une variable continue (≈ qui peut prendre une infinité de
# valeurs). Ex: taille des invididus au sein d'une population.

# En statistique descriptive, un décile est chacune des 9 valeurs qui divisent
# un jeu de données, triées selon une relation d'ordre, en 10 parts égales,
# de sorte que chaque partie représente 1/10 de l'échantillon de population.
# Exemple de phrase utilisant “décile“:
#     Le 3e décile vaut 42.  (?)
#}}}
# Input:  a column of numbers, all between 0 and 100
# Output: histogram of deciles {{{

# The numbers must be grouped inside 11 buckets:    0 - 9, 10 - 19, … , 100
# The amount of numbers inside a bucket is a decile.

# The histogram must draw a sequence of `*` for each bucket, representing how
# many numbers are inside.

# Suppose we only have the numbers 11, 22 and 33, which appear 4 times, 5 and
# 6 times respectively. Then the histogram should look like:

#     10 - 19:  ****
#     20 - 29:  *****
#     30 - 39:  ******
#}}}
# We need to count how many numbers are inside a bucket. {{{
#
# What variables must we increment to count them?
#
# 11 variables are too much to manage: to store the amount of numbers
# in each bucket, an array `x` is better. Naive implementation:
#
#     if ($1 <= 9)
#         x[0]++
#     else if ($1 < 19 && $1 >= 10)
#         x[1]++
#     ...

# Too long to write.
# If we knew a relation `f` between $1 and the index of `x` to increment,
# we could reduce the previous code to:
#
#     x[f($1)]++

# What's the relation which verifies:
#
#     f([0, 9])   = 0
#     f([10, 19]) = 1
#     f([20, 29]) = 2
#     ...
#     f(100)      = 10
# ?

# Answer:    f(n) = E(n/10)

# Conclusion:
# to count how many numbers there are inside each bucket, we simply need to
# write:
#
#     { x[int($1/10)]++ }

# Another way of looking at it:
# we have 11 buckets. Let's give them a name: 0, 1, 2, …, 10
# Now, suppose we have the number 85. We know it must go in the bucket 8.
# What's the transformation we need to apply to the number 85 so that it goes
# into the bucket whose name is 8?
#
#     f(n) = E(n/10)

# So, `f(n)` gives us the index of the element of the array we must increment.
#}}}
{ x[int($1/10)]++ }

END {
    # initialize `max` and `term_width`
    # `max` will be updated to the biggest decile (length of the longest string of `*`)
    max = 25

    # get the number of columns of the terminal (output of `tput cols`)
    "tput cols" | getline term_width

    # remove 15 to this number, because some space is taken by the prefix text:
    #         10 - 19: xxx
    term_width -= 15

    # with `max`  and `term_width`, we can  scale the histogram to  the width of
    # the terminal,  by multiplying all  the frequencies (`x[i]`) by  the factor
    # `term_width/max`

    # For example,  if the  width is 100  but the biggest  decile is  200, we'll
    # multiply all deciles by  1/2, so that all the deciles  fit on the terminal
    # screen.

    # We need a loop with 10 iterations to draw the histogram. {{{
    # Because there are 10 buckets of numbers (outside of last bucket {100}):
    #
    #     1:    0 - 9
    #     2:   10 - 19
    #     3:   20 - 29
    #     ...
    # }}}
    for (i = 0; i <= 9; ++i)
        if (x[i] > max)
            max = x[i]
    for (i = 0; i <= 9; ++i) {
        printf " %2d - %2d: %3d %s\n",
               10*i,                          # lower border of the i-th bucket
               10*i + 9,                      # upper border of the i-th bucket
               x[i],                          # how many numbers are inside the i-th bucket
               rep(x[i] * term_width/max)     # strings of `*` to draw the bars of the histogram
    }
    # draw last bar
    printf "100:      %3d %s\n", x[10], rep(x[10] * term_width/max)
}

function rep(n,   s) {
    # We declare `s` as a local variable. {{{
    # This function is called several times in a `for` loop.
    # Therefore, if we let `s` be global, we  would have to reset it to an empty
    # string at the beginning of the function.
    # Without resetting  `s`, the histogram  would print lines longer  than what
    # they should be.
    # }}}
    # We could have used a `for` loop: {{{
    #
    #     for (i = 1; i <= n; ++i)

    # ... but `while` is shorter, and it doesn't create the global variable `i`.
    # With a `for`  loop, we would have to  declare `i` as a local  one to avoid
    # getting a conflict with a `i` in another loop of the main code.
    # }}}
    while (n-- > 0)
        s = s "*"
    return s
}

# Version 2 {{{1

# Add support for a variable width of buckets.

# Input:  a number interpreted as the desired number of buckets
#         + same as before (numbers between 0 and 100)
# Output: same as before (histogram)

#     BEGIN {
#         # get the desired number of buckets
#         nbuckets = ARGV[1]
#         # delete the numeric argument, so that it's not interpret as a file of the
#         # input
#         ARGV[1] = ""
#         # if the program didn't receive a numeric argument, exit, because dividing
#         # by zero is forbidden
#         if (nbuckets == 0)
#             exit
#         # deduce the width of the buckets
#         bucket_width = int(100/nbuckets)
#     }
#
#     { x[int($1/bucket_width)]++ }
#
#     END {
#         # TODO: How to avoid repeating the `exit` statement both in BEGIN and END.
#         if (nbuckets == 0)
#             exit
#
#         max = 25
#         "tput cols" | getline term_width
#         term_width -= 15
#
#         for (i = 0; i <= (nbuckets - 1); ++i)
#             if (x[i] > max)
#                 max = x[i]
#
#         for (i = 0; i <= (nbuckets - 1); ++i) {
#             printf " %2d - %2d: %3d %s\n",
#                    bucket_width * i,
#                    bucket_width * i + (bucket_width - 1),
#                    x[i],
#                    rep(x[i] * term_width/max)
#         }
#         printf "100:      %3d %s\n", x[10], rep(x[10] * term_width/max)
#     }
#
#     function rep(n,   s) {
#         while (n-- > 0)
#             s = s "*"
#         return s
#     }

# Version 3 {{{1

# Add support for any input numbers (the biggest is not necessarily 100 anymore)

# Input:  numbers between 0 and N
# Output: same as before (histogram)


#     BEGIN {
#         # get the desired number of buckets
#         nbuckets = ARGV[1]
#         # delete the numeric argument, so that it's not interpret as a file of the
#         # input
#         ARGV[1] = ""
#         # if the program didn't receive a numeric argument, exit, because dividing
#         # by zero is forbidden
#         if (nbuckets == 0)
#             exit
#     }
#
#     { x[NR] = $1 }
#
#     END {
#         "tput cols" | getline term_width
#         term_width -= 15
#
#         for (i in x)
#             if (x[i] > max)
#                 max = x[i]
#
#         if (nbuckets == 0 || max == 0)
#             exit
#
#         # deduce the width of the buckets
#         bucket_width = int(max/nbuckets)
#
#         for (i in x)
#             y[int(x[i]/bucket_width)]++
#
#         for (i = 0; i <= (nbuckets - 1); ++i) {
#             printf " %2d - %2d: %3d %s\n",
#                    bucket_width * i,
#                    bucket_width * i + (bucket_width - 1),
#                    y[i],
#                    rep(y[i] * term_width/max)
#         }
#         printf "%d:      %3d %s\n", max, y[10], rep(y[10] * term_width/max)
#     }
#
#     function rep(n,   s) {
#         while (n-- > 0)
#             s = s "*"
#         return s
#     }

