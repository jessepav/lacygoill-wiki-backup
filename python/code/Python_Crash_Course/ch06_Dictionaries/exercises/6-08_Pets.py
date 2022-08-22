# Purpose: Make  several  dictionaries,  where   each  dictionary  represents  a
# different pet.  In each dictionary, include the kind of animal and the owner's
# name.  Store these  dictionaries in a list called `pets`.   Next, loop through
# your list and as you do, print everything you know about each pet.

# Reference: page 112 (paper) / 150 (ebook)

pet1 = {
    'name': 'kovu',
    'kind': 'cat',
    'owner': 'john',
}

pet2 = {
    'name': 'ginger',
    'kind': 'dog',
    'owner': 'alice',
}

pet3 = {
    'name': 'milo',
    'kind': 'bird',
    'owner': 'bob',
}

pets = [pet1, pet2, pet3]

for pet in pets:
    owner = pet["owner"].title()
    name = pet["name"].title()
    print(f'{owner} has a {pet["kind"]} named {name}.')
#     John has a cat named Kovu.
#     Alice has a dog named Ginger.
#     Bob has a bird named Milo.
