# Pitfalls
## ?

What should I always do when passing `%` the name of the current file name to a shell command.

Whenever you  used `system()`, `systemlist()`, or  `:!` to run a  shell command,
and it contained a filename, make sure  you used the filename modifiers `:p` and
`:S`.

Among other things, `:p` is useful to prevent a filename beginning with a hyphen
from being interpreted as an option by the shell:

    $ cmd -some_file
          ^
          ✘

    $ cmd /path/to/-some_file
                   ^
                   ✔

---

Update: I think most of this section applies to any argument passed to a shell command (`:S`/`shellescape()`).

Look for `system()`, `systemlist()` everywhere,  and make sure we've always used
`:S`, `shellescape()` (and `:p` for file names).

From `~/.vim/autoload/myfuncs.vim:848`:

    " Old Interesting Alternative:
    "
    "     sil! exe 'grep! '..shellescape(@")..' .'
    "
    " Even though `:grep` is a Vim command, we really need to use `shellescape()`
    " and NOT `fnameescape()`. Check this:
    "
    "                         ; is special             % is special
    "                         on shell's               on Vim's
    "                         command-line             command-line
    "    ┌───────────────────┬──────────┬─────────────┬────────────┐
    "    │         @"        │  foo;ls  │  that's     │  foo%bar   │
    "    ├───────────────────┼──────────┼─────────────┼────────────┤
    "    │ fnameescape(@")   │  foo;ls  │  that\'s    │  foo\%bar  │
    "    ├───────────────────┼──────────┼─────────────┼────────────┤
    "    │ shellescape(@")   │ 'foo;ls' │ 'that'\''s' │ 'foo%bar'  │
    "    ├───────────────────┼──────────┼─────────────┼────────────┤
    "    │ shellescape(@",1) │ 'foo;ls' │ 'that'\''s' │ 'foo\%bar' │
    "    └───────────────────┴──────────┴─────────────┴────────────┘
    "
    " `fnameescape()` would not protect `;`.
    " The  shell  would  interpret  the  semicolon as  the  end  of  the
    " `grep(1)` command, and would execute the rest as another command.
    " This can be dangerous:
    "
    "     foo;rm -rf
    "
    " Conclusion:
    " When you have a command whose arguments can contain special characters,
    " and you want to protect them from:
    "
    "    - Vim       use `fnameescape(...)`
    "    - the shell use `shellescape(...)`
    "    - both      use `shellescape(..., 1)`
    "                                     │
    "                                     └ only needed after a `:!` command; not in `system(...)`
    "                                       `:!` is the only command to remove the backslashes
    "                                       added by the 2nd non-nul argument
    "
    "                             MWE:
    "                             :sp /tmp/foo\%bar
    "                             :sil call system('echo '.shellescape(expand('%')).' >>/tmp/log')
    "                             :sil call system('echo '.shellescape(expand('%'),1).' >>/tmp/log')
    "
    "                                       $ cat /tmp/log
    "                                           /tmp/foo%bar
    "                                           /tmp/foo\%bar
    "                                                   ^
    "
    " ---
    "
    " Update:
    " If the argument  which can contain special characters  is the name
    " of  the current  file,  you  can use  the  filename modifier  `:S`
    " instead of `shellescape(..., 1)`.
    " It's less verbose.
    " `:S` must be the last modifier, and it can work with other special
    " characters such as `#` or `<cfile>`.

---

Look for `system()` and `systemlist()` everywhere, and look for comments related
to the  issue about `:cexpr`  which parses a bar  as a command  termination even
inside quotes.

Report the issue.

##
# Todo

Look for `C-a` everywhere.
Use `\x01` or `$'\x01'` instead.

