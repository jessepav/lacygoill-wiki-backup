# Purpose: Think of at least five places in the world you'd like to visit.{{{
#
#    - Store the locations in a list.  Make sure the list is not in
#      alphabetical order.  Print it in its original order.
#
#    - Use `sorted()` to print the list in alphabetical order without modifying
#      the actual list.  Print the list to show that it's still in its original
#      order by printing it.
#
#    - Repeat the previous step, but this time, reverse the alphabetical order.
#
#    - Use `reverse()` to change the order of the list.  Print the list to show
#      that its order has changed.
#
#    - Repeat the previous step.  Print the list to show it's back to its
#      original order.
#
#    - Use `sort()` to change the list so it's stored in alphabetical order.
#      Print the list to show that its order has changed.
#
#    - Repeat the previous step, but this time, reverse the alphabetical order.
#}}}
# Reference: page 46 (paper) / 84 (ebook)

locations = ['New York', 'Tokyo', 'London', 'Berlin', 'Hong Kong']
print(locations)

print(sorted(locations))
print(locations)
print(sorted(locations, reverse=True))
print(locations)
#     ['Berlin', 'Hong Kong', 'London', 'New York', 'Tokyo']
#     ['New York', 'Tokyo', 'London', 'Berlin', 'Hong Kong']
#     ['Tokyo', 'New York', 'London', 'Hong Kong', 'Berlin']
#     ['New York', 'Tokyo', 'London', 'Berlin', 'Hong Kong']

locations.reverse()
print(locations)
locations.reverse()
print(locations)
#     ['Hong Kong', 'Berlin', 'London', 'Tokyo', 'New York']
#     ['New York', 'Tokyo', 'London', 'Berlin', 'Hong Kong']

locations.sort()
print(locations)
locations.sort(reverse=True)
print(locations)
#     ['Berlin', 'Hong Kong', 'London', 'New York', 'Tokyo']
#     ['Tokyo', 'New York', 'London', 'Hong Kong', 'Berlin']
