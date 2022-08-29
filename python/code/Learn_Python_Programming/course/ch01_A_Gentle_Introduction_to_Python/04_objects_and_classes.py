# Purpose: show how classes can create objects
# Reference: page 62

# Definition {{{1

# A class definition starts with a `class` statement:
class Bike:
    # Now we're inside the body of the class.

    # We define a method.
    # That's how we refer to a function when it's defined inside a class body.
    # `__init__()` is a special method, called an **initializer**.{{{
    #
    # When we'll  call `Bike()` to  instantiate an object, `__init__()`  will be
    # called automatically.  It's  meant to set the object  attributes.  Here we
    # set the `color` and `frame_material` attributes.
    #}}}
    def __init__(self, color, frame_material):
        self.color = color
        self.frame_material = frame_material

    def brake(self):
        # that's the line of the class definition
        print('Braking!')

# Instantiation {{{1

# Instantiate a `red_bike` object and a `blue_bike` object:
red_bike = Bike('Red', 'Carbon fiber')
blue_bike = Bike('Blue', 'Steel')

# Instances of a given class are objects whose type is that class:
print(type(red_bike))
print(type(blue_bike))
#     <class '__main__.Bike'>
#     <class '__main__.Bike'>

# Printing attributes {{{1

# Print some characteristics of those objects:
print(red_bike.color)
print(red_bike.frame_material)
print(blue_bike.color)
print(blue_bike.frame_material)
#     Red
#     Carbon fiber
#     Blue
#     Steel

# Calling methods {{{1

# Make the `red_bike` do something:
red_bike.brake()
#     Braking!
