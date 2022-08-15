# Purpose: use type hints to get type checking
# Reference: page 41 (paper) / 62 (ebook)


#        2 type hints
#        v---v  v-----v
def odd(n: int) -> bool:
    return n % 2 != 0
# You can  attach a  type hint  to a  variable or  function parameter  using the
# syntax `: type`.  And do  the same for a value returned  from a function using
# `-> type`.

print(odd('Hello, world!'))
# Thanks to the previous type hints, we can get an error before even running the code.
# First, install mypy:
#
#     $ python -m pip install --user --upgrade mypy
#
# Then, use it:
#
#     $ mypy --strict code/Python_Object-Oriented_Programming/ch02_Objects_in_Python/course/03_type_hints.py
#     Argument 1 to "odd" has incompatible type "str"; expected "int"
