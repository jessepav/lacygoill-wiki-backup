# Purpose: Write  a loop  that  prompts the  user  to enter  a  series of  pizza
# toppings until they enter a 'quit' value.  As they enter each topping, print a
# message saying you'll add that topping to their pizza.

# Reference: page 123 (paper) / 161 (ebook)

active = True
while active:
    topping = input(
        '\nPlease enter a topping which you want on your pizza:'
        "\n(Enter 'quit' when you are finished.) "
    )
    if topping == 'quit':
        active = False
    else:
        print(f"We'll add {topping} on your pizza.")
#     Please enter a topping which you want on your pizza:
#     (Enter 'quit' when you are finished.) mushrooms
#     We'll add mushrooms on your pizza.
#
#     Please enter a topping which you want on your pizza:
#     (Enter 'quit' when you are finished.) pepperoni
#     We'll add pepperoni on your pizza.
#
#     Please enter a topping which you want on your pizza:
#     (Enter 'quit' when you are finished.) quit
