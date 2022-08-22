# Purpose: Modify  the  `make_shirt()` function  so  that  shirts are  large  by
# default with a message  that reads "I love Python".  Make a  large shirt and a
# medium  shirt with  the  default message,  and  a  shirt of  any  size with  a
# different message.

# Reference: page 137 (paper) / 175 (ebook)

def make_shirt(size='large', msg='I love Python'):
    print(f"The shirt's size is {size}, and \"{msg}\" is printed on it.")

make_shirt()
make_shirt('medium', 'Hello world!')
#     The shirt's size is large, and "I love Python" is printed on it.
#     The shirt's size is medium, and "Hello world!" is printed on it.
