# Purpose: work with dictionaries
# Reference: page 92 (paper) / 130 (ebook)

alien_0 = {'color': 'green', 'points': 5}

# The syntax of a dictionary is `{'key': 'value', ...}`. {{{1

alien_0 = {'color': 'green', 'points': 5}
#          ^--------------^  ^---------^
#
# This dictionary contains 2 key-value pairs.
# The comma separates 2 consecutive pairs.
# The colon separates a key from its value inside a given pair.
# }}}1

# The expression `dict['key']` lets you retrieve a value from a dictionary via its key. {{{1

#     v--------------v
print(alien_0['color'])
print(alien_0['points'])
#     green
#     5

# This expression can be saved in a variable and used later.
#            v---------------v
new_points = alien_0['points']
print(f'You just earned {new_points} points!')
#     You just earned 5 points!

#   The same syntax – used as an lvalue – lets you add a new key-value pair in a dictionary. {{{1

# Notice that this time, `dict['key']` is written on the LHS of an assignment.
# In this position, we're no longer dealing with an expression; that's an lvalue.
# ------------------v
alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)
#     {'color': 'green', 'points': 5, 'x_position': 0, 'y_position': 25}
#                                     ^-------------------------------^
#
# These 2 key-value pairs have been added  into the dictionary by the previous 2
# assignments.

#   Or change an existing value. {{{1

alien_0 = {'color': 'green'}
print(f"The alien is {alien_0['color']}.")

# -------------v
alien_0['color'] = 'yellow'
print(f"The alien is {alien_0['color']}.")
#     The alien is green.
#     The alien is yellow.
# }}}1

# `{}` is the empty dictionary.  It can be used to initialize a dictionary variable. {{{1
# That's useful when you need to build a dictionary programmatically at runtime.

#         vv
alien_0 = {}

alien_0['color'] = 'green'
alien_0['points'] = 5

print(alien_0)
#     {'color': 'green', 'points': 5}

# The `del` statement lets you remove a key-value pair from a dictionary. {{{1

alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

# v
del alien_0['points']
print(alien_0)
#     {'color': 'green', 'points': 5}
#     {'color': 'green'}
#
# Notice that you only  need to specify the name of the  dictionary and the key;
# not  the  value  associated  with  the  key.  Without  a  key,  the  value  is
# automatically removed too.

# A dictionary can be broken down on several lines. {{{1
# Typically, one key-value per line.

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

language = favorite_languages['sarah'].title()
print(f"Sarah's favorite languages is {language}.")
#     Sarah's favorite languages is C.

# The `get()` methods lets you retrieve a value from a dictionary using a key which might be absent from the latter. {{{1

alien_0 = {'color': 'greeen', 'speed': 'slow'}

#                           key           default value
#                         v------v  v------------------------v
point_value = alien_0.get('points', 'No point value assigned.')
print(point_value)
#     No point value assigned.
#
# No exception is raised because `get()` fell back on the default value supplied
# as its 2nd argument.

#                                 the 2nd argument is optional
#                                 v
point_value = alien_0.get('points')
print(point_value)
#     None
#
# If the second argument is omitted, and  the key is absent from the dictionary,
# `get()` uses `None`.  It's a keyword used to indicate the absence of a value.

print(alien_0['points'])
#     KeyError: 'points'
#
# Without `get()`,  an exception  is raised  because we've  asked for  the value
# associated  to the  'points' key  inside  the `alien_0`  dictionary.  But  the
# latter has no such key.
