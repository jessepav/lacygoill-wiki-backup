# How to get help for a command?

    /help command
          ^
          notice that there's no slash in front of the name

# Which command allows me to call built-in WeeChat functions from a key binding?

    /input

# How to get the name of the plugin providing a command?

When you execute the `/help command`,  the plugin providing the command is given
(inside brackets):

    /help nick
    [irc]  /nick  [-all] <nick>~
    ^---^

# How to read the output of a shell command in the current buffer?   In a new buffer?

    /exec -o ls
    /exec -n ls

