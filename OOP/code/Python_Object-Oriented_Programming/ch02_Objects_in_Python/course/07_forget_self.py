# Purpose: study what happens when we forget `self` in a method's header
# Reference: page 47 (paper) / 68 (ebook)


class Point:
    # we purposefully omit `self` to see what will happen
    #         ✘
    #         v
    def reset():
        self.x = 0
        self.y = 0
p = Point()
p.reset()
#     TypeError: reset() takes 0 positional arguments but 1 was given
#
# We get an error which is expected.
# Although, the message could be more helpful:
#
#     missing self argument in method
