# Purpose: use functions which return values
# Reference: page 137 (paper) / 175 (ebook)

# A function might return a value. {{{1

# Such a  function is  helpful to  make the  code more  readable by  hiding some
# computation behind a telling name.
#
# It contains a `return` statement which  defines what value should be returned;
# this value is also called the "output" of the function.
# The `return` statement has 2 effects:
#
#    - it makes the execution quit the function
#    - it replaces any call to the function with its argument value
#
# Usually, it has no side effect.

def get_formatted_name(first_name, last_name):
    """Return a full name, neatly formatted."""
    full_name = f'{first_name} {last_name}'
    return full_name.title()
    # ---^
    #
    # The `return` statement is responsible for returning an arbitrary value.

musician = get_formatted_name('jimi', 'hendrix')
print(musician)
#     Jimi Hendrix

#   Any kind of value; even more complex data structures such as lists and dictionaries. {{{1

def build_person(first_name, last_name, age=None):
    """Return a dictionary of information about a person."""
    #        v--------------------------------------v
    person = {'first': first_name, 'last': last_name}

    # augment the dictionary with the age, if one was passed to the function
    if age:
        person['age'] = age

    return person

musician = build_person('jimi', 'hendrix', age=27)
print(musician)
#     {'first': 'jimi', 'last': 'hendrix', 'age': 27}
# }}}1

# A function can be called inside any control flow block. {{{1

# As an example, let's call a function inside a `while` loop.

def get_formatted_name(first_name, last_name):
    """Return a full name, neatly formatted."""
    full_name = f'{first_name} {last_name}'
    return full_name.title()

# --v
while True:
    print('\nPlease tell me your name:')
    print("(enter 'q' at any time to quit)")

    f_name = input('First name: ')
    if f_name == 'q':
        break

    l_name = input('Last name: ')
    if l_name == 'q':
        break

    #                v----------------v
    formatted_name = get_formatted_name(f_name, l_name)
    print(f'\nHello, {formatted_name}!')
#     Please tell me your name:
#     (enter 'q' at any time to quit)
#     First name: eric
#     Last name: matthes
#
#     Hello, Eric Matthes!
#
#     Please tell me your name:
#     (enter 'q' at any time to quit)
#     First name: q
