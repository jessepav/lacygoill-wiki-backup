# Purpose: do some arithmetic on booleans
# Reference: page 78

# `True`  and `False`  are keywords  used  to represent  boolean values  (called
# "truth values"  in boolean algebra).   They are objects instantiated  from the
# `bool` class (i.e. their type is `bool`).
print(type(True))
print(type(False))
#     <class 'bool'>
#     <class 'bool'>

# `bool` is a subclass of `int`, which can only instantiate 1 and 0.
# In  an integer  context  (i.e. where  Python expects  an  integer), `True`  is
# evaluted to 1, and `False` to 0.
print(int(True))
print(int(False))
#     1
#     0
print(1 + True)
print(False + 42)
#     2
#     42

# In a boolean context, (i.e. where Python expects a boolean), 0 is evaluated to
# `False`, and all other integers evaluate to `True`.
print(bool(0))
print(bool(1))
print(bool(-42))
#     False
#     True
#     True

# boolean  values can  be  combined  in boolean  expressions  using the  logical
# operators `and`, `or`, `not`
print(not True)
print(True and True)
print(False and True)
print(False or True)
#     False
#     True
#     False
#     True
