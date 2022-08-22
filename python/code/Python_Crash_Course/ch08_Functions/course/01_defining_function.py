# Purpose: define a function
# Reference: page 130 (paper) / 168 (ebook)

# Let's define a simple function. {{{1

# function definition
def greet_user():
# function body

    # docstring
    """Display a simple greeting."""

    print('Hello!')

# function call
greet_user()
#     Hello!
# Let's define a function expecting an argument. {{{1

#              parameter
#              v------v
def greet_user(username):
    """Display a simple greeting."""
    print(f'Hello {username.title()}!')

#          argument
#          v-----v
greet_user('jesse')
greet_user('sarah')
#     Hello Jesse!
#     Hello Sarah!

