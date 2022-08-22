# Purpose: A  movie  theater charges  different  ticket  prices depending  on  a
# person's age.  If a person is under the  age of 3, the ticket is free; if they
# are between 3 and  12, the ticket is $10; and if they  are over 12, the ticket
# is $15.  Write a loop in which you ask users their age, and then tell them the
# cost of their movie ticket.

# Reference: page 123 (paper) / 161 (ebook)

while True:
    age = input(
        '\nPlease enter your age:'
        "\n(Enter 'quit' when you are finished.) "
    )
    if age == 'quit':
        break
    age = int(age)

    if age < 3:
        price = 0
    elif age < 12:
        price = 10
    else:
        price = 15

    print(f'The cost of your movie ticket is ${price}.')
#     Please enter your age:
#     (Enter 'quit' when you are finished.) 1
#     The cost of your movie ticket is $0.
#
#     Please enter your age:
#     (Enter 'quit' when you are finished.) 11
#     The cost of your movie ticket is $10.
#
#     Please enter your age:
#     (Enter 'quit' when you are finished.) 22
#     The cost of your movie ticket is $15.
#
#     Please enter your age:
#     (Enter 'quit' when you are finished.) quit
