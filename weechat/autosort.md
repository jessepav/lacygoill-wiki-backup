# Rules
## How does `autosort.py` use the rules to sort my buffer list?

For each buffer, the script evaluates the expression assigned to each rule.
As a result,  each buffer is bound to a  list of values, which can be  seen as a
matrix.
You can see it with the `/autosort debug` command.

Then, the script tries  to sort the buffers according to the  first value of all
these lists (the first column of the matrix).
If the values are numbers, they're sorted numerically.
If they're strings, they're sorted lexicographically.

If the value is  identical for some buffers, then the script  tries to sort them
using the second values of the lists (2nd column of the matrix).

The process repeats itself: every time the script encounters a subset of buffers
for which the n-th  values of the lists are identical, it  uses the (n+1) values
to sort further.

## What are the default rules used to sort my buffer list?

Make sure the core buffer comes first:

    0: ${core_first}


Make sure the channel/server buffers come after special buffers (fset, xfer)

    1: ${irc_last}


Sort the buffers according to the name of the plugin which created them

    2: ${buffer.plugin.name}


Make sure the raw buffers come first

    3: ${irc_raw_first}


Sort the buffers according to the servers from which they've been created.
Note that  we need  to test  whether the buffer  has been  created by  the `irc`
plugin, because `${server}` exists only for this type of buffer.

    4: ${if:${plugin}==irc?${server}}


Sort the buffers according to their type:

                                                 ┌ type of the buffer
                                                 ├─────┐
    5: ${if:${plugin}==irc?${info:autosort_order,${type},server,*,channel,private}}
                           ├──────────────────────────────────────────────────────┘
                           └ 0 if `${type}` evaluates to 'server'
                             1 if `${type}` evaluates to '*'
                             2 if `${type}` evaluates to 'channel'
                             3 if `${type}` evaluates to 'private'


Sort the buffers according to their names without number signs:

    6: ${if:${plugin}==irc?${hashless_name}}


Sort the buffers according to their full names:

    7: ${buffer.full_name}

---

They use the following helper variables:

                                        ┌ by using `!=`, the expression will evaluate to `1` for all buffers,
                                        │ except for the core buffer where it will evaluate to `0`,
                                        │ so we can be sure that the core buffer will always be first
                                        │
    core_first: ${if:${buffer.full_name}!=core.weechat}

                                   ┌ The plugin name will always be 'irc' except for special buffers
                                   │ (fset, xfer, ...).
                                   │ The expression will evaluate to `0` for special buffers,
                                   │ and `1` for irc ones.
                                   │ So we can be sure that the special buffers will always come before
                                   │ the channel/server buffers.
                                   │
    irc_last: ${if:${buffer.plugin.name}==irc}

    irc_raw_first: ${if:${buffer.full_name}!=irc.irc_raw}

    hashless_name: ${info:autosort_replace,#,,${buffer.name}}

## How to print the list of sort rules?

    /autosort rules list

## How to add a new rule at the end of the list?

    /autosort rules add <expr>

## How to insert a new rule in 3rd position in the list?

    /autosort rules insert 3 <expr>

## How to update the 3rd rule?

    /autosort rules update 3 <expr>

## How to remove the 3rd rule?

    /autosort rules delete 3

## How to move the 3rd rule to the 5th position?

    /autosort rules move 3 5

## How to swap the rules 3 and 5?

    /autosort rules swap 3 5

## How to debug my sort rules?

    /autosort debug

This will show the evaluation of the sort rules for each buffer.
Example:

    autosort: core.weechat:           ['0', '0', '',    '1', '',         '',  '',                  'core.weechat']
    autosort: irc.server.abjects:     ['1', '1', 'irc', '1', 'abjects',  '0', 'server.abjects',    'irc.server.abjects']
    autosort: irc.abjects.#mg-chat:   ['1', '1', 'irc', '1', 'abjects',  '2', 'abjects.mg-chat',   'irc.abjects.#mg-chat']
    autosort: irc.abjects.#moviegods: ['1', '1', 'irc', '1', 'abjects',  '2', 'abjects.moviegods', 'irc.abjects.#moviegods']
    autosort: irc.server.freenode:    ['1', '1', 'irc', '1', 'freenode', '0', 'server.freenode',   'irc.server.freenode']
    autosort: irc.freenode.#ircv3:    ['1', '1', 'irc', '1', 'freenode', '2', 'freenode.ircv3',    'irc.freenode.#ircv3']
    autosort: irc.freenode.#ranger:   ['1', '1', 'irc', '1', 'freenode', '2', 'freenode.ranger',   'irc.freenode.#ranger']

##
# Signals
## When does `autosort.py` sort my buffer list?

By default, whenever a buffer is opened, merged, unmerged or renamed.

## How to change the list of signals causing my buffer list to be sorted?

Edit the `autosort.sorting.signals` option to add or remove any signal you want.

## How to prevent all automatic sorting?

Empty this option:

    autosort.sorting.signals

And disable this one:

    autosort.sorting.sort_on_config_change

##
# Helper variables
## What's a helper variable?

To make your rules more readable, you  can assign a long/complex expression to a
helper variable with a telling name.
Then, you can refer to it in your rules with the syntax:

    ${my_helper_variable}

## How to print the list of helper variables?

    /autosort helpers list

## How to add or update the helper variable 'foo'?

    /autosort helpers set foo <expr>

## How to delete the helper variable 'foo'?

    /autosort helpers delete foo

## How to rename the helper variable 'foo' into 'bar'?

    /autosort helpers rename foo bar

## How to swap the expressions of the helper variables 'foo' and 'bar'?

    /autosort helpers swap foo bar

##
# Misc.
## How to manually sort my buffers?

    /autosort sort

## What's the expression which evaluates to the name of the buffer, stripped of all its number signs?

           ┌ info hook added by `autosort.py`
           │
    ${info:autosort_replace,#,,${buffer.name}}
                             ├┘
                             └ no replacement

---

The general syntax is:

    ${info:autosort_replace,from,to,text}

---

To  include  a comma  or  a  backslash inside  an  argument,  escape it  with  a
backslash.

## What's the expression which evaluates to the position of the type of the buffer in the list [server,*,channel,private]?

    ${info:autosort_order,${type},server,*,channel,private}

