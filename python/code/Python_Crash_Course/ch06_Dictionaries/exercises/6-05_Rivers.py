# Purpose: Make a dictionary containing three majors rivers and the country each
# river runs through.  One key-value pair might be `'nile': 'egypt'`.
#
#    - Use a loop to print a sentence about each river, such as "The Nile runs
#      through Egypt.".
#
#    - Use a loop to print the name of each river included in the dictionary
#    - Use a loop to print the name of each country included in the dictionary

# Reference: page 105 (paper) / 143 (ebook)

rivers = {
    'nile': 'egypt',
    'amazon': 'peru',
    'mississippi': 'usa',
}

for river, country in rivers.items():
    if country == 'usa':
        print(f'The {river.title()} runs through {country.upper()}.')
    else:
        print(f'The {river.title()} runs through {country.title()}.')
#     The Nile runs through Egypt.
#     The Amazon runs through Peru.
#     The Mississippi runs through USA.

for river in rivers:
    print(river)
#     nile
#     amazon
#     mississippi

for country in rivers.values():
    print(country)
#     egypt
#     peru
#     usa
