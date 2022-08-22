# Purpose: write nested lists/dictionaries
# Reference: page 106 (paper) / 144 (ebook)

# You can nest dictionaries inside a list. {{{1

alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0, alien_1, alien_2]
#         ^-----^  ^-----^  ^-----^
#
# When a composite data structure (such as the `alien_*` dictionaries) is inside
# another composite data structure (such as the `aliens` list), we say that it's
# *nested*.   Here,  `alien_0`,  `alien_1`,  and  `alien_2`  are  nested  inside
# `aliens`.

for alien in aliens:
    print(alien)
#     {'color': 'green', 'points': 5}
#     {'color': 'yellow', 'points': 10}
#     {'color': 'red', 'points': 15}

# You can nest lists inside a dictionary. {{{1

# Store information about a pizza being ordered.
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
    #           ^---------------------------^
}

# Summarize the order.
print(f"You ordered a {pizza['crust']}-crust pizza "
    "with the following toppings:")
# Inside parentheses, consecutive strings are implicitly concatenated.

#              v---------------v
for topping in pizza['toppings']:
    print("\t" + topping)
#     You ordered a thick-crust pizza with the following toppings:
#             mushrooms
#             extra cheese
#
# Without parentheses, the `+` operator can be used to concatenate strings.

# You can nest dictionaries inside a dictionary. {{{1

users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton',
    },
    'mcurie': {
        'first': 'marie',
        'last': 'curie',
        'location': 'paris',
    },
}

for username, user_info in users.items():
    print(f'\nUsername: {username}')

    full_name = f'{user_info["first"]} {user_info["last"]}'
    location = f'{user_info["location"].title()}'

    print(f'\tFull name: {full_name.title()}')
    print(f'\tLocation: {location}')

#     Username: aeinstein
#             Full name: Albert Einstein
#             Location: Princeton
#
#     Username: mcurie
#             Full name: Marie Curie
#             Location: Paris

# Parsing nested data often requires a nested `for` loop. {{{1
# One to iterate over  the items of the outer structure,  and another to iterate
# over the items inside the nested structure.

favorite_languages = {
    'jen': ['python', 'ruby'],
    #      ^----------------^
    'sarah': ['c'],
    #        ^---^
    'edward': ['ruby', 'go'],
    #         ^------------^
    'phil': ['python', 'haskell'],
    #       ^-------------------^
}

# outer loop
# v
for name, languages in favorite_languages.items():
    if len(languages) == 1:
        print(f"\n{name.title()}'s favorite language is {languages[0].title()}.")
    else:
        print(f"\n{name.title()}'s favorite languages are:")
        # inner loop
        # v
        for language in languages:
        #               ^-------^
            print(f'\t{language.title()}')
#     Jen's favorite languages are:
#             Python
#             Ruby
#
#     Sarah's favorite language is C.
#
#     Edward's favorite languages are:
#             Ruby
#             Go
#
#     Phil's favorite languages are:
#             Python
#             Haskell

# Nested data structures are handy when trying to model a list of entities with the same characteristics. {{{1
# For example, suppose we want to model a fleet of aliens in a game.

# Make an empty list for storing aliens.
aliens = []

# Make 30 green aliens.
for _ in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    # Even though all  the generated aliens have the  same characteristics, they
    # are distinct objects, which we will be able to alter independently later.
    aliens.append(new_alien)
    # `new_alien` is now nested inside `aliens`

for alien in aliens[:3]:
    # This test is useless for now, but it might become necessary in the future.{{{
    #
    # In  a  real  game,  the  state  of  the  fleet  could  change  in  various
    # circumstances.  Some  aliens might change  color over time, in  which case
    # there is no guarantee that all aliens are green anymore.
    #}}}
    # let's make green aliens a little faster
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['speed'] = 'medium'
        alien['points'] = 10

    # same thing for yellow aliens
    elif alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = 'fast'
        alien['points'] = 15

# Show the first 5 aliens.
for alien in aliens[:5]:
    print(alien)
print('...')

# Show how many aliens have been created.
print(f'Total number of aliens: {len(aliens)}')
#     {'color': 'yellow', 'points': 10, 'speed': 'medium'}
#     {'color': 'yellow', 'points': 10, 'speed': 'medium'}
#     {'color': 'yellow', 'points': 10, 'speed': 'medium'}
#     {'color': 'green', 'points': 5, 'speed': 'slow'}
#     {'color': 'green', 'points': 5, 'speed': 'slow'}
#     ...
#     Total number of aliens: 30
