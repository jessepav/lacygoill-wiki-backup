# Purpose: write a simple class
# Reference: page 43 (paper) / 64 (ebook)


# A class name must follow the same rules as a variable name.
# It  must start  with a  letter or  underscore, and  can only  be comprised  of
# letters,  underscores, and  digits.   Besides, PEP8  recommends  that a  class
# should be named using "CapWords" notation (aka CamelCase).
#     v----------v
class MyFirstClass:
    pass
#     ^^
# Instead of adding data or behaviors, we use `pass` which is a null operation.
# It doesn't do anything.
# But syntactically we're required to include at least 1 statement in our class;
# so we use `pass` as a placeholder.


# It looks like we're calling a function,  but we're actually calling a class to
# create a new object.
#               vv
a = MyFirstClass()
b = MyFirstClass()
# instantiate an object from `MyFirstClass`, and assign it to `a`
print(a)
#     <__main__.MyFirstClass object at 0x7f2f33f301f0>
#                                              ^----^

# instantiate another object, and assign it to `b`
print(b)
#     <__main__.MyFirstClass object at 0x7f2f33e5eb20>
#                                              ^----^
# The last 6 digits  of this memory address is different  from the previous one.
# This shows that the 2 `MyFirstClass()`  calls have created 2 distinct objects,
# because they live at different memory addresses.

# We could also have used the `is` comparison operator to check that the objects
# are indeed distinct:
print(a is b)
#     False
