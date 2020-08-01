# Files
## How to reload the configuration from all the files on the disk?   Only the config of the `xfer` plugin?

    /reload
    /reload xfer
               ^
               notice that there's no '.conf' extension

## Why shouldn't I edit a config file directly?

1. WeeChat may overwrite the file at any time (for example on `/quit`).

2. You need to execute `/reload` after editing a file so that WeeChat reads the
   changes.

In both  cases (`/quit`, `/reload`),  any change  which wasn't saved  by `/save`
will be lost.

##
# Options
## How to set an option manually?

    /set file.section.option value
         │    │       │
         │    │       └ the option name
         │    │
         │    └ section to which belongs the option
         │
         └ basename of the file (without the extension '.conf')
           where the option will be saved

           core options are saved in `weechat.conf`,
           the others are saved in `plugin_name.conf`

## How to set an option interactively?

    /set plugin.section.option
    M-C-m
    # assign new value
    C-m

## How to set a value A to an option in all buffers, except in the ones ending with `pat` where I would prefer B?

    /set my.option "value_A"
    /allchan -include=*pat /command_to_set_value_B

---

Example:

    /set aspell.check.default_dict "en"
    /allchan -include=*fr aspell setdict fr

This  should set  make the  `aspell`  plugin use  an english  dictionary in  all
buffers, except in the ones whose name end with `fr`.

##
## How to get info about an option?

    /help file.section.option

## How to list all options?   Core (i.e. non-plugin) options?   The options of the IRC plugin?

    /set
    /set weechat.*
    /set irc.*

## How to list all options containing the word 'color'?  (2)

    /fset color
    /set *color*

## How to list all options whose value has been changed?

    /fset d:*

## How to list all options whose type is 'color' or 'string', and value contains 'white'?

    /fset c:${value} =~ white && (${type} == color || ${type} == string)
          ├┘├──────┘
          │ └ replaced by the value of the option
          │
          └ the following will be evaluated and used as a condition

## How to export all options whose value has been changed in a file?

    /fset d:*
    /fset -export -help /tmp/wee.conf
                  │
                  └ include comments before each `/set` command
                    to describe what the option does

##
## How to interactively reset an option?

    r C-m

## How to reset all core options?

    /unset -mask weechat.*

## How to reset all options of the `xfer` plugin?

    /unset -mask xfer.*

##
## How to save the new value given to an option?

    /save

Or:

    /quit

## Do I need to restart WeeChat after resetting an option?

No.

WeeChat immediately uses the new value.

## How to close the buffer opened by `/set`?   (2)

    q C-m

Or:

    /close

##
# Logging
## How to see which buffers are being logged, and what is being logged?

    /logger list

##
# Resources
## Which option sets a limit on the resources consumed by the WeeChat process?

    weechat.startup.sys_rlimit

## What's the format of its value?

    "res1:limit1,res2:limit2,..."
     │
     └ resource name

To get the name of a resource, see `man getrlimit`.
Look for constant names prefixed by `RLIMIT_`.
Take the name afterwards, and use it in its lowercase form.

Example:

               v-v
        RLIMIT_CPU
    →
        cpu

---

As an  example, to set an  unlimited size for  core files and limit  the virtual
memory to 1GB, you would execute:

    /set weechat.startup.sys_rlimit "core:-1,as:1000000000"
                                             ^^
                                             Address Space

## How to remove any limit on a resource?

Give the value `-1` to its limit.

## How to enable core files?

Set the option `weechat.startup.sys_rlimit` to the value `-1`:

    /set weechat.startup.sys_rlimit "core:-1"

##
# Key bindings
## How to bind a key to a command?

    /key bind <key> /<cmd>

## How to remove a key binding?

    /key unbind <key>

##
## How to list all the key bindings?   All the ones which have been added/removed/redefined?

    /key list
    /key listdiff

## How to reset a key to its default binding?

    /key reset <key>

## How to reset all key bindings?

    /key resetall -yes

##
## In the lhs of a key binding, can WeeChat distinguish between `meta-g` and `meta-G`?

Yes.

Example:

    /key bind meta-g /set weechat.bar.title.hidden toggle
    /key bind meta-G /set weechat.bar.nicklist.hidden toggle

Enter a channel and press `M-g`, then `M-G`:
it will toggle the title and the nicklist, separately.

## In the lhs of a key binding, can WeeChat distinguish between `ctrl-g` and `ctrl-G`?

No.

Counter-example:

    # ✘
    /key bind ctrl-g /set weechat.bar.title.hidden toggle

    # ✔
    /key bind ctrl-G /set weechat.bar.title.hidden toggle

If the  lhs of  your key  binding uses  the Ctrl  modifier, you  need to  use an
UPPERCASE letter.

---

Why the inconsistency between ctrl and meta?

Because of the terminal.
It can't distinguish between `ctrl-g` and  `ctrl-G`, but it can between `meta-g`
and `meta-G`; try with `cat(1)`.

## Can I use both ctrl and meta?

Yes, but only if you use `meta-ctrl-[a-z]`:

    /key bind meta-ctrl-g /set weechat.bar.title.hidden toggle

---

It doesn't work if you use `ctrl-meta-[a-zA-Z]`:

    # ✘
    /key bind ctrl-meta-g /set weechat.bar.title.hidden toggle
    /key bind ctrl-meta-G /set weechat.bar.title.hidden toggle

And it doesn't work if you use `meta-ctrl-[A-Z]`

    # ✘
    /key bind meta-ctrl-G /set weechat.bar.title.hidden toggle

##
# Aliases
## How to list all currently installed aliases?

      /alias list

## How to remove an alias?

      /alias del <alias>

## How to install an alias, running two commands?

      /alias add <alias> cmd1 ; cmd2
                              ^

##
# Todo
## we've remapped M-j to `/window scroll_down`; this prevents us from using a whole bunch of default key bindings

Run `/key list`, and search for 'meta-j'.
Many default key bindings use M-j as a prefix.
In particular, `M-j 12` lets you jump to the buffer 12.
Remap all of them, so that they use a different prefix.

## ?

Study the differences between `/set` and `/fset`.
Whenever we've used  some `/set` commands in our notes,  make sure `/fset` would
not have been more appropriate; in  particular, maybe `/fset` lets us avoid some
wildcards...

I think that  when you have two  wildcards and a `/set` command,  you should use
`/fset` instead:

    /set *color*
    →
    /fset color

But if  you're looking for several  words, then you should  probably use `/set`,
because `/fset` doesn't seem to work in this case:

    /set foo*bar*

Also, if  you want to be  sure that a  word matches at  the start or end  of the
option names, I think you should use `/set`:

    # foo will match at the start
    /set foo*

    # bar will match at the end
    /set *bar

    # foobar will match anywhere
    /fset foobar

