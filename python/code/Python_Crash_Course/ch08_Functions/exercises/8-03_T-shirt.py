# Purpose: Write a  function called `make_shirt()`  that accepts a size  and the
# text of a  message that should be  printed on the shirt.   The function should
# print a sentence summarizing the size of  the shirt and the message printed on
# it.
#
# Call the function  once using positional arguments to make  a shirt.  Call the
# function a second time using keyword arguments.

# Reference: page 137 (paper) / 175 (ebook)

def make_shirt(size, msg):
    print(f"The shirt's size is {size}, and \"{msg}\" is printed on it.")

make_shirt('medium', 'Hello world!')
make_shirt(msg='Hello world!', size='medium')
#     The shirt's size is medium, and "Hello world!" is printed on it.
#     The shirt's size is medium, and "Hello world!" is printed on it.
