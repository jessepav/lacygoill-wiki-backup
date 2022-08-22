# Purpose: Write different versions of either  Exercise 7-4 or Exercise 7-5 that
# do each of the following at least once:
#
#    - Use a logical expression in the `while` statement to stop the loop.
#    - Use an `active` variable to control how long the loop runs.
#    - Use a `break` statement to exit the loop when the user enters a 'quit' value.

# Reference: page 123 (paper) / 161 (ebook)

# Let's use Exercise 7-5.
# It was already using a `break` statement to exit the loop.
# Let's re-write it so that it uses a logical expression inside the `while` statement instead. {{{1

age = ''

while age != 'quit':
    age = input(
        '\nPlease enter your age:'
        "\n(Enter 'quit' when you are finished.) "
    )

    if age != 'quit':
        age = int(age)

        if age < 3:
            price = 0
        elif age < 12:
            price = 10
        else:
            price = 15

        print(f'The cost of your movie ticket is ${price}.')

# Next, let's re-write it so that it uses an `active` variable. {{{1

active = True

while active:
    age = input(
        '\nPlease enter your age:'
        "\n(Enter 'quit' when you are finished.) "
    )

    if age == 'quit':
        active = False
    else:
        age = int(age)

        if age < 3:
            price = 0
        elif age < 12:
            price = 10
        else:
            price = 15

        print(f'The cost of your movie ticket is ${price}.')
