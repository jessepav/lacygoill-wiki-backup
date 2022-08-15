# Purpose: pass explicit arguments to method
# Reference: page 48 (paper) / 69 (ebook)


import math

# define a `Point` class with 2 attributes (`x` and `y`), and 3 methods
class Point:
    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def reset(self) -> None:
        self.move(0, 0)

    def calculate_distance(self, other: 'Point') -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
        #      ^--------^
        #      computes the distance between between 2 points in a 2-dimensional space

point1 = Point()
point2 = Point()

point1.reset()
point2.move(5, 0)
print(point2.calculate_distance(point1))
#     5.0
#
# The distance between the two points is `5.0`.

# It doesn't  from which  point we call  the `calculate_distance()`  method; the
# result is the  same.  The contrary would  be problematic: there can  only be 1
# distance between 2 points.
assert point2.calculate_distance(point1) == \
       point1.calculate_distance(point2)
       # no error is raised

# after changing  the position of  the first point,  the distance to  the second
# point changes
point1.move(3, 4)
print(point1.calculate_distance(point2))
#     4.47213595499958

# the distance between a point and itself is always zero
#
#     v----v                    v----v
print(point1.calculate_distance(point1))
#     0.0
