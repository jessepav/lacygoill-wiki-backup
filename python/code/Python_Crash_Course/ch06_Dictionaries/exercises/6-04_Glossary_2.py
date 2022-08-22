# Purpose: Now that you know how to loop through a dictionary, clean up the code
# from Exercise 6-3 by replacing your series of `print()` calls with a loop that
# runs through  the dictionary's keys  and values.   When you're sure  that your
# loop works, add  five more Python terms  to your glossary.  When  you run your
# program again, these new words and meaning should automatically be included in
# the output.

# Reference: page 105 (paper) / 143 (ebook)

glossary = {
    'CapWords': 'synonym for CamelCase',
    'None': 'keyword used to define a null value, or no value at all',
    'PEP': 'Python Enhancement Proposal',
    'logical error': 'error in the logic of the code',
    'tuple': 'immutable list',
}

for word, definition in glossary.items():
    print(f'{word}: {definition}\n')
#     CapWords: Synonym for CamelCase.
#
#     None: Keyword used to define a null value, or no value at all.
#
#     PEP: Python Enhancement Proposal
#
#     logical error: Error in the logic of the code.
#
#     tuple: Immutable list.

# let's add 5 new words in our glossary
glossary['set'] = 'collection in which each item must be unique'
glossary['black'] = 'popular Python formatter'
glossary['pylint'] = 'popular Python linter'
glossary['mypy'] = 'static type checker for Python'
glossary['pudb'] = 'TUI front-end for the builtin Python debugger'

for word, definition in glossary.items():
    print(f'{word}: {definition}\n')
#     CapWords: synonym for CamelCase
#
#     None: keyword used to define a null value, or no value at all
#
#     PEP: Python Enhancement Proposal
#
#     logical error: error in the logic of the code
#
#     tuple: immutable list
#
#     set: collection in which each item must be unique
#
#     black: popular Python formatter
#
#     pylint: popular Python linter
#
#     mypy: static type checker for Python
#
#     pudb: TUI front-end for the builtin Python debugger
