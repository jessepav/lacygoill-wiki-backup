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

##
# I need to pass an argument to an Ex command, and it may contain special characters.  When should I use
## `fnameescape()`?

Use it if the characters are special on Vim's command-line (`:h cmdline-special`),
and your argument is unquoted (outside a string).

Example:

    :e /tmp/foo
    :b#
    :sp /tmp/foo#bar
    :echo expand('%:p')
    /tmp/foo/tmp/foobar~
    ✘

    :e /tmp/foo
    :b#
    :exe 'sp '..fnameescape('/tmp/foo#bar')
    :echo expand('%:p')
    /tmp/foo#bar~
    ✔

### Which alternative can I use?

Expand backticks as a Vim expression:

    :e /tmp/foo
    :b#
    :sp `='/tmp/foo#bar'`
    :echo expand('%:p')
    /tmp/foo#bar~
    ✔

See `:h backtick-expansion /=`.

##
## ?

`shellescape()`?

Use it if your argument will be parsed by the shell.

Example:

    :exe 'grep! '..shellescape('==#')..' $VIMRUNTIME'

Wait...
Why is `#` replaced by the alternate filename?

Answer:
Because `:grep` runs the shell command set by `'grepprg'` via `:!`.
Check this:

    :4verb exe 'grep! '..shellescape('==#')..' $VIMRUNTIME'
    :!rg -LS --vimgrep 2>/dev/null '==/tmp/foo#bar' $VIMRUNTIME 2>&1| tee /tmp/v6WVFDZ/45~
     ^

Are there other Ex commands which invoke `:!` (see `:h :index`)?
Make sure that whenever we've used any of them, we've passed the second optional
argument `1` to `shellescape()`.

## ?

Maybe we should replace `[!=]=[#?]\=` with `[!]empty()` everywhere.
This is more readable, and you don't have to wonder whether `#` should be used.

What about `is# ''` and `isnot# ''`?
Should we replace them with `[!]empty()` too?

## ?

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
    " The  shell would  interpret  the semicolon  as the  end  of the  `grep(1)`
    " command, and would execute the rest as another command.
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

## ?

Do we really need `:CGrep`?
We already have `C-g g`...

Old comment:

    " We already have `:CGrep`, so why `:PQ`?
    "
    " `:CGrep` (and `|g`) relies on `rg(1)` and `'efm'` (because we use `:cgetexpr`).
    " `:PQ` gives us more control on the grep program.
    " For example, it lets us pass the argument `-w` to `rg(1)`:
    "
    "    ┌─────────────────────────┬──────────────────────────────────────────────────────┐
    "    │ :CGrep              pat │ search any `pat` using   `$ ripgrep --vimgrep -i -L` │
    "    ├─────────────────────────┼──────────────────────────────────────────────────────┤
    "    │ :PQ ag    --vimgrep pat │ search any `pat` using   `$ ag --vimgrep`            │
    "    ├─────────────────────────┼──────────────────────────────────────────────────────┤
    "    │ :PQ ag -w --vimgrep pat │ search a whole word `pat` using `$ ag -w --vimgrep`  │
    "    └─────────────────────────┴──────────────────────────────────────────────────────┘
    "             -w --word-regexp
    "             Only match whole words.

## ?

Document what's the benefit/disadvantage of `:cexpr` (&friends) compared to `setqflist()`.
Hint: `:cexpr` is better suited for an interactive usage.

Old comment:

    " Why `:lgetexpr` instead of `:lgrep!`?{{{
    "
    " The latter shows us the output of the shell command (`$ rg ...`).
    " This makes the screen flicker, which is distracting.
    "}}}
    "     sil lgetexpr system(cmd)
    "     call setloclist(0, [], 'a', {'title': cmd})

## ?

Remember that we use `:do QuickFixCmdPost` to open the qf window in our plugins?
What pattern should we use? `[cl]window` or `[cl]open`?
Which rule should we follow to decide?

