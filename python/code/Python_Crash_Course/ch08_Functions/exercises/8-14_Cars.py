# Purpose: Write a function that stores information about a car in a dictionary.
# The function should always receive a manufacturer and a model name.  It should
# then accept an arbitrary number of  keyword arguments.  Call the function with
# the required information and two other name-value pairs, such as a color or an
# optional feature.  Your function should work for a call like this one:
#
#     car = make_car('subaru', 'outback', color='blue', tow_package=True)
#
# Print the  dictionary that's  returned to  make sure  all the  information was
# stored correctly.

# Reference: page 150 (paper) / 188 (ebook)

def make_car(manufacturer, model, **features):
    features['manufacturer'] = manufacturer
    features['model'] = model

    return features

car = make_car('subaru', 'outback', color='blue', tow_package=True)
print(car)
#     {'color': 'blue', 'tow_package': True, 'manufacturer': 'subaru', 'model': 'outback'}
#                                            ^------------------------------------------^
#
# Our function  has correctly  extended the  dictionary containing  the variadic
# keyword arguments with the first 2 positional arguments.
