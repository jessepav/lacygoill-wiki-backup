# ?

Document the fact that you can make  terminal.sexy export a scheme to st (select
Simple Terminal).

# ?

Document that you can start st with an arbitrary geometry with the `-g` option.
For fullscreen, try:

    $ st -g=274x77

##
# Read the faq

<https://git.suckless.org/st/file/FAQ.html>

# Read arch wiki

<https://wiki.archlinux.org/index.php/St>

# Watch this video

<https://www.youtube.com/watch?v=9H75enWM22k>

##
# Fix the error messages related to unknown sequences when we start tmux from st.

Start st from another terminal, so that the error message is printed there.

Example of error:

    erresc: unknown str ESC]112ESC\

Update:

I've fixed the issue by temporarily  disabling the Cs and Cr terminfo extensions
in tmux.conf:

    if-shell '[ "$TERM" != "st-256color" ]' 'set -as terminal-overrides ",*:Cs=\E]12;%p1%s\007:Cr=\E]112\007"' ''
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

But I think  it means that we  can't change the color of  the cursor dynamically
from a program (like Vim).

Is it an issue?
It probably breaks our `coC` Vim mapping when we switch to a dark colorscheme.

See here for a patch which adds support to the OSC12 sequence:
<https://www.reddit.com/r/unix/comments/8tjcen/how_to_change_the_color_of_the_vim_cursor_in_st/e192px6/>

    --- st.c.orig       2018-06-25 11:15:17.934818947 +0200
    +++ st.c    2018-06-25 12:41:28.419547222 +0200
    @@ -1854,6 +1854,20 @@
                        if (narg > 1)
                                xsettitle(strescseq.args[1]);
                        return;
    +           case 12:
    +                   if (narg == 2)
    +                   {
    +                           int j = atoi(strescseq.args[1]);
    +
    +                           if (j >= 0 && j < ncolors)
    +                           {
    +                                   defaultcs = j;
    +                                   redraw();
    +                                   return;
    +                           }
    +                   }
    +                   fprintf(stderr, "erresc: invalid OSC 12 use\n");
    +                   return;
                case 52:
                        if (narg > 2) {
                                char *dec;
    --- st.h.orig       2018-06-25 11:25:03.116919565 +0200
    +++ st.h    2018-06-25 12:44:03.547830166 +0200
    @@ -121,3 +121,5 @@
     extern unsigned int tabspaces;
     extern unsigned int defaultfg;
     extern unsigned int defaultbg;
    +extern unsigned int defaultcs;
    +extern unsigned const int ncolors;
    --- config.def.h    2018-03-20 21:29:59.000000000 +0100
    +++ config.h        2018-06-25 12:44:24.711323373 +0200
    @@ -111,6 +111,7 @@
        "#555555",
     };

    +unsigned const int ncolors = sizeof(colorname)/sizeof(*colorname);

     /*
      * Default colors (colorname index)
    @@ -118,7 +119,7 @@
      */
     unsigned int defaultfg = 7;
     unsigned int defaultbg = 0;
    -static unsigned int defaultcs = 256;
    +unsigned int defaultcs = 256;
     static unsigned int defaultrcs = 257;

     /*

##
# Which patches should we apply?

<https://st.suckless.org/patches/bold-is-not-bright/>

Review the other patches.

# Why does st uses the `dch1` capability for the delete key?

Press C-v then Del; it prints `^[[P`.

    $ infocmp -x | grep dch1
    cvvis=\E[34l, dch=\E[%p1%dP, dch1=\E[P, dim=\E[2m,~
    kcud1=\EOB, kcuf1=\EOC, kcuu1=\EOA, kdch1=\E[3~,~

urxvt and xfce4-terminal use the `kdch1` capability...

##
# Patches
## How to use the Xresource file to configure st?

Download it from here:
<https://st.suckless.org/patches/xresources/>

Fix the index of the foreground, background, and cursor colors:

    $ sed -i '/background/s/[0-9]\+/0/; /foreground/s/[0-9]\+/7/; /cursorColor/s/[0-9]\+/256/' /path/to/patch.diff

Finally, apply it:

    $ patch </path/to/patch.diff

---

The latest version atm is:
<https://st.suckless.org/patches/xresources/st-xresources-20190105-3be4cf1.diff>

The header of the patch reads:
> Subject: [PATCH] Update base patch to 0.8.1

Which means that it should work on st version 0.8.1.
I've tested it against 0.8.2, and it still works.

The patch sets  the foreground, background, and cursor colors,  with the indices
256, 257, 258, while [it should use 0, 7 and 256][1].

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

You can test this issue by running `$ infocmp`.
If the output is not readable, it's because you didn't fix the patch.
Although, for  some reason, the issue  is not present inside  tmux (even without
any tmux config).

### Why should I avoid this patch?

It provides little benefit: a compilation takes little time.

It adds complexity: I have a hard time  understanding which color is going to be
applied when configuring `config.h`.

It can lead to bugs if you don't fix it, like we explained earlier.

Even after being fixed, the arguments of a command are invisible.
This is due to our zsh syntax highlighting plugin.
More specifically, this line:

    ZSH_HIGHLIGHT_STYLES[default]='fg=black'

I found one – weird – solution:

    ZSH_HIGHLIGHT_STYLES[default]='fg=white'
                                      ^^^^^

Or:

    ZSH_HIGHLIGHT_STYLES[default]='fg=7'
                                      ^

It probably means that sth is wrong in our patched `config.h`.

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
the  latter  is  created by  `$  make`,  and  the  latter does  *not*  duplicate
`config.def.h` into `config.h` if it already exists.

Another solution is to  remove `config.h`, but then you lose  all the values you
changed (like the colors for example).

## ?

<https://st.suckless.org/patches/fix_keyboard_input/>

This patch breaks the Enter key.
When you press Enter, it inserts `09 5u` on the command-line.

## ?

Image preview is buggy.
The image often disappears when you move to another file then come back.
<https://github.com/ranger/ranger/issues/856>

You could try to increase the value of `st.xfps` to 300 or higher:
<https://github.com/ranger/ranger/issues/759#issuecomment-276355995>

##
# Reference

[1]: https://github.com/dcat/st-xresources/issues/3#issue-394957047

