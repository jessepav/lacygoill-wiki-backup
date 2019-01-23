# ?

The sequence `\e]52;c; text \x07` is described on [this page](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Operating-System-Commands).

It tells that the function called by the sequence may be disabled using the `allowWindowOps` resource.
This is how it's described in `$ man xterm`:

> allowWindowOps (class AllowWindowOps)
>
> Specifies whether extended window control sequences (as used in dtterm) should
> be  allowed.  These  include several  control sequences  which manipulate  the
> window size or  position, as well as  reporting these values and  the title or
> icon name.   Each of these  can be abused in  a script; curiously  enough most
> terminal emulators  that implement  these restrict  only a  small part  of the
> repertoire.  For finetuning, see disallowedWindowOps.  The default is “false”.

Note that it says that the resource is disabled by default.
You can enable it by writing in `~/.Xresources`:

    xterm.VT100.allowWindowOps:  true

Then, if you start `xterm` and run this command:

    $ printf -- '\e]52;c;%s\x07' $(base64 <<<'hello')

Your clipboard should contain the text `hello`.

However, it seems that `urxvt` doesn't support this resource. At least I couldn't find it in one of its manpages (`$ man -Kw allowWindowOps`).

I tried to include a wildcard in the name resource:

    *.allowWindowOps:  true

But the sequence still doesn't work in `urxvt`.

Edit:

It might depend on how your binary was compiled. According to `$ man 7 urxvt`, the `--enable-frills` option enables some non-essential features otherwise disabled, including the OSC escape sequences.
I'm not sure it would help, but maybe you could try to recompile with `--enable-frills`.

# ?

The following is useful to synchronize the local clipboard with the one of a remote server:

    " Inspiration:
    " https://www.reddit.com/r/vim/comments/ac9eyh/talk_i_gave_on_going_mouseless_with_vim_tmux/ed6kl67/
    " Doesn't work atm...
    fu! s:osc_52_yank() abort
        let seq = system('base64 -w0', @0)
        let seq = substitute(seq, '\n$', '', '')
        let seq = '\e]52;c;' . seq . '\x07'
        if !empty($TMUX)
            let seq = '\ePtmux;' . substitute(seq, '\\e', '\\e\\e', 'g') . '\e\\'
        endif
        let tty = matchstr(system('ls -l /proc/'.getpid().'/fd/0'), '/dev/pts/\d\+')
        sil exe '!printf -- ' . shellescape(seq, 1) . ' > ' . tty
    endfu

    augroup test_sth
        au!
        au TextYankPost * if v:event.operator is# 'y' | call s:osc_52_yank() | endif
    augroup END

> silent exe "!echo -ne ".shellescape(buffer)." > ".shellescape("/dev/pts/0")

One possible improvement in the code would  be to escape characters such as `!`,
`#` and `%`, which  are considered as special when you run  the `:!` command, by
passing a  non-zero number as a  second argument to `shellescape()`,  invoke the
latter once instead of twice, and use `$ printf` instead of `$ echo`:

    silent exe "!printf -- ".shellescape(buffer." > /dev/pts/0", 1)
    "            ^^^^^^ ^^                                       ^

If you  can use `system()` instead  of `:!`, then  you don't need to  escape the
special characters `!`, `#`, `%`, but I'm not sure it would work.

# ?

Document how we can get the number of colors supported by the terminal.

`$ tput colors` is not reliable, because it relies on `$TERM` which could lie.
`:echo &t_Co` is even less reliable.

To determine whether the terminal supports:

   - more than 256 colors, you can run our custom script `$ truecolor`
   - 256 colors, you can run our custom script `$ palette`
   - a given color, you could try:

            $ printf '\e]4;%d;?\a' 123 | if read -d $'\a' -s -t 1; then echo 'color 123 is supported'; fi

Understand how the last command works:

        https://unix.stackexchange.com/a/23789/289772

# ?

Look for all the places where we wrote a raw sequence in our plugins:

        vim /\%(\\033\|\\e\)[[\]P]/gj ~/.vim/**/*.vim ~/.vim/**/vim.snippets ~/.vim/vimrc

When possible, try to use `tput` instead.

# ?

Try to always use \033, instead of \e.

Why?
Easier to grep. Fewer matches when we have an issue with a terminal capability.

# ?

`infocmp rxvt-unicode-256color` gives weird sequence for `rmcup`:

        \E[r\E[?1049l

Should we use it instead of the one we're currently using in `vim-term`?

        \E[?1049l

# ?

Do this:

        # open a tmux pane
        $ tput Cs
        the cursor becomes pink~

        # get back to Vim, and press `coC` twice:
        # the cursor becomes black

        # get back to the shell tmux pane:
        # the cursor becomes pink

        # get back to Vim, and press `coC` twice:
        # the cursor becomes black

        # open another tmux pane:
        # the cursor becomes pink

        # close all tmux panes, except the one where Vim is
        # get back to Vim, and press `coC` twice:
        # the cursor becomes black

        # open another tmux pane:
        # the cursor stays black

# ?

To restore the color of the cursor, you can try this:

        $ tput Cs '#373b41'

Find a way to make `coC` more reliable.

# ?

Study:

        :lh \cterm\%(info\|cap\) (in Neovim and maybe in Vim)

# ?

To read:

        https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
        https://github.com/neovim/neovim/issues/6978
        https://github.com/neovim/neovim/pull/3165
        https://misc.flogisoft.com/bash/tip_colors_and_formatting

# ?

Finish summarizing this:

        https://www.linusakesson.net/programming/tty/

   [breakdown 1][1]

A user  types at a  terminal (a  physical teletype). This terminal  is connected
through  a  pair  of  wires  to a  UART  (Universal  Asynchronous  Receiver  and
Transmitter) on the computer. The operating  system contains a UART driver which
manages the  physical transmission  of bytes, including  parity checks  and flow
control. In a  naïve system, the  UART driver  would then deliver  the incoming
bytes directly to some application process. But  such an approach would lack the
following features:

        - line editing
        - session management

Line editing.

Think of it as a primitive kernel-level `sed`.

Most users make mistakes while typing,  so a backspace key is often useful. This
could be implemented by the applications  themselves, but in accordance with the
UNIX design philosophy, applications should be kept as simple as possible.

So as  a convenience, the operating  system provides an editing  buffer and some
rudimentary editing commands (backspace, erase word, clear line, …), which are
enabled by default inside the line discipline. Advanced applications may disable
these features by putting the line discipline in raw mode instead of the default
cooked mode.

Most interactive applications  (editors, mail user agents,  shells, all programs
relying on curses or readline) run in  raw mode, and handle all the line editing
commands  themselves. The line  discipline also  contains options  for character
echoing and  automatic conversion between carriage  returns and linefeeds.


Session management.

    - The user  probably wants  to run several  programs simultaneously,  and
      interact with them one at a time.
    - If a program goes into an endless loop,  the user may want to kill it or
      suspend it.
    - Programs that are started in the background should be able to execute
      until they try to write to the terminal, at which point they should be
      suspended.
    - User input should be directed to the foreground program only.

The operating system implements all these features in the TTY driver.

The TTY driver  is a passive object. It  contains some data and  methods, but it
can only do  something when one of its  methods gets called from a  process or a
kernel interrupt handler. The line discipline is likewise a passive entity.

The combination of a:

    - UART driver
    - line discipline instance
    - TTY driver

may be referred to as a TTY (device).

A  user  process  can affect  the  behaviour  of  any  TTY by  manipulating  the
corresponding device file under `/dev`. Write permissions to the device file are
required, so when a user logs in on  a particular TTY, that user must become the
owner of  the device file. This  is traditionally  done by the  `login` program,
which runs with root privileges.

Let's move on to a typical desktop  system. This is how the Linux console works:

   [breakdown 2][2]

The TTY  driver and line discipline  behave just like in  the previous examples,
but there  is no UART  or physical  terminal involved anymore. Instead,  a video
terminal (a  complex state machine  including a  frame buffer of  characters and
graphical character attributes)  is emulated in software, and rendered  to a VGA
display.

The console subsystem is somewhat rigid. Things get more flexible (and abstract)
if we  move the terminal emulation  into userland. This is how  xterm(1) and its
clones work:

        breakdown 3

To facilitate moving  the terminal emulation into userland,  while still keeping
the TTY  subsystem (session management  and line discipline) intact,  the pseudo
terminal or pty was invented. And as you  may have guessed, things get even more
complicated when you start running  pseudo terminals inside pseudo terminals, à
la screen(1) or ssh(1).

Now let's take a step back and see how all of this fits into the process model.

##
# Reference

[1]: $MY_WIKI/graph/terminal/breakdown_1.pdf
[2]: $MY_WIKI/graph/terminal/breakdown_2.pdf
[3]: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Operating-System-Commands

