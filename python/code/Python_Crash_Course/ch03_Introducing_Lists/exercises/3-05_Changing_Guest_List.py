# Purpose: You just heard that  one of your guests can't come  to dinner, so you
# need to send  out a new set  of invitations.  You'll have to  think of someone
# else to invite.
#
#    - Start with your program from Exercise 3-4.  Add a `print()` call at the
#      end of your program stating the name of the guest who can't make it.
#
#    - Modify your list, replacing the name of the guest who can't make it with
#      the name of the new person you are inviting.
#
#    - Print a second set of invitation messages, one for each person who is
#      still in your list.

# Reference: page 42 (paper) / 80 (ebook)

# program from Exercise 3-4
guests = ['Liu Cixin', 'Veritasium', 'Jodie Foster']
print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')
#     Hello Liu Cixin, would you like to come to dinner?
#     Hello Veritasium, would you like to come to dinner?
#     Hello Jodie Foster, would you like to come to dinner?

# modify list of guests
print("\nVeritasium can't come to dinner\n")
#     Veritasium can't come to dinner
guests.remove('Veritasium')
guests.insert(1, 'Jon Stewart')

# print 2nd set of invitation messages
print(f'Hello {guests[0]}, would you like to come to dinner?')
print(f'Hello {guests[1]}, would you like to come to dinner?')
print(f'Hello {guests[2]}, would you like to come to dinner?')
#     Hello Liu Cixin, would you like to come to dinner?
#     Hello Jon Stewart, would you like to come to dinner?
#     Hello Jodie Foster, would you like to come to dinner?
