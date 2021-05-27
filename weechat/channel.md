# Getting info
## How to print the modes set on a given channel?

    /mode #chan

The info will be printed in the buffer of `#chan`:

    Mode #weechat [+Ccntj 6:10]˜
    Channel created on Sun, 26 Nov 2006 07:42:51˜

## How to get the meaning of a given mode?

It probably depends on the network hosting the channel.

For the libera network, you can get more information from here:
<https://libera.chat/guides/channelmodes>

##
# Joining a channel
## How to join `#chan` without giving the focus to its buffer?

    /j -noswitch #chan

## How to join `#chan`, `#protected_chan`, and give the key required by the latter?

    /j #protected_chan,#chan <key>

Channels requiring a key must come first.
Otherwise, how would WeeChat know which channel needs the key?

---

Note that you can join several channels requiring a key:

    /j #protected_chan1,#chan <key1>,<key2>

###
## If I type `/j #chan`, while I'm connected to multiple networks, on which network will `#chan` be selected?

The one of the current channel, if you're in a channel.

The one which has the focus, if you're in the core buffer.
Press C-x to change the focus.

## How to join a channel on the network B, while I'm in a channel on the network A?

Use the `-server` argument:

    /j -server abjects #mg-chat

##
# Leaving a channel
## What's the difference between `/part` and `/close`?

`/close` leaves the current channel (or private buffer) AND closes its window.
`/part` only leaves the channel.

## To leave a channel, should I use `/part` or `/leave`?   Why?

Prefer `part`.

`leave` is only an alias for `part`.
WeeChat understands it, but the IRC server probably doesn't.
When  you execute  `/leave`, WeeChat  automatically replaces  this command  with
`/part`.

If  one day  you use  an  unfamiliar IRC  client/server, it  may not  understand
`/leave`.
The server does not necessarily know any command your client accepts from you.
So, better take the habit of using `/part`.

## How to leave `#chan1`, `#chan2` and `#chan3`, and give the message 'going to bed'?

    /part #chan1,#chan2,#chan3 going to bed

