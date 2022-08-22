# Purpose: Start  with  your  work  from   Exercise  8-10.   Call  the  function
# `send_messages()` with  a copy  of the  list of  messages.  After  calling the
# function, print both of your lists to show that the original list has retained
# its messages.

# Reference: page 146 (paper) / 184 (ebook)

def send_messages(messages):
    """Print each message from the list `messages`."""
    while messages:
        current_message = messages.pop()
        print(current_message)
        sent_messages.append(current_message)

sent_messages = []
messages = ['foo', 'bar', 'baz']

# Pass a copy for the original value of `messages` to be preserved.
#                     vvv
send_messages(messages[:])
#     baz
#     bar
#     foo

print()
print(messages)
print(sent_messages)
#     ['foo', 'bar', 'baz']
#     ['baz', 'bar', 'foo']
#
# Notice that `messages` has not changed.
