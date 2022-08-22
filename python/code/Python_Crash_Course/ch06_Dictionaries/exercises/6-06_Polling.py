# Purpose: Use the code in the course which sets the `favorite_languages` dictionary.
#
#    - Make a list of people who should take the favorite languages poll.
#      Include some names that are already in the dictionary and some that are
#      not.
#
#    - Loop through the list of people who should take the poll.  If they have
#      already taken the poll, print a message thanking them for responding.
#      If they have not yet taken the poll, print a message inviting them to
#      take the poll.

# Reference: page 105 (paper) / 143 (ebook)

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

participants = ['john', 'sarah', 'paul', 'phil']

for participant in participants:
    if participant in favorite_languages:
        print(f'Thank you for taking the poll, {participant.title()}.')
    else:
        print(f"You're invited to take a poll, {participant.title()}.")
#     You're invited to take a poll, John.
#     Thank you for taking the poll, Sarah.
#     You're invited to take a poll, Paul.
#     Thank you for taking the poll, Phil.
