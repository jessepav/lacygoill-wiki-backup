# Purpose: Make a dictionary called `favorite_places`.   Think of three names to
# use as keys in the dictionary, and store one to three favorite places for each
# person.  Loop through  the dictionary, and print each person's  name and their
# favorite places.

# Reference: page 112 (paper) / 150 (ebook)

favorite_places = {
    'john': 'berlin',
    'alice': 'hong kong',
    'bob': 'new york',
}

for name, place in favorite_places.items():
    print(f"{name.title()}'s favorite place is {place.title()}.")
#     John's favorite place is Berlin.
#     Alice's favorite place is Hong Kong.
#     Bob's favorite place is New York.
