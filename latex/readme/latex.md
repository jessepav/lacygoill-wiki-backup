# Installation
## What's TeX Live?

The most popular LaTeX distribution on linux atm.

## How to remove an old installation before updating it?

Try this:

        $ rm -rf ~/texlive/

TODO: Is it really enough?

        https://tex.stackexchange.com/a/95502/169646

##
## How to install it?
### manually

        $ mkdir ~/texlive/
        $ cd /tmp && mkdir texlive && cd texlive

        $ wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
        $ xt install-tl-unx.tar.gz
        $ TEXLIVE_INSTALL_PREFIX=~/texlive/ ./install-tl
        # press i to install
        # wait ≈ an hour for the installation to complete

Why setting `$TEXLIVE_INSTALL_PREFIX` to `~/texlive/` ?

By default, the script will install texlive in a root directory (`/usr/local/`).

But it's better to install it in your  home, because it will allow you to manage
your packages  via `tlmgr` without `sudo`,  and without having to  configure the
`$PATH` of the root user.

        # `$PATH`, `$MANPATH`, `$INFOPATH`
        # should contain the path to your texlive distribution
        $ cat <<'EOF' >>~/.zshenv

        export PATH=$HOME/texlive/2018/bin/i386-linux:$PATH
        export MANPATH=$HOME/texlive/2018/texmf-dist/doc/man:$MANPATH
        export INFOPATH=$HOME/texlive/2018/texmf-dist/doc/info:$INFOPATH
        EOF

        $ sudo aptitude install perl-tk

`perl-tk` is necessary to start `tlmgr` in GUI via `$ tlmgr --gui`.

Source: https://tug.org/texlive/distro.html#perltk

---

For more info, see:

    https://www.tug.org/texlive/doc/texlive-en/texlive-en.html
    OR
    ~/texlive/2017/texmf-dist/doc/texlive/texlive-en/texlive-en.pdf

    https://www.tug.org/texlive/acquire-netinstall.html
    http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz

### via aptitude

        $ sudo aptitude install texlive-full

Can take a lot of space (3-5 gigs) and some time (twenty minutes).

##
## Why is a manual installation better?

With  a manual  installation, your  texlive  distribution is  more complete  and
up-to-date.

---

In particular, it includes the package `tikz-3dplot`, which, atm, is not present
when you install texlive via `aptitude`.

You can find a use case for `tikz-3dplot` in this plot:

        http://www.texample.net/tikz/examples/spherical-polar-pots-with-3dplot/

Just replace this line:

        \usepackage{3dplot}

                →

        \usepackage{tikz-3dplot}

###
## What's latexmk?

It's a  perl script  for running LaTeX  the correct number  of times  to resolve
cross references,  etc; it  also runs auxiliary  programs (bibtex,  makeindex if
necessary, and dvips and/or a previewer as requested).

It has a number  of other useful capabilities, for example  to start a previewer
and then run latex whenever the source  files are updated, so that the previewer
gives an up-to-date view of the document.

## How to install it?

It should be included in your TeX Live distribution.
However, if you want to download it manually, do it from here:

        http://personal.psu.edu/jcc8//software/latexmk-jcc/

Then, move it in `~/bin`.

To be notified when a new version is released, you could subscribe to this rss feed:

        https://www.ctan.org/ctan-ann/atom/latexmk.xml

## How to configure it?

Use one of these files:

        $HOME/.latexmkrc
        $XDG_CONFIG_HOME/latexmk/latexmkrc

##
# Commands
## What are the main purposes of commands?

Some  of them  generate output  (like `\section`),  others set  properties (like
`\documentclass`).

## How are commands named?

They all begin with a backslash.

Most of them are descriptive and use small letters.
Some of them consist only of a backslash + a non-letter character.
Some of them contain upper case alphabetic characters (ex: \LaTeX).

## What's the syntax to use a command?

        \command[optional argument]{mandatory argument}

## What's the simplest syntax to define a new command?

        \newcommand{\mymacro}{my text}

## What's the syntax to define a new command accepting three arguments?

                                 ┌ the code here could be arbitrarily complex
                                 │
                                 │ for example, you could format the second argument
                                 │ in bold with `\textbf{#2}`
                                 │
                                 │ or you could add “hello” between the first
                                 │ and second arguments
                                 │
                                 ├──────┐
        \newcommand{\mymacro}[3]{#1 #2 #3}
                             ├─┘
                             └ this second argument passed to `\newcommand` is OPTIONAL,
                               hence the square brackets instead of the curly brackets

                               it stands for the number of mandatory arguments
                               your new command expects

                               if you don't provide it, LaTeX will assume
                               your new command expects NO argument

                               you can provide any integer between 1 and 9


`#1`, `#2`,  `#3` will be replaced  with the first, second,  third arguments you
pass to `\mymacro`:

        \mymacro{foo}{bar}{baz}

## What's the general syntax to define a new command?

        \newcommand{\name}[n][default]{definition}

---

        name

The name of the new command, using:

   - lowercase and/or uppercase letters
   - a single non-letter symbol

The new command must not be already defined and its name is not allowed to begin
with `end`.

---

        n

An integer from 1 to 9.
It's the number of arguments of the new command.

If omitted, the command will have no arguments.

---

        default

If this is  present, then the first  argument would be optional,  and by default
its value would be `default`.

Otherwise all arguments are mandatory.

---

        definition

Every occurrence  of the  command will  be replaced  by `definition`,  and then,
every occurrence of the form `#n` will be replaced by the nth argument.

## How to load a package?

        \usepackage{mypackage}

This will load the package `mypackage`, and read in all of its definitions.
From now on, we may use all commands contained in that package.

## Why isn't a space printed in the output when it's right after a command?

The space(s) after a command is  interpreted as a separation between the command
and the following text.


To solve this issue, escape the space:

        \latex  is great    ✘
        \latex\ is great    ✔
              ^

## How to prevent a space after a macro to be “consumed”?

Load  the `xspace`  package  in the  preamble via  `\usepackage`,  then use  the
`\xspace` command in the definition of the macro.

Example:

                    ┌ package
                    │
        \usepackage{xspace}
        \newcommand{\mymacro}{my text\xspace}
                                      │
                                      └ command

`\xspace` inserts a space depending on the following character:

   - if it's a normal letter, `\xspace` will  insert a space
   - if it matches  [.,!?]    `\xspace` won't insert a space

##
# Declarations
## What's the scope of a declaration?

It depends on what its immediate surroundings are:
a command, a group or an environment.

The scope of a declaration begins from where it's placed until:

   - the end of the command argument    in which it's used
   - the end of the group               "
   - the end of the environment         "

   - the next conflicting declaration if there's one

Example:

        \tiny hello \Huge world
                    │
                    └ the scope of \tiny ends here

## How to convert a declaration into an environment?

        \declaration

                ⇔

        \begin{declaration}
        \end{declaration}

## How to limit the scope of a declaration?

Place it inside a group, by surrounding it with curly braces:

        foo {\sffamily bar} baz

Or, convert it into an environment:

        foo \begin{sffamily} bar \end{sffamily} baz

## Should I prefer groups or environments?

Using  environments   instead  of   braces  might   make  complex   code  easily
understandable.

## Can I nest groups?

Yes:

        Normal text, {\sffamily sans-serif text {\bfseries and bold}}.

##
# Fonts
## What are the main families of fonts?

   - serif / roman
   - sans-serif
   - monospaced / typewriter

## Which usage are the serif/roman fonts good for?

Serif  typefaces  have  historically  been credited  with  increasing  both  the
readability and reading speed of long passages of text because they help the eye
travel across a line, especially if lines  are long or have relatively open word
spacing (as with some justified type).

Others dispute this viewpoint, asserting that what we read most (serif text), we
read best.
This might very well account for the popularity and dominance of serif typefaces
in the U.S.
for lengthy text in print, including books and newspapers.

## Which usage are the sans-serif fonts good for?

For shorter text settings – such  as captions, credits, column headings, as well
as text in charts and graphs.
Its  simplified letterforms  are unencumbered  by serifs,  which can  impede the
readability of characters at very small sizes.

They are also good for low resolution screens.

## Which usage are the monospaced/typewriter fonts good for?

Code and urls.

All the letters of a monospaced font have the same width.

## Which family of font should I use?

Many sans-serif  typefaces exist  that are  more legible at  any size  than some
serif designs.
So whichever style  you choose, take note of the  particular characteristics and
overall  legibility of  the design,  including specific  weights and  upright vs
italic.

## How to change the font family of some text?

    ┌──────────────┬───────────────┬─────────────┐
    │ font         │ command       │ declaration │
    ├──────────────┼───────────────┼─────────────┤
    │ roman        │ \textrm{}     │ \rmfamily   │
    ├──────────────┼───────────────┼─────────────┤
    │ sans-serif   │ \textsf{}     │ \sffamily   │
    ├──────────────┼───────────────┼─────────────┤
    │ typewriter   │ \texttt{}     │ \ttfamily   │
    ├──────────────┼───────────────┼─────────────┤
    │ default font │ \textnormal{} │ \normalfont │
    └──────────────┴───────────────┴─────────────┘

## How to change the size of the text?

Use one of these declarations:

   - \tiny
   - \scriptsize
   - \footnotesize
   - \small
   - \normalsize
   - \large
   - \Large
   - \LARGE
   - \huge
   - \Huge

## Do \tiny & friends always produce the same font size?

No it depends on the base font.

For example,  if your  document has  a base font  of 10  pt, then  `\tiny` would
result in a text smaller than with a base font of 12 pt.

## Can I use a declaration changing the shape or the size of the text in the body?

Yes,  but usually  you  will only  use  them  in definitions  of  macros in  the
preamble, because they're quite low-level commands.

A notable exception are freely designed passages like title pages.

## Can I combine any font properties?

It depends on the chosen font.

For  instance, fonts  with small  caps combined  with variations  like bold  and
italic are rare.

## Why should I avoid using the term 'roman'?

It's too vague.

It has at least three distinct meanings in different areas.

   1. It can mean upright instead of italic, and potentially of regular weight
      as well (as opposed to light or bold).

   2. It can mean the style of Roman inscriptions. The typefaces Trajan, Weiss
      and Optima are Roman in this sense.

   3. When talking about character sets, it can refer to Latin (as opposed to
      Greek, Cyrillic or other alphabets) and even specifically a Latin-1 or
      Western European character set of some sort.

So, don't use the term “roman”. Instead write:

   1. upright

   2. classical Roman or Roman inscriptional

   3. western European or Latin-1

##
# Formatting
## How to choose a class for the document?

        \documentclass{my class}

To be used in the preamble.

## How to apply a style to some text?

    ┌────────────┬───────────┬─────────────┐
    │ style      │ command   │ declaration │
    ├────────────┼───────────┼─────────────┤
    │ bold-faced │ \textbf{} │ \bfseries   │
    │ medium     │ \textmd{} │ \mdseries   │
    ├────────────┼───────────┼─────────────┤
    │ italics    │ \textit{} │ \itshape    │
    │ upright    │ \textup{} │ \upshape    │
    ├────────────┼───────────┼─────────────┤
    │ slanted    │ \textsl{} │ \slshape    │
    ├────────────┼───────────┼─────────────┤
    │ small caps │ \textsc{} │ \scshape    │
    ├────────────┼───────────┼─────────────┤
    │ emphasized │ \emph{}   │ \em         │
    └────────────┴───────────┴─────────────┘

`\mdseries`  cancels  `\bfseries`
`\upshape`   cancels  `\itshape`

## Can two styles be combined?

Yes, you can always nest two commands to apply two styles to some text:

        This text is \textit{\textbf{bold-faced and in italics}}.

Also, two styles mean emphasizing twice which might be a questionable choice.
Change the font shape wisely, and consistently.

## How is the output affected by the insertion of additional spaces/line breaks between words?

It's not.

You can include as many spaces between words as you want, and you can break your
lines in as many lines as you want, the output will stay the same.

## What's the effect of a single line break in the source code?

The same as a space.

## How to add a line break in the output to separate two lines?

Use the `\\` command.

## How to add a paragraph break to separate two paragraphs?

Create a blank line.

Multiple blank lines are treated as one.
Like for spaces.

## How to suppress a paragraph indentation?

Use  the `\noindent`  declaration at  the  beginning of  the first  line of  the
paragraph.

Note that  there's no  need for `\noindent`  if the paragraph  is right  after a
heading: LaTeX doesn't indent the first line of such a paragraph.

## How to add some vertical space between two paragraphs?

Use the `\bigskip` command.

## How to print a TeX or LaTeX logo?

        \LaTeX
        \TeX

## How to print the title, author and date of the document in a formatted manner?

        \maketitle

These information must have been defined before via the commands:

   - \author
   - \title
   - \date

To be used in the preamble.

## How to print a heading?

        \section{some heading}

A heading is bigger than normal text and bold-faced.

## Do some characters need a special treatment to be included literally in the document?

Yes.

Some characters need to be escaped:

   - #
   - $
   - %
   - &
   - _
   - {
   - }

Technically,  we don't  really escape  them, we  execute special  commands whose
single purpose is to print a character.


The backslash is a special case, you must use this command:

        \textbackslash

## Changing the font size at the end of a paragraph should be done right after or before the break?

After:

        \begin{document}                    \begin{document}
        \begin{huge}                        \begin{huge}

        ...                                 ...
        ...                                 ...
        last line of paragraph   ┐          last line of paragraph   ┐
                                 │ ✔        \end{huge}               │ ✘
        \end{huge}               ┘                                   ┘
        another paragraph                   another paragraph
        \end{document}                      \end{document}


LaTeX uses the current  font size at the very end of a  paragraph to compute the
interline spacing between the latter and the previous/next paragraph.

If all your paragraph is written with a bigger than normal font, and you restore
the normal size BEFORE the break,  LaTeX will produce an interline spacing which
fits a paragraph written with a normal font size (which is not the case).

##
# Emphasizing
## What happens when I
### emphasize some text once?

By default, LaTeX typesets the text in italic shape.

###  emphasize some text twice?

Two emphasizing cancel out:

        \emph{some \emph{important} word}

                        ⇔

        \emph{some} important \emph{word}

The  rationale being  that  if  you typeset  an  important  theorem entirely  in
italics, you should still have the opportunity to highlight a word inside.
You can do so by re-emphasizing it.

### apply the same style twice?

Usually nothing:

        \textbf{\textbf{some text}}

                        ⇔

                \textbf{some text}

### apply two opposite styles to the same text?

The most local one wins:

        \textbf{text in bold \textmd{text in medium}}

        \textmd{text in medium \textbf{text in bold}}

##
## Is `\emph` semantic markup or visual markup?

It's semantic markup because it refers to  the meaning, not to the appearance of
the text.

## What is the slanted style?

It's just an oblique version of the normal font.

OTOH, the `italics` style has different letter shapes.

Btw, don't use the `slanted` style:

> Serif typefaces with a good slanted variant are extremely rare, so if you care
> about typography, you should stick to italics.

https://tex.stackexchange.com/questions/68931/what-is-the-difference-between-italics-and-slanted-text#comment147156_68932

##
# Miscellaneous
## What's the main reason to change the style of some text from the preamble rather than the body?

If  your  change  needs  to  affect  several  occurrences  of  the  text,  doing
it  by  creating  an  abstraction  from  the  preamble  is  more  efficient  and
reliable/consistent.

It's more efficient because you have less code to repeat.
A simple abstraction can be replaced by an arbitrarily complex formatting.

It's more reliable/consistent because, contrary to  you, LaTeX will never make a
mistake when replacing it.

A change from the preamble affects all the body: it's global.
A change  from the body  affects only the text  to which it's  directly applied:
it's local.

##
# Issues
## Are there bugs?

In `vimtex`, the  filename of an entry  in the qfl may be  wrongly prefixed with
Vim's working  directory, instead of  the path  to the directory  containing the
source code.

Because of this,  when we press Enter in  the qf window to jump to  an error, we
may end up in an irrelevant buffer.

MWE:

        $ cat /tmp/vimrc

                set rtp^=~/.vim/plugged/vimtex/
                set rtp+=~/.vim/plugged/vimtex/after

                filetype plugin indent on
                syntax enable

                let g:vimtex_matchparen_enabled = 0

                augroup open_qf_window
                    au!
                    au QuickFixCmdPost * nested copen
                augroup END

                let g:vimtex_compiler_latexmk = {
                    \ 'backend' : has('nvim') ? 'nvim' : 'jobs',
                    \ 'background' : 1,
                    \ 'build_dir' : '',
                    \ 'callback' : 1,
                    \ 'continuous' : 1,
                    \ 'executable' : 'latexmk.pl',
                    \ 'options' : [
                    \      '-pdf',
                    \      '-verbose',
                    \      '-file-line-error',
                    \      '-synctex=1',
                    \      '-interaction=nonstopmode',
                    \ ],
                    \}

                let g:tex_flavor = 'latex'


        $ cat ~/Downloads/file.tex

                \documentclass{article}
                \begin{document}
                Such commands can be \texit{\textbf{nested}}.
                                        ^ missing `t` (purposeful error)
                \end{document}


        $ vim -Nu /tmp/vimrc
        :e ~/Downloads/file.tex
        :VimtexCompileSS
        :copen


It should have been fixed:

        https://github.com/lervag/vimtex/issues/963

But I  can still  reproduce the  issue if I  install an  autocmd opening  the qf
window. I can fix the issue if I delay the opening though.

Try to submit a bug report.
If it's fixed one day, remove the delay we've introduced in:

        ~/.vim/plugged/vim-qf/autoload/qf.vim:639



Old alternative solutions:

Try to configure `latexmk` (or `pdftex`) so that it displays absolute paths.


Or try to use `pplatex` to parse the logfile.
`pplatex` is  a command-line  utility used  to pretify the  output of  the LaTeX
compiler:

        https://github.com/stefanhepp/pplatex

To use it:

        let g:vimtex_quickfix_method = 'pplatex'

You  may  need  to  tweak  `g:vimtex_compiler_latexmk`  and  remove  the  option
`-file-line-error`  from the  dictionary. Maybe `vimtex`  does it  automatically
though. See :h g:vimtex_quickfix_method.


Or  try to  write a  filter  which would  replace  all the  relative paths  with
absolute paths, tweak 'makeprg' and submit a PR.


Or try to tweak  the mapping starting the compilation, so that  it `:lcd` in the
directory of the current file before compiling.

#
# TODO

[texlive-en.pdf](~/texlive/2018/texmf-dist/doc/texlive/texlive-en/texlive-en.pdf)

https://github.com/lervag/vimtex/issues
https://github.com/honza/vim-snippets/blob/master/UltiSnips/tex.snippets
https://github.com/honza/vim-snippets/blob/master/UltiSnips/texmath.snippets

http://dante.ctan.org/tex-archive/info/luatex/lualatex-doc/lualatex-doc.pdf (short guide to luatex)

http://cremeronline.com/LaTeX/minimaltikz.pdf (Minimal introduction to TikZ)

http://detexify.kirelabs.org/classify.html  (draw a symbol in the browser and get the corresponding macro)
http://www.texample.net/tikz/examples/      (examples of graphs)
https://www.latextemplates.com/             (examples of templates)

https://www.overleaf.com/blog/571-an-introduction-to-luatex-part-1-what-is-it-and-what-makes-it-so-different#.WrF8AHXwYrg

---

Interresting LaTeX package:

    https://ctan.org/pkg/pythontex
    Run Python from within a document, typesetting the results

---

Document these commands:

        x_|c    compile selection
        n_|c    single shot compilation
        n_|C    continuous compilation

        n_|ec   edit latexmkrc

        n_|n    clean some auxiliary files
        n_|N    clean all auxiliary files

        n_|s    stop continuous compilation of current file
        n_|S    stop continuous compilation of all files

        n_|v    view compiled file
        n_|V    view compiled selection


Also, document the  fact that when you  compile a visual selection,  it must NOT
include the  preamble. Otherwise, you won't  get the expected result.   It seems
vimtex adds the preamble at the beginning of the file automatically.

Also, according to  `:h VimtexCompileSelected`, you could add  a custom operator
to compile a text-object:

        When  used  as  a normal  mode  mapping,  the  mapping  will act  as  an
        |operator| on the following motion or text object. Finally, when used as
        a visual mode mapping, it will act on the selected lines.

Try sth like this:

        nmap  |?  <plug>(vimtex-compile-selected)
               ^
               replace with whatever key you want

