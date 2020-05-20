# How to paste a register in a terminal buffer in Vim?

You must be in Terminal-Job mode, and temporarily switch to Terminal-Normal mode
via `'termwinkey'`.  From this stack of modes, you can paste the `a` register by
pressing:

    "a

It's similar to how you would insert  the register from insert mode in a regular
buffer after  pressing `C-r`.   Except that  in a terminal  buffer, you  have to
prefix the register name  with `"`, so that Vim knows that  you're not trying to
execute a normal mode command.

See `:h t_CTRL-W_quote`.

## What about Nvim?

Like you would in a regular buffer.
To paste the `a` register, you must be in Terminal-Normal mode, and press `"ap`.

##
# Pitfalls
## In xterm, Vim doesn't make the difference between `<m-g>` and `<m-G>`!

The shift modifier must be explicit:

    <m-s-g>
       ^^

Example:

    ✘
    vim -Nu NONE +'nno <m-g> :echo "m-g"<cr>' +'nno <m-G> :echo "m-G"<cr>'
    " press m-g and m-G: no difference

    ✔
    vim -Nu NONE +'nno <m-g> :echo "m-g"<cr>' +'nno <m-s-g> :echo "m-G"<cr>'
                                                       ^^
    " press m-g and m-G: Vim makes the difference

##
## How to send a command from a (N)Vim terminal to a host Vim process?

Write an OSC 51 sequence on the tty:

    $ vim -Nu NONE -S <(cat <<'EOF'
        term
        fu Tapi_func(buf, arglist)
            echom 'arbitrary command run from buffer '..a:buf
            echom 'the function received the arguments '..join(a:arglist)
        endfu
    EOF
    )

    " in Vim's terminal
    $ printf -- "\033]51;[\"call\", \"Tapi_func\", [\"arg1\", \"arg2\"]]\007"
    :mess
    arbitrary command run from buffer 2~
    the function received the arguments arg1 arg2~

See `:h terminal-api` for more info.

### Wait.  Why can't I use something like `--remote-expr`?

You could, but you would need the host Vim process to have become a server.

If that's  not the case (i.e. Vim  was not started with  `--servername {name}`),
you could make it become one with `remote_startserver()`:

    :call remote_startserver('my server')

Then, you would be able to communicate with it like so:

    $ vim --servername 'my server' --remote-expr 'execute("tabe $MYVIMRC")'

But you can't make Vim become a server without an X server.
That's because the communication between a  client and a server goes through the
latter.  See `:h x11-clientserver` for more info.

As a result, the OSC 51 sequence is  easier (no need to make sure Vim has become
a server), and more reliable (doesn't require an X server).

### It doesn't work because of "E474: invalid argument"!

Make sure you've wrapped all the arguments inside double quotes, and not single ones:

    $ vim -Nu NONE +term
    " in Vim's terminal
    $ printf -- "\033]51;[\"drop\", 'file']\007"
    E474: Invalid argument          ^    ^~
                                    ✘    ✘

    $ printf -- "\033]51;[\"drop\", \"file\"]\007"
                                     ^     ^
                                     ✔     ✔

---

Because of  this, if your argument  comes from some Vim  expression (which could
happen  if your  terminal buffer  runs a  nested Vim  instead of  an interactive
shell),  you can't  use `string()`  to include  its evaluation  inside a  string
concatenation:

    $ vim -Nu NONE +term

    " in Vim's terminal
    $ vim -Nu NONE +'let file = "/tmp/file"'
                                                            ✘
                                                            vvvvvv
    :call writefile([printf('%s]51;["drop", %s]%s', "\033", string(file), "\007")], '/dev/tty', 'b')
    E474: Invalid argument~

Use `json_encode()` instead:
                                                            ✔
                                                            vvvvvvvvvvv
    :call writefile([printf('%s]51;["drop", %s]%s', "\033", json_encode(file), "\007")], '/dev/tty', 'b')

### It doesn't work for no apparent reason!

Make sure your sequence is not too long.

    $ vim -Nu NONE -S <(cat <<'EOF'
        term
        fu Tapi_drop(_, files)
            exe 'tabnew | drop '..join(a:files)
        endfu
    EOF
    )

    " in Vim's terminal
    $ vim -Nu NONE
    :let files = map(range(1, 279), {_,v -> '/tmp/file'..v})
    :call writefile([printf('%s]51;["call", "Tapi_drop", %s]%s', "\033", json_encode(files), "\007")], '/dev/tty', 'b')
    " fails for 279 or more files, but succeeds for 278 or fewer

There seems to be a limit size on the sequence you can send via OSC 51.

If  you have  to execute  a very  long command  (e.g. if  it includes  many file
paths), write most of it inside a temporary file, and let the outer Vim read it.
This allows you  to shorten the sequence;  you just have to include  the name of
the temporary file.

    $ vim -Nu NONE -S <(cat <<'EOF'
        term
        fu Tapi_drop(_, filelist)
            exe 'tabnew | drop '..join(readfile(a:filelist))
        endfu
    EOF
    )

    " in Vim's terminal
    $ vim -Nu NONE
    :let files = map(range(1, 279), {_,v -> '/tmp/file'..v})
    :call writefile(files, '/tmp/filelist', 'b')
    :call writefile([printf('%s]51;["call", "Tapi_drop", "/tmp/filelist"]%s', "\033", "\007")], '/dev/tty', 'b')

##
# Issues
## Vim only
### The image preview in ranger is buggy!

It's wrongly positioned and is too small.

There were other issues in the past which were fixed when Vim updated libvterm.
Maybe this issue will be fixed when libvterm is updated yet again...

##
## Nvim only
### The terminal doesn't support the bracketed paste mode!

MWE:

    $ nvim -Nu NONE +'let @+ = "# a\n# b"' +terminal +startinsert
    C-S-v

`# a` is wrongly run.

It's a known issue: <https://github.com/neovim/neovim/issues/11418>

### Nvim crashes after I delete too many lines in a terminal buffer!

MWE:

    $ nvim -Nu NONE +term +setl\ modifiable +startinsert
    $ cat ~/.vim/vimrc
    C-\ C-n
    dgg
    i
    ls Enter

It's a known issue:

>    Will crash if all lines are deleted.
>
>    It's difficult  to support line  deletions, because scrollback  is received
>    passively from  libvterm.  Instead, one  can safely and  correctly "delete"
>    lines by temporarily setting 'scrollback' option to a smaller value.

<https://github.com/neovim/neovim/pull/6142>

>    Note there is a known issue: deleting lines may cause a crash.
>    Deleting lines isn't supported (it will be prevented in a future PR).

<https://github.com/neovim/neovim/pull/6142#issuecomment-282690785>

###
### I can't edit the current command-line by pressing `C-x C-e`!

Well it doesn't make much sense to do it.
I mean, you're in already in an editor.
If you want to edit the line with Nvim commands, just press Escape.

But yeah, it's broken:

    :term
    $ ls C-x C-e
    Error detected while processing function <SNR>119_LoadRemotePlugins[1]..<SNR>119_GetManifest[1]..~
    line    7:~
    E117: Unknown function: stdpath~

There seems  to be  some kind of  recursive loop;  `s:LoadRemotePlugins()` keeps
calling itself again and again.

Same issue in bash and zsh, and same issue when you run `fc`.

---

Workaround: set `$EDITOR` to `nvim` (instead of `vim`) when starting ranger.

    EDITOR=nvim ranger

You could try to  set the variable only when inside  a Nvim terminal (inspecting
some environment variable which is only set in the latter).

#### An error is displayed when I open a file in Vim from ranger!

This is the same error as previously.

Workaround: In your zshrc, replace `vim` with `nvim`:

    __sane_vim() STTY=sane command nvim +'...'
                                   ^^^^

##### and when I use `| vipe`!

Workaround: Set `VISUAL` to `nvim`.

##
# Todo
## Document that `term_sendkeys()` is not instantaneous.

So, if your  next command depends on `term_sendkeys()` to  have finished, try to
first invoke `term_wait()`.

    call term_sendkeys(...)
    call term_wait(...)
    ...

See here for a real example:
<https://github.com/vim/vim/commit/52ea92b19d2bc992dd4570add64c12d98eab9db2>

