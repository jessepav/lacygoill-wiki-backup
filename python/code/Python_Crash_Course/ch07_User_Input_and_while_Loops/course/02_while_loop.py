# Purpose: repeat code while a condition is `True`
# Reference: page 118 (paper) / 156 (ebook)

# To repeat a block of code while a condition is satisfied, use the `while` control flow statement. {{{1

current_number = 1

# --v
while current_number <= 5:
    print(current_number)
    current_number += 1
#     1
#     2
#     3
#     4
#     5
#
# The  `while` loop  keep executing  its body  repeatedly until  its controlling
# expression  is  `False`.   Here,  the  controlling  expression  is  a  logical
# expression  `current_number <= 5`.  IOW,  the loop  keeps running  as long  as
# `current_number` evaluates to a number lower than `5`.
#
# ---
#
# The `+=`  assignment operator lets us  avoid repeating the same  variable name
# `current_number` on the RHS:
#
#                    v
#     current_number = current_number + 1
#                      ^------------^
#
#     ⇔
#
#     current_number += + 1
#                    ^^
# A `while` loop is useful to let the user decide when a program should end. {{{1

prompt = (
    '\nTell me something, and I will repeat it back to you:'
    "\nEnter 'quit' to end the program. "
)

# we need to  init `message` now, so  that `while` has something to  test on its
# first iteration
message = ''

# iterate until the user inputs the word "quit"
#     v---------------v
while message != 'quit':
    message = input(prompt)

    if message != 'quit':
        print(message)
#     Tell me something, and I will repeat it back to you:
#     Enter 'quit' to end the program. Hello everyone!
#     Hello everyone!
#
#     Tell me something, and I will repeat it back to you:
#     Enter 'quit' to end the program. Hello  again.
#     Hello  again.
#
#     Tell me something, and I will repeat it back to you:
#     Enter 'quit' to end the program. quit

# If the condition gets too complex, use a flag. {{{1

prompt = (
    '\nTell me something, and I will repeat it back to you:'
    "\nEnter 'quit' to end the program. "
)

# Boolean variable which we'll use as a flag.
# We initialize it with  the Boolean `True`, so that the  next loop doesn't bail
# out immediately before asking the user for a message at least once.
# ---v
active = True

# The loop will keep running until `active` is `False`.
#     v----v
while active:
    message = input(prompt)

    # Here, the condition is simple, because  there is only 1 circumstance where
    # we want the program to end (when the user has input the word "quit"); so a
    # flag doesn't help a lot.
    # But in  the future, there  might be more  circumstances where we  want the
    # program to end, in which case a flag helps us organize the tests in a more
    # readable  way  (i.e.  at  different  locations  vs  in  a  single  `while`
    # statement).  For example,  we could add 1 new `elif`  clause for every new
    # circumstance where we want the program to end.
    if message == 'quit':
        active = False
    else:
        print(message)
# }}}1

# `break` is a control flow statement which lets you break out of a loop immediately, wherever you're in its body. {{{1

prompt = (
    '\nPlease enter the name of a city you have visited:'
    "\n(Enter 'quit' when you are finished.) "
)

# A `while True` loop can only end if its body contains a `break` statement.
while True:
    city = input(prompt)

    if city == 'quit':
        break
        # --^
        #
        # End the  loop if the  user has input the  word "quit", instead  of the
        # name of a city.
    else:
        print(f"I'd love to go to {city.title()}!")
#     Please enter the name of a city you have visited:
#     (Enter 'quit' when you are finished.) New York
#     I'd love to go to New York!
#
#     Please enter the name of a city you have visited:
#     (Enter 'quit' when you are finished.) San Francisco
#     I'd love to go to San Francisco!
#
#     Please enter the name of a city you have visited:
#     (Enter 'quit' when you are finished.) quit

#   `break` works in any kind of loop; including a `for` loop. {{{1

for n in range(5):
    if n == 3:
        break
    print(n)
#     0
#     1
#     2
#
# The loop has only printed the numbers 0, 1, and 2; not 3 and 4.
# That's because  it has ended  prematurely when `n`  reached the value  `3`; at
# that moment,  the `if` block  has executed  its `break` statement  causing the
# execution to jump out of the loop.
# }}}1

# `continue` is another control flow statement which lets you skip the rest of an interation. {{{1
# It doesn't quit the loop; the execution immediately jumps back to the `while` (or `for`) statement.

# iterate over positive integers lower than 10
current_number = 0
while current_number < 10:
    current_number += 1

    if current_number % 2 == 0:
        continue
        # -----^
        #
        # If  `current_number`  is  an  even  number,  then  the  previous  test
        # succeeds,  the   `continue`  statement  is  run,   and  the  execution
        # immediately jumps back to the  `while` statement.  In effect, the next
        # `print()` is then skipped, which is only odd numbers are printed.

    print(current_number)
#     1
#     3
#     5
#     7
#     9
# A `while` loop might unexpectedly never end. {{{1

x = 1
while x <= 5:
    print(x)
    #     x += 1
    #
    # With this incrementation, the loop would end quickly.
    #
    # But if for some reason, you forget it (here it's commented out which gives
    # the same results), then the loop will never terminate, causing the program
    # to consume a lot  of CPU.  That's because the value  of `x` never changes;
    # it keeps  the value  1 which  will always be  lower than  5, and  thus the
    # controlling expression will always evaluate to `True`.
    #
    # If you get stuck in an infinite  loop, press `CTRL-C` to send the `SIGINT`
    # signal to the Python process.
