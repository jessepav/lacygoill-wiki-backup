# Purpose: add behaviors to a simple class
# Reference: page 45 (paper) / 66 (ebook)


# create a class
class Point:
    # Add the `reset()` method.
    # Notice that the syntax is identical to a regular function.
    def reset(self):
    #         ^--^
    #         instance variable
    #
    # `self` is a reference to the object that the method is being invoked on.
        self.x = 0
        self.y = 0

p = Point()
p.reset()
# ------^
# No need  to pass `p`  to `reset()`, even though  the latter method  is defined
# with the `self` parameter in its header.  Python does it automatically for us.
# This is equivalent to:
#
#     Point.reset(p)

print(p.x, p.y)
#     0 0
