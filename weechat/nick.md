# get info about someone
## How to query information about user(s)?

    /whois  [<nick>[,<nick>...]]
              │
              └ may be a mask

## What happens when you use the previous command without any argument?

Without argument, `/whois` will target:

   - your own nick if the current buffer belongs to a network/channel

   - the remote nick if the current buffer is a private one
     (discussion between 2 people)

##
# nicklist bar
## How to scroll in the nicklist bar?

Press `F11` or `F12`.

##
# my nick
## How to change it for the current network?   For all networks on which I'm connected?

    /nick        my_new_nick
    /nick  -all  my_new_nick

##
# ignore people
## How to ignore the nick 'toto'?

    /ignore add toto

## How to ignore the host 'toto@domain.com' on the network libera?

    /ignore add toto@domain.com libera

## How to ignore the host 'toto@domain.com' on the channel #weechat on the network libera?

    /ignore add toto*@*.domain.com libera #weechat

## How to ignore all nicks beginning with 'toto'?   (with and without a regex)

                ┌ the following text is not a literal nick/hostname;
                │ it's a regex
                ├─┐
    /ignore add re:toto.*
                   ├────┘
                   └ POSIX extended regular expression

    /ignore add toto*
                ├───┘
                └ mask (!= regex)

In a mask, `*` can match 0 or more characters.

## How to ignore all nicks beginning with 'toto', case-sensitively?

    /ignore add re:(?-i)toto.*

FIXME: It doesn't work.
Why?
According to `/help ignore`, adding `(?-i)` in front of the regex should make it
case-sensitive.

## What's the general syntax of the `/ignore add` command?

    /ignore add [re:]<nick> [<network> [<#channel>]]

###
## How to list all the nicks ignored?

    /ignore list

###
## How to remove a nick from my ignore list?

    # note the id of the entry you want to remove
    /ignore list

    /ignore del <id>

## How to empty my ignore list?

    /ignore del -all

##
# Issues
## I've successfully added an ignore, but it fails to hide the messages from the person I want to ignore!

If you used a regex, it must describe the whole nick/hostname; not just a part.

---

In the prefix in the chat area, if the  nick you want to ignore is followed by a
`▹` sign, it means that it's longer than what can be displayed.
You have to  display the nicklist bar,  which should be wide enough  to show the
nick in its entirety.

