# Purpose: work with specialized container data types from the `collections` module
# Reference: page 111

# namedtuple {{{1

# If we need to work on the vision  of patients in a hospital, it makes sense to
# store measurements in tuples  with 2 numbers; one for the  left eye, the other
# for the right one:
vision = (9.5, 8.8)
print(vision)
print(vision[0])
print(vision[1])
#     (9.5, 8.8)
#     9.5
#     8.8

# Now, suppose we later  want to enhance this data by  including some number for
# the combined vision in  the middle of the tuple.  As  a result, `vision[1]` no
# longer pertains  to the right eye,  and we need to  refactor every `vision[1]`
# into `vision[2]`, which can be painful.
# We  could  have avoided  this  pitfall  if we  had  implemented  our data  via
# namedtuples instead of regular tuples.  Because in that case, the measurements
# could be referred to with names like `vision.left` and `vision.right`, instead
# of positions:
from collections import namedtuple
Vision = namedtuple('Vision', ['left', 'right'])
vision = Vision(9.5, 8.8)
print(vision)
print(vision.left)
print(vision.right)
#     Vision(left=9.5, right=8.8)
#     9.5
#     8.8

# Now, if we need to include a number  for the combined vision in the middle, we
# don't need to also refactor  every `vision[1]` into `vision[2]`, provided that
# we referred to the numbers (fields) via their names (attributes):
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

# defaultdict {{{1

d = {}

d['age'] = d.get('age', 0) + 1
print(d)
#     {'age': 1}

d = {'age': 39}
d['age'] = d.get('age', 0) + 1
print(d)
#     {'age': 40}

from collections import defaultdict
dd = defaultdict(int)
dd['age'] += 1
print(dd)
#     defaultdict(<class 'int'>, {'age': 1})
