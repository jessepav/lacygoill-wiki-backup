# Purpose: Do  the following  to create  a program  that simulates  how websites
# ensure that everyone has a unique username.
#
#    - Make a list of five or more usernames called `current_users`.
#
#    - Make another list of five usernames called `new_users`.  Make sure one
#      or two of the new usernames are also in the `current_users` list.
#
#    - Loop through the `new_users` list to see if each new username has
#      already been used.  If it has, print a message that the person will need
#      to enter a new username.  If a username has not been used, print
#      a message saying that the username is available.
#
#    - Make sure your comparison is case insensitive.  If 'John' has been used,
#      'JOHN' should not be accepted.  To do this, you'll need to make a copy
#      of `current_users` containing the lowercase versions of all existing
#      users.

# Reference: page 89 (paper) / 127 (ebook)

current_users = ['john', 'Paul', 'george', 'RINGO', 'vincent']
new_users = ['mark', 'paul', 'janice', 'ringo', 'saul']

current_users_insensitive = []
for user in current_users:
    current_users_insensitive.append(user.lower())

for new_user in new_users:
    if new_user.lower() in current_users_insensitive:
        print(f'Sorry, {new_user.lower()} is already taken.  Choose a different username.')
    else:
        print(f'{new_user} is available.')
#     mark is available.
#     Sorry, paul is already taken.  Choose a different username.
#     janice is available.
#     Sorry, ringo is already taken.  Choose a different username.
#     saul is available.
