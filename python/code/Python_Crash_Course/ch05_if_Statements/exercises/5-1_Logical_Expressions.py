# Purpose: Write a series of logical  expressions.  Print a statement describing
# each expression and your prediction for its evaluation.  Your code should look
# something like this:
#
#     car = 'subaru'
#     print("Is car == 'subaru'?  I predict True.")
#     print(car == 'subaru')
#
#     print("\nIs car == 'audi'?  I predict False.")
#     print(car == 'audi')
#
# - Look  closely at  your results,  and make  sure you  understand why  each
#   line evaluates to `True` or `False`.
#
# - Create at least ten tests.  Have at least five tests evaluate to `True` and
#   another five tests evaluate to `False`.

# Reference: page 78 (paper) / 116 (ebook)

# equality {{{1

food = 'pizza'
print("Is food == 'pizza'?  I predict True.")
print(food == 'pizza')
#     True

print("\nIs food != 'pizza'?  I predict False.")
print(food != 'pizza')
#     False

# relational {{{1

n = 42
print("\nIs n < 42?  I predict False.")
print(n < 42)
#     False

print("\nIs n <= 42?  I predict True.")
print(n <= 42)
#     True

n = 123
print("\nIs n > 123?  I predict False.")
print(n < 123)
#     False

print("\nIs n >= 123?  I predict True.")
print(n >= 123)
#     True

# logical {{{1

print("\nIs 100 < n and n < 200?  I predict True.")
print(100 < n and n < 200)
#     True

print("\nIs n > 200 or n < 100?  I predict False.")
print(n > 200 or n < 100)
#     False

# membership {{{1

names = ['John', 'Paul', 'George', 'Ringo']
print("\nIs 'Paul' in names?  I predict True.")
print('Paul' in names)
#     True

print("\nIs 'George' in names?  I predict False.")
print('George' not in names)
#     False
