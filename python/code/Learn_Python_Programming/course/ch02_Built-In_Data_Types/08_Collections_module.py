# Purpose: work with specialized container data types from the `collections` module
# Reference: page 111

# namedtuple {{{1

# If we need to work on the vision  of patients in a hospital, it makes sense to
# store data in tuples  with 2 numbers; one for the left eye,  the other for the
# right one:
vision = (9.5, 8.8)
print(vision)
print(vision[0])
print(vision[1])
#     (9.5, 8.8)
#     9.5
#     8.8

# Now, suppose we later  want to enhance this data by  including some number for
# the combined vision in  the middle of the tuple.  As  a result, `vision[1]` is
# no longer  an information  for the  left eye,  and we  need to  refactor every
# `vision[1]` into `vision[2]`, which can be painful.
# We  could  have avoided  this  pitfall  if we  had  implemented  our data  via
# namedtuples  instead of  regular tuples.   Because in  that case,  the numbers
# could be accessed  by names like `vision.left` and  `vision.right`, instead of
# by positions:
from collections import namedtuple
Vision = namedtuple('Vision', ['left', 'right'])
vision = Vision(9.5, 8.8)
print(vision)
print(vision.left)
print(vision.right)
#     Vision(left=9.5, right=8.8)
#     9.5
#     8.8

# If we now need  to include a number for the combined vision  in the middle, we
# don't also need to refactor  every `vision[1]` into `vision[2]`, provided that
# we accessed the numbers (fields) via their names (attributes):

#                                      v--------v
Vision = namedtuple('Vision', ['left', 'combined', 'right'])
#                    vvv
vision = Vision(9.5, 9.2, 8.8)
print(vision)
print(vision.left)
print(vision.combined)
print(vision.right)
#     Vision(left=9.5, combined=9.2, right=8.8)
#     9.5
#     9.2
#     8.8
