# Purpose: Make a  list containing a  series of  short text messages.   Pass the
# list to a function called `show_messages()`, which prints each text message.

# Reference: page 146 (paper) / 184 (ebook)

def show_messages(messages):
    """Print each message from the list `messages`."""
    for msg in messages:
        print(msg)

messages = ['foo', 'bar', 'baz']
show_messages(messages)
#     foo
#     bar
#     baz
