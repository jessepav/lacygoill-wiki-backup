# Configuration
## How to create a color scheme for st?

Use [terminal.sexy][1], and export your scheme to st by selecting “Simple Terminal”.

## ?

Our current white color makes several things unreadable:

    $ rm -rf ...

This command is highlighted in a red background, and a white foreground.
But the white is grey.

Look also at the cmus interface.
And look at this:

    $ highlight -O ansi ~/bin/python/xkbmapd.py

The  issue  is  in  `~/.config/st/patches/01_custom_config.diff`;  we've  chosen
`#808080` for white.
We did this, because we've copied the value from `~/.Xresources`.
There was a reason.
See whether you can find a value which makes a white text always readable.

But this is weird...
Why does the same hexcode makes cmus readable in urxvt, but not in st?

##
## patches to apply
### ?

Which patches should we apply?

<https://st.suckless.org/patches/bold-is-not-bright/>

Review the other patches.

### ?

Explain how to create a patch.
I.e. create a temporary branch, commit, edit files, and run `$ git diff`.

###
## patches to avoid
### clipboard

<https://st.suckless.org/patches/clipboard/>

It seems it only makes us lose the  ability to paste some selected text from the
browser into the terminal via middle click.
It's inconsistent with all other terminal emulators we're using.
So, don't use it.

### fix keyboard input

<https://st.suckless.org/patches/fix_keyboard_input/>

This patch breaks the Enter key.
When you press Enter, it inserts `09 5u` on the command-line.

###
### Xresources
#### How to use it?

<https://st.suckless.org/patches/xresources/>

Fix the index of the foreground, background, and cursor colors:

    $ sed -i '/background/s/[0-9]\+/0/; /foreground/s/[0-9]\+/7/; /cursorColor/s/[0-9]\+/256/' /path/to/patch.diff

Finally, apply it:

    $ patch </path/to/patch.diff

---

The latest version atm is:
<https://st.suckless.org/patches/xresources/st-xresources-20190105-3be4cf1.diff>

The header of the patch reads:
>     Subject: [PATCH] Update base patch to 0.8.1

Which means that it should work on st version 0.8.1.
I've tested it against 0.8.2, and it still works.

The patch sets  the foreground, background, and cursor colors,  with the indices
256, 257, 258, while [it should use 0, 7 and 256][2].

If you don't fix the patch, these colors will be wrong.
That is, the only way to set the background color of st like in urxvt is to have
these lines:

                             v
    unsigned int defaultbg = 0;
    ...
    { "background",   STRING,  &colorname[0] },
                                          ^

Same thing for the foreground and cursor colors.

Besides, without the fix, when the output of a command contains a tab character,
it will occupy almost a whole line on the terminal.
This is because there's no color indexed by 258 in the array `*colorname[]`:

    ...
    "cyan",
    "white",

    [255] = 0,

    /* more colors can be added after 255 to use with DefaultXX */
    [256] = "#cccccc",
    [257] = "#555555",

You can test this issue by running `infocmp(1)`.
If the output is not readable, it's because you didn't fix the patch.
Although, for  some reason, the issue  is not present inside  tmux (even without
any tmux config).

#### Why should I avoid it?

It provides little benefit: a compilation takes little time.

---

It adds complexity: I have a hard time  understanding which color is going to be
applied when configuring `config.h`.

---

It can lead to bugs if you don't fix it, like we explained earlier.

---

Even after being fixed, the arguments of a command are invisible.
This is due to our zsh syntax highlighting plugin.
More specifically, this line:

    ZSH_HIGHLIGHT_STYLES[default]='fg=black'

I found one – weird – solution:

    ZSH_HIGHLIGHT_STYLES[default]='fg=white'
                                      ^---^

Or:

    ZSH_HIGHLIGHT_STYLES[default]='fg=7'
                                      ^

It probably means that sth is wrong in our patched `config.h`.

##
# Usage
## How to start st with an arbitrary geometry?

Use the `-g` option.

    $ st -g=<cols>x<rows>[{+-}<xoffset>{+-}<yoffset>]

For fullscreen in a 1080p screen, try:

    $ st -g=120x35

##
# Issues
## The compilation fails!

Did you apply a patch between now and the last successful compilation?

If so, run vimdiff on the `config.h` and `config.def.h` files.
If there are entirely new lines (not simple change of values), try to merge them
by pressing `dp`.

This is necessary, for example, if you build st, then apply the Xresource patch,
then try to rebuild.

The patch  adds new  lines into  `config.def.h`, but  not to  `config.h` because
the  latter  is  created  by  `make(1)`,  and  `make(1)`  does  *not*  duplicate
`config.def.h` into `config.h` if it already exists.

Another solution is to  remove `config.h`, but then you lose  all the values you
changed (like the colors for example).

## I'm trying to paste the primary selection by pressing the middle-click of the mouse.  It doesn't work!

If you're in tmux, press shift+middle-click.
Or, temporarily disable the mouse (`pfx M-m`).

See: <https://stackoverflow.com/questions/17445100/getting-back-old-copy-paste-behaviour-in-tmux-with-mouse>

## I'm trying to preview an image.  It constantly gets erased!

So, your issue is that the image  often [disappears][3] when you move to another
file then come back.

Solution: use [ueberzug][4] instead of w3mimgdisplay to preview an image:

    $ python3 -m pip install --user ueberzug
    $ sed -ibak '/set\s\+preview_images_method/s/.*/set preview_images_method ueberzug/' ~/.config/ranger/rc.conf

---

Alternatively, you  could try to [increase the value of `st.xfps`][5]  to 300 or
higher; but last time I tried, it didn't help.

You  can also  press `C-l`,  maintain the  key pressed  for a  short time,  then
release `l` (but maintain `Ctrl`).
The image should be redrawn.
But for some  reason, as soon as  you release `Ctrl`, the image  is erased again
(because of xcape which sends an Escape?).

##
# Todo
## Add support for hex colors in an OSC 12 sequence

When we change the cursor color from Vim (`coC`), it would be nice to be able to
use `#ab1234` or `rgb:ab/12/34`.

---

Also, try  to make Vim  read read the current  cursor color from  the terminal's
config:

   - `~/.Xresources`, /cursorColor
   - `~/.config/st/patches/01_custom_config.diff`, /defaultcs

And save it in a Vim global variable as soon as we start Vim.
Finally, make `toggle_settings.vim` use this  color when change the color scheme
back to its original state.

All of this would fix the following issue:
when we change the  color scheme, then get back to the  original one, the cursor
color is not properly restored.

## Implement OSC 112 to be able to restore the default cursor color

We don't really need this, but maybe it could be useful in the future.

See `~/.config/st/patches/99_osc_12.diff` for inspiration.
And this [reddit thread][6].

Once  you've implemented  it, update  your tmux.conf  to set  the `Cr`  terminfo
extension *un*conditionally:

    set -as terminal-overrides ',*:Cs=\E]12;%p1%s\007'
    if-shell '[ "$TERM" != "st-256color" ]' 'set -as terminal-overrides ",*:Cr=\\E]112\\007"' ''

    →

    set -as terminal-overrides ',*:Cs=\E]12;%p1%s\007:Cr=\E]112\007'

##
## Read the faq

<https://git.suckless.org/st/file/FAQ.html>

## Read the arch wiki

<https://wiki.archlinux.org/index.php/St>

## Watch this video

<https://www.youtube.com/watch?v=9H75enWM22k>

## Prevent `make(1)` from compiling the terminfo description into our local database.

I don't trust it.
I prefer to rely on the one from invisible-island.

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src

Note somewhere that we should remove these lines:

    tic -sx st.info
    @echo Please see the README file regarding the terminfo entry of st.

... from `~/Vcs/st/Makefile`.

This should be done automatically (with `sed(1)`), so we need to use a script.
Maybe use `upp`.

---

Why don't you trust this terminfo description?

When you look at the terminfo.src from invisible-island, you can read this:

>     Se and Ss are implemented in the source-code, but the terminfo
>     provided with the source is incorrect, since Se/Ss are mis-coded
>     as booleans rather than strings.

...

>     The source includes two entries which are not useful here:
>           st-meta| simpleterm with meta key,
>           st-meta-256color| simpleterm with meta key and 256 colors,
>     because st's notion of "meta" does not correspond to the terminfo definition.
>     Rather, it acts like xterm - when the meta feature is disabled.

It seems to indicate that the  terminfo description which comes with st's source
code is  not always correct... Search  for `\C\<st\>` in terminfo.src,  and read
the few reviews that you find.

---

After reading this: <https://github.com/tmux/tmux/issues/1264>
I wonder whether we should stick with the terminfo description from st source code.

And if you read this:
<https://github.com/tmux/tmux/issues/1593#issuecomment-460063051>
You may, yet again, change your mind:
>     The upstream st (which I've seen more than once comment suggesting as an improvement) also is incorrect.

---

Also, if you write a script to install st, make sure it runs `$ make clean`.
<https://github.com/tmux/tmux/issues/1264#issuecomment-397909842>

## join the irc `#suckless` channel

It would be useful to gather some useful tips/information organically over time.

- <https://suckless.org/community/>
- <https://www.oftc.net/>

This requires that you register your nick on the OFTC network.

##
# Reference

[1]: https://terminal.sexy/
[2]: https://github.com/dcat/st-xresources/issues/3#issue-394957047
[3]: https://github.com/ranger/ranger/issues/856
[4]: https://github.com/seebye/ueberzug
[5]: https://github.com/ranger/ranger/issues/759#issuecomment-276355995
[6]: https://www.reddit.com/r/unix/comments/8tjcen/how_to_change_the_color_of_the_vim_cursor_in_st/e197b3t/
