# How to send an OSC or CSI sequence to the host terminal?

Use `echoraw()`:

    let seq = '...'
    call echoraw(seq)

Example:

    # open an xterm terminal *outside* tmux
    $ vim -Nu NONE -S <(tee <<'EOF'
        let seq = "\033]52;c;" .. system('printf -- "%s" "test" | base64 | tr -d "\n"') .. "\007"
        call echoraw(seq)
        qa!
    EOF
    )

    # press:  C-S-v
    # 'test' is inserted

---

You could also try `!printf`:

    let seq = '...'
    exe '!printf -- ' .. string(seq)

But if the sequence contains characters  which are special on Vim's command-line
(like  `#`), you  need  escape them.   This is  not  necessary with  `echoraw()`
because the sequence  is sent directly to the terminal,  without passing through
Vim's command-line.

---

You could also try `writefile()`:

    let seq = '...'
    call writefile([seq], '/dev/tty', 'b')

But it's more verbose, and it doesn't work in the GUI:

    $ vim -g
    :call writefile([''], '/dev/tty', 'b')
    E482: Can't create file /dev/tty˜

---

Note that you still need double quotes to make Vim translate control characters:

    call echoraw("\033]12;" .. color .. "\007")
                 ^        ^             ^    ^

You could use single quotes if you used `:!printf`; probably because `printf(1)`
takes care of the translation regardless of the type of quotes.

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

##
# Pitfalls
## How to send a command from a Vim terminal to a host Vim process?

Write an OSC 51 sequence on the tty:

    $ vim -Nu NONE -S <(tee <<'EOF'
        term
        fu Tapi_func(buf, arglist)
            echom 'arbitrary command run from buffer ' .. a:buf
            echom 'the function received the arguments ' .. join(a:arglist)
        endfu
    EOF
    )

    " in Vim's terminal
    $ printf -- "\033]51;[\"call\", \"Tapi_func\", [\"arg1\", \"arg2\"]]\007"
    :mess
    arbitrary command run from buffer 2˜
    the function received the arguments arg1 arg2˜

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
    E474: Invalid argument          ^    ^˜
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
                                                            v----v
    :call writefile([printf('%s]51;["drop", %s]%s', "\033", string(file), "\007")], '/dev/tty', 'b')
    E474: Invalid argument˜

Use `json_encode()` instead:

                                                            ✔
                                                            v---------v
    :call writefile([printf('%s]51;["drop", %s]%s', "\033", json_encode(file), "\007")], '/dev/tty', 'b')

### It doesn't work for no apparent reason!

Make sure your sequence is not too long.

    $ vim -Nu NONE -S <(tee <<'EOF'
        term
        fu Tapi_drop(_, files)
            exe 'tabnew | drop ' .. join(a:files)
        endfu
    EOF
    )

    " in Vim's terminal
    $ vim -Nu NONE
    :let files = range(1, 279)->map({_, v -> '/tmp/file' .. v})
    :call writefile([printf('%s]51;["call", "Tapi_drop", %s]%s', "\033", json_encode(files), "\007")], '/dev/tty', 'b')
    " fails for 279 or more files, but succeeds for 278 or fewer

There seems to be a limit size on the sequence you can send via OSC 51.

If  you have  to execute  a very  long command  (e.g. if  it includes  many file
paths), write most of it inside a temporary file, and let the outer Vim read it.
This lets  you shorten the sequence;  you just have  to include the name  of the
temporary file.

    $ vim -Nu NONE -S <(tee <<'EOF'
        term
        fu Tapi_drop(_, filelist)
            exe 'tabnew | drop ' .. readfile(a:filelist)->join()
        endfu
    EOF
    )

    " in Vim's terminal
    $ vim -Nu NONE
    :let files = range(1, 279)->map({_, v -> '/tmp/file' .. v})
    :call writefile(files, '/tmp/filelist', 'b')
    :call writefile([printf('%s]51;["call", "Tapi_drop", "/tmp/filelist"]%s', "\033", "\007")], '/dev/tty', 'b')

##
# Issues
## The image preview in ranger is buggy!

It's wrongly positioned and is too small.

There were other issues in the past which were fixed when Vim updated libvterm.
Maybe this issue will be fixed when libvterm is updated yet again...

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

