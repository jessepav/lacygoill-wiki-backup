# Purpose: create and use a class
# Reference: page 158 (paper) / 196 (ebook)

# We define a `Dog` class, using the `class` statement.
class Dog:
    """A simple attempt to model a dog."""

    # Any function defined in a class is a *method*.{{{
    #
    # It's meant to be invoked on an object instantiated from the class.
    #}}}
    # The `__init__`  method is special.{{{
    #
    # It's  called  automatically  whenever  we   create  a  new  instance  (aka
    # instantiate) based on the `Dog` class.
    #}}}
    # The `self` parameter is also special.{{{
    #
    # Any time  you call a method  on an object,  a reference to that  object is
    # automatically  passed to  the  method  as a  first  argument.  The  `self`
    # parameter is necessary to be assigned that argument.
    #
    # Inside any method, the `self` variable  lets you access all attributes and
    # methods of the object on which the method is being invoked.
    #
    # The name "self" is not special.  You could use any other name.
    # However, "self" is used by convention (which is codified in PEP 8).
    #}}}
    def __init__(self, name, age):
        """Initialize name and age attributes."""
        # We add 2 attributes `name` and `age` to any `Dog` object.{{{
        #
        # And we  assign them whatever values  will be passed to  the class when
        # instantiating an object.
        #
        # Attributes help identify an instance of  a class, out of all the other
        # instances of  that class.  Although  not uniquely; 2 objects  can have
        # the same attributes.  For example, you could have 2 dogs with the same
        # name and the same age.
        #
        # Attributes are  attached to an  object, and  any method invoked  on an
        # object can access  all of its attributes.  Here, by  adding `name` and
        # `age` to  the object's attributes, we  make sure that the  `sit()` and
        # `roll_over()` method will have access to those values whenever we call
        # them, without having to pass the values explicitly.
        #}}}
        self.name = name
        self.age = age

    # we define another method
    def sit(self):
        """Simulate a dog sitting in response to a command."""
        print(f'{self.name} is now sitting.')

    # and yet another method
    def roll_over(self):
        """Simulate rolling over in response to a command."""
        print(f'{self.name} rolled over!')


# We're not calling the `Dog()` function; we're instantiating an object from the `Dog` class.{{{
#
# Which we assign to the `my_dog` variable.
#
# ---
#
# Even though  `self` must be  declared explicitly in  the header of  a function
# defined inside a class, no argument must  be written explicitly for it when we
# call one of  its methods explicitly, nor when we  instantiate an object (which
# calls  the `__init__()`  method implicitly);  the object  reference is  passed
# implicitly.
#}}}
#        v--v
my_dog = Dog('Willie', 6)
#            ^------^  ^
# We need to pass 2 arguments: the name of the dog, and its age.{{{
#
# They're expected by the `__init__()` function:
#
#     def __init__(self, name, age):
#                        ^--^  ^^^
#}}}

# `my_dog` is an object with the `name` and `age` attributes.{{{
#
# Because that's how we named them in `__init__()`:
#
#     self.name = name
#          ^--^
#
#     self.age = age
#          ^^^
#}}}
# We  can  refer  to  the  attribute  of  an  object  using  the  dot  notation:
# `object.attribute`.  We  use this syntax  here, to  print a message  about the
# name and the age of the dog object that we've just instantiated.
print(f"My dog's name is {my_dog.name}.")
print(f"My dog is {my_dog.age} years old.")
#     My dog's name is Willie.
#     My dog is 6 years old.
