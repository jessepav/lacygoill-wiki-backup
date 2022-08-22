# Purpose: A Python dictionary can be used to model an actual dictionary.
# However, to avoid confusion, let's call it a glossary.
#
#    - Think of five programming words you've learned about in the previous
#      chapters.  Use these words as the keys in your glossary, and store their
#      meanings as values.
#
#    - Print each word and its meaning as neatly formatted output.  You might
#      print the word followed by a colon and then its meaning, or print the
#      word on one line and then print its meaning indented on a second line.
#      Use the newline character (`\n`) to insert a blank line between each
#      word-meaning pair in your output.

# Reference: page 99 (paper) / 137 (ebook)

glossary = {
    'CapWords': 'synonym for CamelCase',
    'None': 'keyword used to define a null value, or no value at all',
    'PEP': 'Python Enhancement Proposal',
    'logical error': 'error in the logic of the code',
    'tuple': 'immutable list',
}

print(f"Capwords: {glossary['CapWords']}\n")
print(f"None: {glossary['None']}\n")
print(f"PEP: {glossary['PEP']}\n")
print(f"logical error: {glossary['logical error']}\n")
print(f"tuple: {glossary['tuple']}")
#     Capwords: synonym for CamelCase
#
#     None: keyword used to define a null value, or no value at all
#
#     PEP: Python Enhancement Proposal
#
#     logical error: error in the logic of the code
#
#     tuple: immutable list
