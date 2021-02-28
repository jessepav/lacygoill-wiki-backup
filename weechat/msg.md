# How to send a message
## to a nick connected on the network B, while I'm in a channel on the network A?

Use the `-server` argument:

    /msg -server abjects nick

## to someone which is not connected right now?

    /msg memoserv send bob I hope you'll read this when you're connected again
                       ^^^
                       replace with the nick you want to send a memo to

To get a complete list of all the commands you can send to the bot:

    /msg memoserv help

For more info about a particular command:

    /msg memoserv help <cmd>
                        │
                        └ some useful ones: send, read, list, del, forward, ignore

