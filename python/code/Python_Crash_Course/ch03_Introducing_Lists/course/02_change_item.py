# Purpose: change an item from a list
# Reference: page 38 (paper) / 76 (ebook)

# The `list[index]` syntax  which you can use  to *get* a list item  can also be
# used on the LHS of an assignment to *change* a list item.
motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)
#     ['honda', 'yamaha', 'suzuki']
#       ^---^

motorcycles[0] = 'ducati'
print(motorcycles)
#     ['ducati', 'yamaha', 'suzuki']
#       ^----^
