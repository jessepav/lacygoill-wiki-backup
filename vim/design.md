What about the name of the buffer:

        'foobar'
        tempname().'foobar'
        'plugin://foobar'

# sidebar
## Should I use `bh=wipe` or `bh=delete`?

Never use `bh=wipe`.
It would prevent  you from recovering the  buffer if you lose  it temporarily by
accident, by pressing `C-^` or `--` for example.

If  the  buffer  is  automatically   populated  on  `BufNewFile`,  you  can  use
`bh=delete`.
Indeed, if  you lose  it by pressing  `C-^`, pressing `C-^`  a second  time will
trigger `BufNewFile` (whose definition is: starting  to edit a file that doesn't
exist) which will re-populate the buffer.

## Should I use `bt=nofile` or `bt=nowrite`?

`bt=nofile`.

You  probably don't  want to  create a  real file  every time  you display  some
temporary info.
Besides, contrary  to `nowrite`, `nofile`  makes the  name of the  buffer fixed,
i.e. it's not updated whenever you change the working directory (`:cd`).

## Should I use `:leftabove` or `:topleft`?

If the information is specific to the current buffer, choose `:leftabove`.
Otherwise, choose `:topleft`.

## Should I install custom mappings to open filepaths, using special keys (C-s, C-v C-v, C-t)?

No.

There are already default commands for that:

        • gf
        • gF
        • C-w f
        • C-w F
        • C-w gf
        • C-w gF
        • C-w T

You should rely on default commands as much as possible (consistency, synergy, ...).
When they're improved (by you, a  plugin, Vim's developers), you'll benefit from
it automatically.

Avoid  the NIH  syndrome:  don't  create an  ad-hoc  system  which doesn't  work
everywhere, and not always in the same manner.

[Reuse code][1] as much as possible.

##
# Reference

[1]: https://en.wikipedia.org/wiki/Code_reuse
