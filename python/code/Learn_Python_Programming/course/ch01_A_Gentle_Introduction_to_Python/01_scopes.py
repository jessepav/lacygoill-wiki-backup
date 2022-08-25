# Purpose: show how the local scope has priority over the global one
# Reference: page 58

def local():
    # we define `m` within the local scope
    m = 7
    print(m, 'from the local scope')

# we define `m` within the global scope
m = 5
local()
print(m, 'from the global scope')
#     7 from the local scope
#     5 from the global scope
#
# The two output  numbers are different because the bindings  occur in different
# scopes.  The  `print()` in  `local()` prints  7 because in  its scope,  `m` is
# bound to  7 (because of the  `m = 7` assignment).  OTOH, the  `print()` in the
# script/module prints 5 because in its scope, `m` is bound to 5.
#
# This illustrates that Python looks first  in the local scope before the global
# scope.
