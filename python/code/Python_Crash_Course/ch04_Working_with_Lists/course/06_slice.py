# Purpose: work on slice of a list
# Reference: page 61 (paper) / 99 (ebook)

players = ['charles', 'martina', 'michael', 'florence', 'eli']

# A slice is a contiguous subset of items from a given list. {{{1

# The general syntax is:{{{
#
#     list[a:b:c]
#
# Which evaluates to  the sublist of items  in `list` from the index  `a`, up to
# the index  `b`, skipping `c` items  when retrieving 2 consecutive  items.  The
# index `b` is exclusive, just like the 2nd argument of `range()`.
#
# All 3 indexes are optional, as well as the second colon.
# The first colon is mandatory.
#}}}

# That's a slice of  the `players` list which starts from  the first item (index
# 0), and ends right before the fourth item (index 3).
#            v---v
print(players[0:3])
#     ['charles', 'martina', 'michael']

# Here is another slice:
#            v---v
print(players[1:4])
#     ['martina', 'michael', 'florence']

# The first index can be omitted, in which case it defaults to 0. {{{1

#             v
print(players[:4])
#     ['charles', 'martina', 'michael', 'florence']

# The second index can also be omitted. {{{1

# In which case the slice goes till  the last item (including the latter).  It's
# not equivalent to writing -1, because the 2nd index is exclusive; with -1, the
# slice would stop right before the last item.

#              v
print(players[2:])
#     ['michael', 'florence', 'eli']

# Here is a slice where the third index is not omitted: {{{1

#                 vv
print(players[1:-1:2])
#     ['martina', 'florence']

# So far, we've only iterated over *whole* lists.  But it's also allowed to iterate over a *slice* of a list. {{{1

print('Here are the first three players on my team:')
#                    v--v
for player in players[:3]:
    print(player.title())
#     Here are the first three players on my team:
#     Charles
#     Martina
#     Michael

# `[:]` is a special slice which lets us make a copy of a list. {{{1

# I and my friend  like almost the same foods; but each of  us like 1 extra food
# not liked by the other.  Let's build 2 lists of the foods we like using a copy
# of a list for the foods we have in common.

my_foods = ['pizza', 'falafel', 'carrot cake']
# This is what creates a copy of `my_foods`.{{{
#
# If you omit it, `friend_foods` will not be assigned a *copy* of `my_foods`; it
# will be assigned a *reference* to the latter.  Which means that both variables
# will point to the same object.  Whatever  change you perform using one of them
# will affect the other.
#}}}
#                      vvv
friend_foods = my_foods[:]
# now that `friend_foods` is  a copy of `my_foods`, we can  start adding 1 extra
# food to each list without affecting the other
my_foods.append('cannoli')
friend_foods.append('ice cream')

print('My favorite foods are:')
print(my_foods)

print("\nMy friend's favorite foods are:")
print(friend_foods)
#     My favorite foods are:
#     ['pizza', 'falafel', 'carrot cake', 'cannoli']
#                                         ^-------^
#                                         extra food
#
#
#     My friend's favorite foods are:
#     ['pizza', 'falafel', 'carrot cake', 'ice cream']
#                                         ^---------^
