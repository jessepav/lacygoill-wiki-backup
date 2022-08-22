# Purpose: Using the  list `sandwich_orders`  from Exercise  7-8, make  sure the
# sandwich 'pastrami' appears  in the list at least three  times.  Add code near
# the beginning of your  program to print a message saying the  deli has run out
# of  pastrami,  and  then  use  a  `while` loop  to  remove  all  instances  of
# 'pastrami' from `sandwich_orders`.  Make sure no pastrami sandwiches end up in
# `finished_sandwiches`.

# Reference: page 127 (paper) / 165 (ebook)

print('The deli has run out of pastrami.\n')

#                             v--------v         v--------v         v--------v
sandwich_orders = ['chicken', 'pastrami', 'egg', 'pastrami', 'ham', 'pastrami']
while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')
    #              ^-----^

finished_sandwiches = []

while sandwich_orders:
    order = sandwich_orders.pop()
    finished_sandwiches.append(order)
    print(f'I made your {order} sandwich.')

print('\nThese sandwiches were made:')
for sandwich in finished_sandwiches:
    print(f'\t{sandwich}')
#     The deli has run out of pastrami.
#
#     I made your ham sandwich.
#     I made your egg sandwich.
#     I made your chicken sandwich.
#
#     These sandwiches were made:
#             ham
#             egg
#             chicken
