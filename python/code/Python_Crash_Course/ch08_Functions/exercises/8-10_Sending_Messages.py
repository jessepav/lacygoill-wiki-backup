# Purpose: Start with a copy of your program from Exercise 8-09.
# Write a  function called `send_messages()`  that prints each text  message and
# moves  each message  to a  new list  called `sent_messages`  as it's  printed.
# After calling the function, print both of your lists to make sure the messages
# were moved correctly.

# Reference: page 146 (paper) / 184 (ebook)

def send_messages(messages):
    """Print each message from the list `messages`."""
    while messages:
        current_message = messages.pop()
        print(current_message)
        sent_messages.append(current_message)

sent_messages = []
messages = ['foo', 'bar', 'baz']

send_messages(messages)
#     baz
#     bar
#     foo

print()
print(messages)
print(sent_messages)
#     []
#     ['baz', 'bar', 'foo']
#
# Notice that `messages` has changed; it's now empty.
