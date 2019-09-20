# Why don't you use `kitty` atm?

        https://github.com/kovidgoyal/kitty/issues/214

I think the fonts are not properly  rendered on an old monitor with a resolution
of 1920x1080: the glyphs look too “thin”.
There's no aliasing.

We should wait for a monitor with a better resolution, or for `kitty` to support
aliasing.

Update:

Maybe we could use a thicker font?

From:

    https://github.com/kovidgoyal/kitty/issues/214#issuecomment-419317498

> If you like thicker fonts, why not just use a font with a thicker stem size?
> It seems  backwards to  me to get  the font rendering  subsytem to  jump through
> hoops just to thicken your fonts.
> Different typefaces have  different design characteristics and IMO  it should be
> the job of the rendering system to render them as accurately as possible.
> Otherwise font designers will never be able  to rely on rendering systems to get
> rendering right.

Read this:

    http://webagility.com/posts/finding-the-best-programming-font

##
# Installation

        $ git clone https://github.com/kovidgoyal/kitty && cd kitty

        $ make
        python3 setup.py
        CC: gcc (5, 4)
        Package harfbuzz was not found in the pkg-config search path.
        Perhaps you should add the directory containing `harfbuzz.pc'
        to the PKG_CONFIG_PATH environment variable
        No package 'harfbuzz' found
        harfbuzz >= 1.5 is required, found version: not found
        Makefile:9: recipe for target 'all' failed
        make: *** [all] Error 1

---

        $ apt-cache policy libharfbuzz-dev
        libharfbuzz-dev:
        Installed: (none)
        Candidate: 1.0.1-1ubuntu0.1
        Version table:
            1.0.1-1ubuntu0.1 500
                500 http://fr.archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages
                500 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages
            1.0.1-1build2 500
                500 http://fr.archive.ubuntu.com/ubuntu xenial/main amd64 Packages

---

https://github.com/harfbuzz/harfbuzz/blob/master/BUILD.md

> On Linux, install the development packages for FreeType, Cairo, and GLib.
> For example, on Ubuntu / Debian, you would do:
>
>        sudo apt-get install gcc g++ libfreetype6-dev libglib2.0-dev libcairo2-dev

---

        $ sudo apt-get install libfreetype6-dev libcairo2-dev
        Reading package lists... Done
        Building dependency tree
        Reading state information... Done
        Some packages could not be installed. This may mean that you have
        requested an impossible situation or if you are using the unstable
        distribution that some required packages have not yet been created
        or been moved out of Incoming.
        The following information may help to resolve the situation:

        The following packages have unmet dependencies:
        libfreetype6-dev : Depends: libfreetype6 (= 2.6.1-0.1ubuntu2.3) but 2.8.1-2 is to be installed
        E: Unable to correct problems, you have held broken packages.

---

        $ sudo apt-get install libfreetype6=2.6.1-0.1ubuntu2.3
            # ✔
        $ sudo apt-get install libfreetype6-dev
            # ✔
        $ sudo apt-get install libcairo2-dev
            # ✔

---

Download latest tarball:

https://www.freedesktop.org/software/harfbuzz/release/

        $ ./configure
        $ make
        $ sudo checkinstall

---

In kitty directory:

        $ make

        Package xkbcommon-x11 was not found in the pkg-config search path.
        Perhaps you should add the directory containing `xkbcommon-x11.pc'
        to the PKG_CONFIG_PATH environment variable
        No package 'xkbcommon-x11' found
        The package xkbcommon-x11 was not found on your system
        Makefile:9: recipe for target 'all' failed
        make: *** [all] Error 1

---

        $ sudo aptitude install libxkbcommon-x11-dev

---

        $ make
            # ✔

---

If you have more issues, read this:

        https://github.com/kovidgoyal/kitty/issues/180
        https://github.com/kovidgoyal/kitty/commit/11b17c09ced4577f5c1464fe1d040bda22972c77

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

        https://sw.kovidgoyal.net/kitty/build.html

# Ligatures

        https://github.com/ToxicFrog/Ligaturizer
        https://github.com/tonsky/FiraCode
        https://www.reddit.com/r/urxvt/comments/728naa/does_anyone_know_how_to_enable_ligatures/
        https://www.reddit.com/r/vim/comments/8n41zb/how_did_she_do_this_vim/dzsmlt4/

To test `DejaVu Sans Mono` with ligature support, dl this file:

        https://github.com/ToxicFrog/Ligaturizer/blob/master/output-fonts/LigaDejaVuSansMono.ttf

Then:

        $ cd Downloads/
        $ sudo cp LigaDejaVuSansMono.ttf /usr/share/fonts/truetype/dejavu

Then, you'll need to configure your terminal emulator so that it uses this font.
Its name is:

        Liga DejaVu Sans Mono

You can find all your fonts with:

        $ fc-list V

##
# Issues
## I can't attach to a running tmux session from a kitty terminal!

You need to copy the terminfo description of kitty inside `~/.terminfo/x/`:

        https://github.com/kovidgoyal/kitty/issues/320#issuecomment-364820455

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

