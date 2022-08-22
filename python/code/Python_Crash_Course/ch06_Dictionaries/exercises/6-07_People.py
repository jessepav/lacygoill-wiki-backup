# Purpose: Start with  the program  you wrote  for Exercise  6-1.  Make  two new
# dictionaries representing  different people, and store  all three dictionaries
# in a  list called `people`.   Loop through your list  of people.  As  you loop
# through the list, print everything you know about each person.

# Reference: page 112 (paper) / 150 (ebook)

person1 = {
    'first name': 'john',
    'last name': 'doe',
    'age': 33,
    'city': 'new york',
}

person2 = {
    'first name': 'maysa',
    'last name': 'mercado',
    'age': 22,
    'city': 'berlin',
}

person3 = {
    'first name': 'heather',
    'last name': 'peel',
    'age': 44,
    'city': 'hong kong',
}

people = [person1, person2, person3]

for person in people:
    full_name = f'{person["first name"]} {person["last name"]}'
    print(f'\nFull name: {full_name.title()}')
    print(f'Age: {person["age"]}')
    print(f'City: {person["city"].title()}')
#     Full name: John Doe
#     Age: 33
#     City: New York
#
#     Full name: Maysa Mercado
#     Age: 22
#     City: Berlin
#
#     Full name: Heather Peel
#     Age: 44
#     City: Hong Kong
