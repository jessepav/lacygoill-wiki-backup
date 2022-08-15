# Purpose: add attributes to a simple class
# Reference: page 44 (paper) / 65 (ebook)


# create an empty class (this time we name it `Point`)
class Point:
    pass

# create 2 instances of `Point`
p1 = Point()
p2 = Point()

# assign each of these instances `x` and  `y` coordinates to identify a point in
# a 2-dimensional space, using the dot notation
# v
p1.x = 5
p1.y = 4
# ^
#
# It works, but don't do that.
# There is a better way, which we'll see later.

p2.x = 3
p2.y = 6

# print the attribute values of the 2 instances
print(p1.x, p1.y)
print(p2.x, p2.y)
#     5 4
#     3 6
