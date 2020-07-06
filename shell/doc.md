# How to print a short help for the `man(1)` command?

    $ man -h

##
# How to know which topic is covered by a section of the manual?

    % man <section number> C-d

This works  only in zsh,  and on the  condition you set  the 'separate-sections'
style to true for the 'manuals' tag:

    zstyle ':completion:*:manuals' separate-sections true

##
# How to get the path to the manpage of the `ls(1)` command?

    $ man -w ls
           │
           └ mnemonic: Where

# How to print the NAME section of the `pstree(1)` command?  (2)

    $ man -f pstree

    $ whatis pstree

##
# How to get the manpages
## whose NAME section contains the word 'sound'?

    $ apropos sound

    $ man -k sound
           │
           └ mnemonic: loo*k* up; small 'k' = just in description

## whose NAME section contains the words 'delete file'?

    $ apropos 'delete file'
    $ man -k 'delete file'

## containing the word 'game' anywhere?

    $ man -s6 -Kw game
           │   ││
           │   │└ mnemonic: I just want to know *w*here it is (don't open the pages)
           │   │
           │   └ mnemonic: loo*K* up; big 'K' = in the whole pages
           │
           └ limit the search to the manpages in section 6

The search is time/cpu-consuming, so it's wise  to add the `-s` option and limit
the search to one or a few section(s) of the manual.

Without `-w`, the shell would open consecutively each found manpage.
And after closing a page, we would have to press:

    ┌─────┬────────────────────────────────┐
    │ CR  │ to load the next found manpage │
    ├─────┼────────────────────────────────┤
    │ C-d │ to skip the next found manpage │
    ├─────┼────────────────────────────────┤
    │ C-C │ stop                           │
    └─────┴────────────────────────────────┘

## whose contents matches a regex?

    $ man -s1 -Kw --regex 'your regex'
                  ^-----^

##
# How to print the list of builtin commands for which there's a help page?

    $ help

# How to print the help about the `fc` builtin command?

    % help fc

    $ help -m fc
            │
            └ in bash, this option displays the help in a Manpage-like format

##
# Issues
## I'm looking for a word containing hyphens with `man -Kw word-with-hypens`.  No page is found!

That's because `man` greps the source code of the man pages, not their rendered version.
And in the source code, a hyphen must be escaped to be rendered literally.

So, escape your hyphens:

    $ man -Kw 'word\-with\-hyphens'
              │
              └ quote the word to prevent the shell from removing the backslashes

---

Remember,  if you  don't understand  why  a keyword/regex  can't be  found in  a
particular page, read its source code.

