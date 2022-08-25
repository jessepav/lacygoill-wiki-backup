# Purpose: show how the global scope can be looked into even in a local scope
# Reference: page 59

def local():
    print(m, 'from the local scope')

m = 5
local()
print(m, 'from the global scope')
#     5 from the local scope
#     5 from the global scope
#
# This time, the two output numbers are identical.
# This illustrates that Python can look in the global scope even for a statement
# which is executed in a local scope.  If it did not, the `print()` in `local()`
# would have given an error since `m`  is not bound to anything in the `local()`
# scope.
