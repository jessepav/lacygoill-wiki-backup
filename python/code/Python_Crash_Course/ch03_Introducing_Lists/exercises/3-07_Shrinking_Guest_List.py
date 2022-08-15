# Purpose: You just  found out that your  new dinner table won't  arrive in time
# for the dinner, and you have space for only 2 guests.
#
#    - Start with your program from Exercise 3-6.  Add a new line that prints
#      a message saying that you can invite only 2 people for dinner.
#
#    - Use `pop()` to remove guests from your list one at a time until only
#      2 names remain in your list.  Each time you pop a name from your list,
#      print a message to that person letting them know you're sorry you can't
#      invite them to dinner.
#
#    - Print a message to each of the 2 people still on your list, letting them
#      know they're still invited.
#
#    - Use `del` to remove the last 2 names from your list, so you have an
#      empty list.  Print your list to make sure you actually have an empty
#      list at the end of your program.

# Reference: page 43 (paper) / 81 (ebook)

# program from Exercise 3-6
guests = ['Liu Cixin', 'Veritasium', 'Jodie Foster']
print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')

print()

print(f"Sorry {guests[0]}, the dinner's location has changed.")
print(f"Sorry {guests[1]}, the dinner's location has changed.")
print(f"Sorry {guests[2]}, the dinner's location has changed.")
guests.insert(0, 'Jon Stewart')
guests.insert(2, 'Richard Feynman')
guests.append('Forest Whitaker')

print()

print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')
print(f'Hello {guests[3]}, would you like to come to dinner?')
print(f'Hello {guests[4]}, would you like to come to dinner?')
print(f'Hello {guests[5]}, would you like to come to dinner?')

print('\nWe can only invite 2 people for dinner.\n')
guests.pop()
guests.pop(0)
guests.pop(0)
guests.pop(0)
print(f"Hello {guests[0]}, you're still invited.")
print(f"Hello {guests[1]}, you're still invited.")
#     Hello Veritasium, you're still invited.
#     Hello Jodie Foster, you're still invited.

# remove the last 2 guests from the list
del guests[0]
del guests[0]
print()
print(guests)
#     []
