# Purpose: Make a  list called `sandwich_orders` and  fill it with the  names of
# various  sandwiches.  Then  make an  empty list  called `finished_sandwiches`.
# Loop through the list  of sandwich orders and print a  message for each order,
# such as "I made your tuna sandwich".  As each sandwich is made, move it to the
# list of finished sandwiches.  After all the sandwiches have been made, print a
# message listing each sandwich that was made.

# Reference: page 127 (paper) / 165 (ebook)

sandwich_orders = ['chicken', 'egg', 'ham']
finished_sandwiches = []

while sandwich_orders:
    order = sandwich_orders.pop()
    finished_sandwiches.append(order)
    print(f'I made your {order} sandwich.')

print('\nThese sandwiches were made:')
for sandwich in finished_sandwiches:
    print(f'\t{sandwich}')
#     I made your ham sandwich.
#     I made your egg sandwich.
#     I made your chicken sandwich.
#
#     These sandwiches were made:
#             ham
#             egg
#             chicken
