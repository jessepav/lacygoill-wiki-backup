# Purpose: avoid common mistakes when writing a loop
# Reference: page 53 (paper) / 91 (ebook)

magicians = ['alice', 'david', 'carolina']

# The body of a loop must contain at least 1 statement. {{{1
for magician in magicians:
# This line is wrong.  It should be indented.
# Without indentation, it's not part of the loop's body; it's run afterward.
# But the loop's body needs this line; without it's empty.
# An empty loop is wrong and raises an error.
print(magician)
#       print(magician)
#       ^
#     IndentationError: expected an indented block
#
# To fix this error, indent the line:
#
#     for magician in magicians:
#         print(magician)
#     ^--^

# The indentation of a statement in the body of a `for` loop must be 1 more than the `for` statement itself. {{{1
for magician in magicians:
    print(f'{magician.title()}, that was a great trick!')
# Here we forgot to indent the line, which prevents it from being run inside the loop.
print(f"I can't wait to see your next trick, {magician.title()}.\n")
#     Alice, that was a great trick!
#     David, that was a great trick!
#     Carolina, that was a great trick!
#     I can't wait to see your next trick, Carolina.
#     ^--------------------------------------------^
# As a result, only the last magician gets this message.
#
# This is a *logical error*, not a syntax error.
# The syntax of the  whole script is valid, but it  doesn't produce the intended
# result.  That's why Python doesn't raise  any error here.  It can't guess what
# you expect, so it  has no way to determine if the  actual result is "correct".
# If you want an error to be raised  here, you need to write a test.  The latter
# can teach Python what result you expect from the code.
#
# ---
#
# Also, notice that `magician` is not local to the `for` block.
# It  remains visible  outside the  loop,  with the  value  it had  in the  last
# iteration.

# A statement must be indented only when necessary. {{{1

# For now, the only statements which need to be indented are the ones inside the
# body of a `for` loop.
message = 'Hello Python world!'
# For now, the only case where you need to indent a line, is inside a `for` loop.
# There is no loop here, so there is no reason to indent this line, hence why an
# error is raised.
# ✘
# vv
    print(message)
# IndentationError: unexpected indent

# A statement after a `for` loop must be *de*-indented. {{{1

for magician in magicians:
    print(f'{magician.title()}, that was a great trick!')
    print(f"I can't wait to wait to see your next trick, {magician.title()}.\n")

# This line should not be indented, because  the message is meant to be sent for
# the magicians  as a group.  Not  for every single magician.   By indenting the
# line, you move it inside the loop, causing it to be run during each iteration.
# This is again a logical error, not a syntax error.
#
# ✘
# vv
    print('Thank you everyone, that was a great magic show!')
#     Alice, that was a great trick!
#     I can't wait to wait to see your next trick, Alice.
#
#     Thank you everyone, that was a great magic show!
#     David, that was a great trick!
#     I can't wait to wait to see your next trick, David.
#
#     Thank you everyone, that was a great magic show!
#     Carolina, that was a great trick!
#     I can't wait to wait to see your next trick, Carolina.
#
#     Thank you everyone, that was a great magic show!

# A `for` statement must end with a colon. {{{1
#                        ✘
#                        v
for magician in magicians
    print(magician)
# SyntaxError: invalid syntax
