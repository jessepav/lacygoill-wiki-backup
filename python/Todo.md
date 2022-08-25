# Read these generic documents about Python

- <https://docs.python.org/3/tutorial/>
- <https://docs.python.org/3/faq/programming.html>
- <https://docs.python.org/3/howto/index.html>
- <https://docs.python.org/3/glossary.html>

##
# Learn these tools, and integrate them in our workflow
## black

Installation:

    $ python -m pip install --user --upgrade black

---

<https://github.com/psf/black>
<https://black.readthedocs.io/en/stable/usage_and_configuration/index.html>

When configuring `black`, you'll often need to choose a style over another.
Which implies that you need to know the pros and cons of each choice.
Read these style guides as references:
- <https://peps.python.org/pep-0008/>
- <https://google.github.io/styleguide/pyguide.html>

## pylint

Read this: <https://pylint.pycqa.org/en/latest/tutorial.html>
As well as the following user guide.

This command populates a default config file for `pylint`:

    $ pylint --generate-rcfile >>~/.pylintrc

Also, take inspiration from this config file from Google:
<https://google.github.io/styleguide/pyguide.html#21-lint>

---

Should we use flake8 instead?
That's the linter recommended by the "Learn Python Programming" book.
Is it easier to use?  faster?
It seems better maintained (much fewer open issues on GitHub).

- <https://github.com/PyCQA/flake8>
- <https://flake8.pycqa.org/en/latest/index.html>

## mypy

<https://mypy.readthedocs.io/en/stable/getting_started.html>

##
## pudb

`pdb` is a module which is built by default into the python interpreter.
`pudb` is a TUI front-end for `pdb`.
To install the latter:

    $ pip install pudb

- <https://www.youtube.com/watch?v=bJYkCWPs_UU>
- <https://documen.tician.de/pudb/#table-of-contents>
- <https://realpython.com/python-debugging-pdb/>

---

Here is an example of command that you  can run to debug `epy` without having to
modify the script:

    $ python -m pudb $(which epy) /home/lgc/VCS/kitty/docs/_build/epub/kitty.epub

### create a README file

    ~/.config/pudb/README

And version control its contents.

### finish customizing its color theme

    ~/.config/pudb/theme.py

### write a cheat sheet

Key bindings:

    ? = Help Menu
    C-P = Edit Preferences

Configuration settings are saved in `~/.config/pudb`.

Note  that  some keys  can  interact  with  the  command-line window  (e.g.  `+`
increases  its height),  but  only  if you  focus  its  `<Clear>` button  (press
`Right`).

##
# Customizations
## customize the tab bar in kitty

    ~/.config/kitty/tab_bar.py

There is a whole bunch of code which we don't understand yet in there.
Also, the comments need to be trimmed down, and moved into
snippets/cheatsheets/notes...

## customize conky to add a weather indicator

    ~/bin/conky-startup

<https://github.com/edusig/conky-weather>

##
# Assimilation
## understand the code in `yt-dlp-comments-prettifier`

    ~/bin/yt-dlp-comments-prettifier

## understand the code in the python scripts used in our subwiki dedicated to hacking

    $ fd . --extension=py ~/wiki/hacking
    ~/wiki/hacking/LiveOverflow/Binary_Exploitation_Memory_Corruption/03_Writing_a_simple_Program_in_Python/matrix.py
    ~/wiki/hacking/LiveOverflow/Binary_Exploitation_Memory_Corruption/07_Uncrackable_Programs_Key_validation_with_Algorithm_and_creating_a_Keygen_Part_1/fuzz.py
    ~/wiki/hacking/LiveOverflow/Binary_Exploitation_Memory_Corruption/07_Uncrackable_Programs_Key_validation_with_Algorithm_and_creating_a_Keygen_Part_1/keygen.py

## various Python programs which we use (we could rewrite some of them)

<https://libraries.io/pypi/ttrv>
Is that a legitimate/right link?

---

WeeChat plugins.
This short one can be used as a starting point:

    # 24 sloc
    ~/.config/weechat/python/toggle_time.py

---

interSubs:

    # 1370 sloc
    ~/.config/mpv/scripts/interSubs.disable/interSubs.py

    # 57 sloc
    ~/.config/mpv/scripts/interSubs.disable/interSubs_config.py

---

<https://github.com/wustho/epy>
Probably too difficult: 8857 sloc.

---

Do we keep using UltiSnips?
If so, try to assimilate this helper script:

    ~/.vim/pack/mine/opt/snippets/pythonx/snippetHelpers.py

