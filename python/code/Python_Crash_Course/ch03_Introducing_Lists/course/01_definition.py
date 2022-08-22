# Purpose: set a list
# Reference: page 33 (paper) / 71 (ebook)

bicycles = ['trek', 'cannondale', 'redline', 'specialized']

# A list is an ordered collection of arbitrary items. {{{1

# It's defined inside square brackets, and its items are separated with commas.
#          v      v             v          v              v
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles)
#     ['trek', 'cannondale', 'redline', 'specialized']
#}}}1

# We can get the  `n`-th item of a list using an  index between square brackets. {{{1

# Since the first  index is always 0,  the `n`-th item can be  obtained with the
# index `n - 1`.
#
#             vvv
print(bicycles[0])
print(bicycles[1])
print(bicycles[2])
#     trek
#     cannondale
#     redline

#   Negative indexes are allowed. {{{1

# Contrary to positive indexes which count from the left, negative indexes count
# from the right.  Also, they start from `-1`, and not from `0`.
# So, to get the last item of a list you can use the index `-1`:
print(bicycles[-1])
#     specialized
#}}}1

# We can call a method on a list item. {{{1

#                v------v
print(bicycles[0].title())
#     Trek

# A list item is an expression, which can be used anywhere an expression is allowed. {{{1

# That includes inside braces in an f-string.
message = f'My first bicycle was a {bicycles[0].title()}.'
print(message)
#     My first bicyclew was a Trek.
