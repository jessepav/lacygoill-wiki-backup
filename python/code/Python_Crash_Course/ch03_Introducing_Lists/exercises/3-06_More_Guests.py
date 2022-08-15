# Purpose: You just found a bigger dinner table, so now more space is available.
# Think of three more guests to invite to dinner.
#
#    - Start with your program from Exercise 3-4 or Exercise 3-5.  Add
#      a `print()`  call to the end  of your program informing  people that you
#      found a bigger dinner table.
#
#    - Use `insert()` to add 1 new guest to the beginning of your list.
#    - Use `insert()` to add 1 new guest to the middle of your list.
#    - Use `append()` to add 1 new guest to the end of your list.
#
#    - Print a new set of invitation messages, one for each person in your list.

# Reference: page 42 (paper) / 80 (ebook)

# program from Exercise 3-4
guests = ['Liu Cixin', 'Veritasium', 'Jodie Foster']
print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')

print()
print(f"Sorry {guests[0]}, the dinner's location has changed.")
print(f"Sorry {guests[1]}, the dinner's location has changed.")
print(f"Sorry {guests[2]}, the dinner's location has changed.")

# add 1 new guest to the beginning of our list
guests.insert(0, 'Jon Stewart')
# add 1 new guest to the middle of our list
guests.insert(2, 'Richard Feynman')
# add 1 new guest to the end of our list
guests.append('Forest Whitaker')

# print new set of invitation messages
print()
print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')
print(f'Hello {guests[3]}, would you like to come to dinner?')
print(f'Hello {guests[4]}, would you like to come to dinner?')
print(f'Hello {guests[5]}, would you like to come to dinner?')
#     Hello Jon Stewart, would you like to come to dinner?
#     Hello Liu Cixin, would you like to come to dinner?
#     Hello Richard Feynman, would you like to come to dinner?
#     Hello Veritasium, would you like to come to dinner?
#     Hello Jodie Foster, would you like to come to dinner?
#     Hello Forest Whitaker, would you like to come to dinner?
