# Why don't you use `kitty` atm?

<https://github.com/kovidgoyal/kitty/issues/214>

I think the fonts are not properly  rendered on an old monitor with a resolution
of 1920x1080: the glyphs look too “thin”.
There's no aliasing.

We should wait for a monitor with a better resolution, or for `kitty` to support
aliasing.

Update:

Maybe we could use a thicker font?

From: <https://github.com/kovidgoyal/kitty/issues/214#issuecomment-419317498>

> If you like thicker fonts, why not just use a font with a thicker stem size?
> It seems  backwards to  me to get  the font rendering  subsytem to  jump through
> hoops just to thicken your fonts.
> Different typefaces have  different design characteristics and IMO  it should be
> the job of the rendering system to render them as accurately as possible.
> Otherwise font designers will never be able  to rely on rendering systems to get
> rendering right.

Read this: <http://webagility.com/posts/finding-the-best-programming-font>

---

Update: could this fix the issue?

<https://github.com/kovidgoyal/kitty/pull/1604>

##
# Installation

<https://github.com/kovidgoyal/kitty/issues/595#issuecomment-504260295>

# Comparison with `urxvt`

I think we should get rid of `urxvt`:

   - I don't want to learn perl to customize the terminal
   - there's no easy way to report bug
   - it doesn't seem to support ligature
   - I can't fix the weird bug with some math symbols which are not rendered

[Kitty](https://github.com/kovidgoyal/kitty) seems a better/more modern/more powerful alternative:

   - we could customize it with python
   - it supports ligatures
   - it supports truecolors (not a watered-down version like urxvt)

However, the compilation is tricky at the moment:
<https://sw.kovidgoyal.net/kitty/build.html>

# Ligatures

   - <https://github.com/ToxicFrog/Ligaturizer>
   - <https://github.com/tonsky/FiraCode>
   - <https://www.reddit.com/r/urxvt/comments/728naa/does_anyone_know_how_to_enable_ligatures/>
   - <https://www.reddit.com/r/vim/comments/8n41zb/how_did_she_do_this_vim/dzsmlt4/>

To test `DejaVu Sans Mono` with ligature support, dl this file:
<https://github.com/ToxicFrog/Ligaturizer/blob/master/output-fonts/LigaDejaVuSansMono.ttf>

Then:

    $ cd Downloads/
    $ sudo cp LigaDejaVuSansMono.ttf /usr/share/fonts/truetype/dejavu

Then, you'll need to configure your terminal emulator so that it uses this font.
Its name is: `Liga DejaVu Sans Mono`.

You can find all your fonts with:

    $ fc-list V

##
# Issues
## I can't attach to a running tmux session from a kitty terminal!

You need to copy the terminfo description of kitty inside `~/.terminfo/x/`:

<https://github.com/kovidgoyal/kitty/issues/320#issuecomment-364820455>

I don't know why.
Try to understand.

    $ cp ~/Vcs/kitty/terminfo/x/xterm-kitty ~/.terminfo/x/

## The background of the terminal bleeds into my Vim color scheme background!

In Vim, the background of some lines  may be wrongly erased and painted with the
background of the terminal color scheme (instead of the Vim color scheme).
Put this in your vimrc:

    let &t_ut = ''

For more info:

    man terminfo /bce
   - <https://sunaku.github.io/vim-256color-bce.html>
   - <https://sw.kovidgoyal.net/kitty/faq.html#using-a-color-theme-with-a-background-color-does-not-work-well-in-vim>

## When I change the lightness of the color scheme, sometimes, the text in the tabline is underlined!

Yep, but I haven't tried to understand this issue yet, sorry.

## The `M-1` key binding (tmux restore session) doesn't work in kitty!

Yes, for some reason, `1` doesn't seem to be a valid key for a key binding in kitty.

Try this in `~/.config/kitty/kitty.conf`:

    map a send_text normal hello

Then press `a`; it will send `hello`.
Now, try this key binding:

    map 1 send_text normal hello

Then press `1`; it doesn't send anything.

I don't know how to fix this issue...

