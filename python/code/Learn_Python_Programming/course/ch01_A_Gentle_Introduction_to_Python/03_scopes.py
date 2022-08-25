# Purpose: show how an enclosing scope can be looked into even in a local scope
# Reference: page 60

def enclosing_func():
    m = 13
    def local():
        print(m, 'printing from the local scope')
    local()

m = 5
print(m, 'printing from the global scope')
enclosing_func()
#     5 printing from the global scope
#     13 printing from the local scope
#
# When `local()` is called, Python can't find `m` in its local scope, but it can
# in the enclosing scope  of the immediate outer function.  It  can also find it
# in the global scope, but since  enclosing scopes come before the global scope,
# that's where Python  retrieves the value (and  that's why 5 is  printed in the
# first output line instead of 13).
