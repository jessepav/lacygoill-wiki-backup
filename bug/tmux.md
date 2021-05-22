# Feature request: add an `-R` flag to `bind-key` to repeat only 1 key

I would like to make more key bindings repeatable.
The current way to do so is to pass the `-r` flag to `bind-key`.
Unfortunately, it frequently leads to unexpected behavior.

Here's one example.
I have these repeatable key bindings to resize panes:

set -g repeat-time 1000
bind -r C-h resizep -L 5
bind -r C-j resizep -D 5
bind -r C-k resizep -U 5
bind -r C-l resizep -R 5

I would like to make `)` and `(` repeatable, and so I install these key bindings:

bind -r ( switchc -p
bind -r ) switchc -n

I frequently want to have a look at a window in another session, so I press the prefix key followed by `)` to focus the next session, then I press `)` again to focus my main session again (I only have 2 sessions).

Update: Ah crap.  It's more complex.  You don't want `-R` to repeat only 1 key, but a particular subset of keys.
Do we want sth like `vim-submode` but for Tmux?

##
# copy-pipe

`copy-pipe` sometimes truncates the selection when piping it to `xsel(1x)`.

I have this key binding which worked well when I was using urxvt as my terminal:

bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard'

Its purpose is to copy the tmux selection into the X clipboard selection.

Now, I'm using st, and I've noticed that the text in the clipboard is truncated after approximately 375 characters.
I think the real number depends on the terminal window width and/or the font size, but I could be wrong.

Here's a MWE which I've tested against Ubuntu 16.04, as well as Ubuntu 18.04 (in a virtual machine).

    $ sudo apt-get update
    $ sudo apt-get install curl git libx11-dev libxft-dev pkg-config xsel
    $ git clone https://git.suckless.org/st
    $ cd st
    $ make
    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src
    $ ./st

# don't include that section in your bug report

    $ cd ..
    $ git clone https://github.com/tmux/tmux
    $ cd tmux

# would this command have worked instead? `$ sudo aptitude build-dep tmux`

    $ sudo apt-get install automake libevent-dev libncurses5-dev
    $ sh autogen.sh
    $ ./configure
    $ make

    $ tmux -Lx -f/dev/null new
    $ tmux set -gw mode-keys vi
    $ tmux bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard'
    $ vim -Nu NONE
    :echo repeat('x', 370) . ' this text should not be truncated'
    C-b [
    kVkkkkk
    y

The Vim command:

    :echo repeat('x', 370) . ' this text should not be truncated'

will output a string of 370 `x` characters on the command-line, followed by the text ` this text should not be truncated`.  The purpose of the motions in copy-mode (`kvkkkkk`) is to select all the characters in this string.

When I try to paste the contents of the X clipboard (in a Vim compiled with the clipboard feature, one can do so by pressing `"+p`), I correctly get 370 characters `x`, but ` this text should not be truncated` is truncated right after ` this`.

## Possible cause

I think the issue is due to an interaction between `copy-pipe` and the st terminal.

It's not due to `copy` (without `-pipe`), because this key binding always works as expected:

    $ tmux bind -T copy-mode-vi y send -X copy-selection

That is, it copies the previous long string in a tmux buffer, without truncation.

And it's specific to st, because I can't reproduce in xterm.

## Wrong hypotheses
### The issue is in `xsel(1X)`

At first, I thought that the issue was due to `xsel(1x)`, because the latter had [a bug](https://github.com/kfish/xsel/issues/13) in the past, which truncated the selection after 4000 characters.  It was fixed by [this PR](https://github.com/kfish/xsel/pull/16).

But this old bug can't be the cause of the current issue, because I've recompiled `xsel(1x)` to get the most recent version.  Besides, I can reproduce with `xclip(1)` too.

In fact, it doesn't even matter to which command you pipe the tmux selection.  You can use a non existing command, and tmux will send it to the X clipboard selection (but still truncate it after around 375 characters).
I checked this with the following key binding:

    $ tmux bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'not_a_command'
                                                                ^^^^^^^^^^^^^

I have no idea what tmux is piping the selection to, though.

### ?

Make some tests with any of these key bindings:

    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'xclip -selection clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'xsel -i --clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'xclip -selection clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'xsel -i --clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

I think the  issue is in an interaction  between `copy-pipe[-and-cancel]` and st.
Indeed, I can't reproduce with `cat(1)` :

    bind -T copy-mode-vi Z send -X copy-pipe 'cat >/tmp/test'

### ?

Find a MWE.

It seems the limit is 376 characters.
Run this:

    :echo repeat('a', 375) . 'bb'

Enter copy-mode and try to copy the 377 characters.
Paste it in a buffer (`""p`), and you'll see that the last `b` is replaced by a backtick.
You can add as many `b` as you want; when you paste, you'll only get one `b` + a backtick.
Weirdly enough, if  you try to reproduce  by writing the text in  a file, then
cat'ing  it in  the shell,  you'll  see that  the  limit is  increased to  379
characters.

But it can't be this, because we've updated xsel, and because we can reproduce
with xclip too.

Update:
Try to install a key binding which  would first simply copy the selection in a
tmux buffer:

    $ tmux bind -T copy-mode-vi Z send -X copy-selection-and-cancel

Now, try to make  the key binding manually invoke `xsel(1x)`  or `xclip(1)` in a
second step.

Does it work?
If it does, you've found a workaround (still, maybe you should report the issue).
If it doesn't, try to install a  key binding which would just call `xsel(1x)` or
`xclip(1)` with a long text.
Does it succeed in populating the clipboard selection?
If it doesn't you've found a simpler MWE.
If it does, this is weird... keep investing.

    ✘
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'
    ✔
    $ tmux bind Z run 'xsel -i --clipboard </tmp/file'

MWE:

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src
    $ git clone https://git.suckless.org/st
    $ cd st
    $ make
    $ ./st
    $ tmux -Lx -f/dev/null new
    $ tmux set -gw mode-keys vi
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'
    $ vim -Nu NONE
    :echo repeat('a', 375) . repeat('b', 10)
    C-b [
    kkkk0
    Vjjj
    Z

Note that `set -gw mode-keys vi` is necessary to make sure that, in copy-mode,
tmux uses the emacs key table, and not the vi one.
This is  because tmux chooses between the  emacs key table vs the vi one based on
the value of the `mode-keys` option.
Also, the motions to select the text depend  on the font size and the width of
the terminal window (and don't press `v` to start the selection, but `V`).
Finally, `tee(1)`  is provided  by the  coreutils package, which  seems to  be a
fundamental package.  So, it should be ok to use it in a MWE.

### ?

Interestingly enough, the next key binding works:

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </home/user/Vcs/tmux/COPYING'

Which seems to  indicate that the issue  is *not* linked to copy  mode, but to
*some* commands in copy mode.

Try to update the previous MWE, to reduce the difference between these commands
(the first one must work, but not the second):

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </home/user/Vcs/tmux/COPYING'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

    ⇒

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </tmp/file'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

to continue...

### ?

I found a workaround:

    bind-key -T copy-mode-vi y run "tmux send -X copy-pipe-and-cancel 'xsel -i --clipboard';"
                                                                                           ^

Notice the semicolon at the end.  It fixes the issue.
This key binding should be roughly equivalent:

    bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard' \; run ':'
                                                                                          ^

And yet, it doesn't fix the issue.  Why?
And why do we need `;` in the first working key binding?

Note that we can't use `;` in the second key binding, because tmux would complain:

    $ tmux bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard' \\\; run ';'
    usage: run-shell [-b] [-t target-pane] shell-command˜

But `:` should have the same effect; i.e. none.
From `man bash /SHELL BUILTIN COMMANDS`:

   > : [arguments]
   >        No effect; the command does nothing beyond  expanding  arguments
   >        and  performing any specified redirections.  A zero exit code is
   >        returned.

### ?

Ask this question to nicm:

   > If it's not a bug in tmux, could you explain:

   > - why do I need to add a trailing `true(1)` statement?
   > - why does the seemingly equivalent workaround fail?
   > - is it a general issue;
   >   i.e. do I need a trailing `true(1)` statement + a `run-shell`, every time I use copy-pipe?

### ?

In Vim, it seems that st doesn't need xsel.
How is that even possible?

It even works when we pipe the tmux selection to a non-existing command

    bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'not_a_command'

### ?

How to use OSC 52 to set the clipboard with arbitrary text?

    $ printf '\e]52;c;%s\x07' $(printf 'hello' | base64)

This should work in tmux too, provided that the outer terminal has the `Ms` capability.

Also, to better understand OSC 52, read this:
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05928.html>
<https://sunaku.github.io/tmux-yank-osc52.html>
<https://medium.freecodecamp.org/tmux-in-practice-integration-with-system-clipboard-bcd72c62ff7b>

Explanation regarding the special argument `-` (used in a command in one of the previous links):
<https://unix.stackexchange.com/questions/41828/what-does-dash-at-the-end-of-a-command-mean>

Security concern:
<https://bugzilla.gnome.org/show_bug.cgi?id=795774#c2>
<https://github.com/mintty/mintty/issues/258>

See also: `OSC Ps ; Pt ST /Ps = 5 2`

---

Issue: if one day we need to sync  a remote and local clipboards via OSC 52, and
we use st, we're limited to around 378 characters.
How to increase this limit?

Solution:

    $ sed -i.bak 's/^\(#define\s\+ESC_BUF_SIZ\s\+(\)[0-9]*\(\*UTF_SIZ)\)/\11024\2/' ~/GitRepos/st/st.c
                                                                           ├──┘
                                                                           └ the default value is 128

Adapt the new max to the max used by the yank script:

74994

Btw, where does this max come from?

Answer: Read the script.
It says that the sequence has a header of 7 bytes (`\e]52;c;`) plus a footer of 1 byte (`\a`) – btw, that's not true in tmux, where those are a little longer – so 99992 bytes remains out of a max of 100000 bytes.
And it mentions a formula (`4 * ceil(n/3)`) which I think gives the size of the base64 encoding of an input string of size `n`.  So, 74994 is the input size to which the encoding is 99992 bytes.

And if you wonder where does the 100000 come from, I think it's an arbitrary max size followed by tmux.
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05950.html>
In the previous comment, sunaku mentions a link (now dead), which I guess mentions this limit.
But nicm explains that xterm doesn't define any limit.
So, 100000 is an arbitrary number.

### ?

To understand st weird behavior regarding the clipboard, read this:

<https://github.com/tmux/tmux/issues/1119>
<https://github.com/tmux/tmux/issues/1407>

### ?

Make some tests to check our understanding of what happens with st.
That is, in urxvt, `xsel(1x)` should be running to own the selection.
But in st,  `xsel(1x)` should not be running,  since st is the last  one to have
written in the X clipboard; so st  should be the owner, `xsel(1x)` is not needed
anymore, therefore it should not be running.

Update: Yes, it's confirmed.
Run tmux in st, then run `ls(1)`, and copy the output in tmux copy mode.
Finally, run `$ ps aux | grep xsel`: there's no xsel process.

Repeat the experiment in urxvt.  This time, there is a xsel process.

### ?

Document that if  the clipboard doesn't contain what you  expect (after using an
OSC 52 sequence), you should inspect all the selections:

    $ xsel -p (primary)
    $ xsel -s (secondary)
    $ xsel -b (clipboard)

### final solution

We've fixed the issue by increasing the value `ESC_BUF_SIZ` in `~/GitRepos/st/st.c:37`

By default, it's:

    128 * UTF_SIZ
    =
    128 * 4
    =
    512

In the patch `~/.config/st/patches/10_big_clipboard.diff`, we increase it to:

    25000 * UTF_SIZ
    =
    100000

Why `100000`?

Because after  a bug  report was  submitted to  nicm (tmux  dev), tmux  allows a
maximum size of 100K bytes for an escape sequence.

Relevant excerpts from the original issue:

Question:

   > However, since the maximum length of an OSC 52 escape sequence is
   > **100,000** bytes[1] and the patched tmux's DCS escape sequence length
   > limit is 32772 bytes (as observed above), how would you recommend
   > sending a maximum-length OSC 52 escape sequence through tmux?

Answer:

   > Actually looking at xterm it doesn't have a limit for this escape
   > sequence, we can probably make tmux's a lot bigger so long as we reduce
   > it back to 32 bytes after the sequence is done.

<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05949.html>
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05950.html>

---

Document all of this in `~/.config/st/patches/README.md`.

##
# `#{pane_status_dead}` sometimes wrongly empty
### Issue description

To reproduce, run these shell commands:

    $ cat <<'EOF' >/tmp/tmux.conf
    bind -T copy-mode-vi x send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"{}\"'"
    EOF
    $ tmux -Lx -f/tmp/tmux.conf
    $ ls | tmux splitw -dI \; set -w remain-on-exit on \; splitw 'aaa'
    C-b :display '#{pane_dead_status}'

The output of the last command is empty, but it should be `127`.

I don't  know why, but  the issue seems  to be due to  this key binding  (and in
particular to the double quotes surrounding the url passed to `xdg-open(1)`):

    bind -T copy-mode-vi x send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"{}\"'"
                                                                                        ^^  ^^

Update:
Forget about this bug for the moment.
I can't reproduce it reliably.
It depends on sth else; I don't know what.

### Required information

- `$ tmux -V`: tmux next-3.1
- `$ uname -sp`: Linux x86_64
- terminal: xterm
- `$TERM` outside tmux: xterm-256color
- `$TERM` inside tmux: screen
- logs from `$ tmux -vv -Lx -f/tmp/tmux.conf`:

