# Purpose: Make a dictionary called `cities`.  Use  the names of three cities as
# keys in your  dictionary.  Create a dictionary of information  about each city
# and include the  country that the city is in,  its approximate population, and
# one  fact about  the city.   The  keys for  each city's  dictionary should  be
# something like  `country`, `population`, and  `fact`.  Print the name  of each
# city and all of the information you have stored about it.

# Reference: page 112 (paper) / 150 (ebook)

cities = {
    'berlin': {
        'country': 'germany',
        'population': '3.645 million',
        'fact': 'The city became the capital of germany in 1871.',
    },
    'london': {
        'country': 'england',
        'population': '8.982 million',
        'fact': "More than 300 languages are spoken in the city.",
    },
    'madrid': {
        'country': 'spain',
        'population': '3.223 million',
        'fact': 'It was created around the year of 860 A.C.',
    },
}

for city, info in cities.items():
    print(f'\n{city.title()}:')
    print(f"\tIt's located in {info['country'].title()}.")
    print(f"\tIt has a population of {info['population']} inhabitants.")
    print(f"\t{info['fact']}")
#     Berlin:
#             It's located in Germany.
#             It has a population of 3.645 million inhabitants.
#             The city became the capital of germany in 1871.
#
#     London:
#             It's located in England.
#             It has a population of 8.982 million inhabitants.
#             More than 300 languages are spoken in the city.
#
#     Madrid:
#             It's located in Spain.
#             It has a population of 3.223 million inhabitants.
#             It was created around the year of 860 A.C.
