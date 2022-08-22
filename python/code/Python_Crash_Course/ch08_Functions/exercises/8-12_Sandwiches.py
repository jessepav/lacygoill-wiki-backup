# Purpose: Write a  function that accepts  a list of items  a person wants  on a
# sandwich.  The function should have one  parameter that collects as many items
# as the function call  provides, and it should print a  summary of the sandwich
# that's being ordered.  Call the function three times, using a different number
# of arguments each time.

# Reference: page 150 (paper) / 188 (ebook)

def make_sandwich(*items):
    """Print the list of items that have been requested."""
    print(items)

make_sandwich('turkey')
make_sandwich('tuna', 'vegetables')
make_sandwich('hard-boiled egg', 'cheese', 'chicken')
#     ('turkey',)
#     ('tuna', 'vegetables')
#     ('hard-boiled egg', 'cheese', 'chicken')
