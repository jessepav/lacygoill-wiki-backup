# Where can I find groff's
## complete documentation?

    $ info groff

## short but complete reference?

    $ man 7 groff

There's another manpage for groff in section 1; don't conflate the two.

## list of the escape sequences for all special glyphs?

    $ man 7 groff_char

##
# How to make Vim apply the `nroff` filetype to my `pgm.1` file?

Write a dot at the start of one of the first 5 lines, then reload the buffer.
`dist#ft#FTnroff()` in `$VIMRUNTIME/autoload/dist/ft.vim:318` will do the rest.

##
# Readability
## Why should I write a newline after every text sentence?

This  tells  groff  to  use  inter-sentence  spacing,  which  is  important  for
[proportionally-spaced][1] output formats.

I think you can notice a difference when you convert the document to pdf:

    $ groff -man mypgm.1 | zathura -

The spacing  between two sentences  is slightly bigger  in the pdf  when they're
separated by a newline in the groff document.

---

It also makes life easier for translators (reading a diff is easier for them and
you).

## Why can't I use indentation in a groff document nor spacing to make it more readable?

Most groff requests must appear at the beginning of a line, in the form of a dot
followed by one or two letters or digits.
Besides, in groff  documents, spaces and blank lines are  significant: two input
spaces produce (approximately) two output spaces.

##
## My groff document is too dense.  How should I add an empty line to make it more readable?

Use an undefined request (lone dot).

    ... long sentence ends.
    .
    long sentence begins...

## How can I write a comment in groff?

Write a backslash-quote.

However, this  will still produce  a line terminator in  the output; to  make it
disappear  prefix the  comment  with a  dot,  so that  it  becomes an  undefined
request:

    .\" some comment
    │
    └ ignore the line terminator in the output

## How to make it easier to spot a section heading?

Use a comment line of equals sign:

    .\" ========================================================

##
# Escape Sequences
## Where can an escape occur?

Anywhere in the input to gtroff.

## What are the first two characters of an escape, usually?

A  backslash  then a  single  character,  which  indicates  the function  to  be
performed.

### If it requires an identifier as a parameter, what are the three possible syntax forms?

   - The next single character is the identifier.

   - If this single character is an opening parenthesis, take the following two
     characters as the identifier.  Note that there is no closing parenthesis
     after the identifier.

   - If this single character is an opening bracket, take all characters until
     a closing bracket as the identifier.

Examples:

    \fB
    \n(XX
    \*[TeX]

---

Other escapes may require several arguments and/or some special format.
In  such cases  the argument  is traditionally  enclosed in  single quotes  (and
quotes are always used in this manual for the definitions of escape sequences).
The enclosed text is then processed according to what that escape expects.

Example:

    \l'1.5i\(bu'

##
## How to write
### a hyphen?

    \-

#### Why shouldn't I simply write `-`?

It looks better typeset than the shorter ordinary hyphen does.
Especially when the code is converted into a pdf.

###
### two consecutive hyphens?

    \-\^\-

#### What's the thing in the middle?

An escape sequence standing for a 1/12th em space.

It's ignored for TTY output devices (rounded to zero).

##### How is it useful?

It prevents the hyphens from running together in Troff output.
In Nroff output, the space will disappear.

When the  groff code is  converted into  a pdf, you  can see that  `\^` slightly
increases the gap between the previous and the next character.

###
### a literal backslash?

Use the  escape sequence  defined for  this purpose:

    \(rs

Mnemonic: Reverse Slash.

### a literal dot at the start of a line?

Use the escape sequence `\&` representing  a zero-width space, to get the period
away from the beginning of the line (which is the only place where it is treated
specially):

    \&.

###
### an em-dash?

Use the macro `\(em`, which is documented at `$ man 7 man-pages`.

#### How is it rendered on an ASCII terminal?

As two hyphens.

##### In other typographical contexts?

As a long dash.

##
# Requests
## How to pass an argument containing whitespace to a groff request?

Use double-quotes to surround it.

###
## What's the name of the request which starts every manpage?

    .TH

### What does it mean?

Text Header

### What are the four arguments it accepts?

   - an uppercased command name
   - a manual section number
   - a revision date (optional)
   - a version number (optional)

#### What are they used for?

They construct the page headers and footers in the formatted output document:

    $ zcat /usr/share/man/man1/bash.1.gz | grep '\.TH'
    .TH BASH 1 "2014 February 2" "GNU Bash 4.3"~

    $ man bash
    BASH(1)                     General Commands Manual                    BASH(1)~
    ...~
    GNU Bash 4.3          2014 February 2          BASH(1)~

###
## What's the name of the request which starts a section?

    .SH

### What does it mean?

Section Heading

### What is the single argument it expects?

The name of the section, quoted if  it contains spaces, and uppercased to follow
manual-page conventions:

    .SH NAME

###
## How is the body of the NAME section of a manpage used by some utilities?

It provides fodder for `$ apropos` – or  equivalently `$ man -k`.

### What should it contain?

It should be exactly one line long, without trailing punctuation.
It takes the form `command — description`.

###
## What's the request to typeset some text in a bold fontface?

.B

### When does its effect stop?

Until the end of the line.

For example:

    .B foo bar
    baz

Here, `foo bar` will be typeset in bold, but not `baz`.

### How to write `mypgm [ --help ]` with every character in bold, except the brackets?

    .B mypgm
    [
    .B \-\^\-help
    ]

We split the `mypgm [ --help ]` on 4 lines to prevent `.B` from operating on the brackets.

##
# Misc.
## Where does the name “roff” come from?

[From the expression “to run off a copy”][2].

[Which means “to quickly print a copy of something”][3].

[“off” is used because the copy comes off the machine][4].

##
##
##
# ?

Let's understand this request:

    .if t .ti +\w'\fBpathfind\fP\ 'u

---

By experiment, we  find that the nroff  ASCII output has a line  break after the
--version option, but since we are in paragraph mode, the next line continues at
the left margin.
That is  objectionable here, so we  put in a conditional  statement that applies
only to nroff, and is ignored by troff .
It uses  the temporary  indentation command  ( .ti  ) with  an argument  of +9n,
meaning to indent  nine spaces, which is  the width of the command  name, plus a
trailing space, in a fixedwidth font:

---

The indentation  amount is  more complex  because with  a proportional  font, we
don't know the width of the command name and one following space.
The  \w'...'u command  measures  the width  of the  material  inside the  single
quotes.
Because  that text  is  set in  a  bold font,  we use  an  inline font  wrapper,
\fB...\fP, meaning switch to  a bold font, and then switch  back to the previous
font.
There are similar font-switching commands for roman ( \fR ), italic ( \fI ), and
fixed-width ( \fC ) fonts.
The C stands for Courier, a widely used fixed-width font dating back to the days
of manual typewriters.

##
# ?

Document that you  when find a word/expression which you  don't understand in an
info page, you most  probably can find it in the index of  one of the appendices
at the bottom.

For example, in `$ info groff`, one can read this after searching for `\.ti`:

> This request causes a break; its value is associated with the
> current environment (*note Environments::).  The default scaling
> indicator is 'm'.  A call of 'ti' without an argument is ignored.

What is a “scaling indicator”?

Jump to the bottom of the page, and search backward for `scaling indicator`:

> * scaling indicator:                     Measurements.        (line   6)

Now, you know that the info is at `$ info -n Measurements groff`.

# ?

Some  escape sequences  take arguments  separated by  single quotes,  others are
regulated by a length encoding introduced  by an open parenthesis or enclosed in
square brackets.

# ?

The following information/questions stem from reading “Write The Fine Manual”.

What's the `an` macro package?
What does it provide?

See `man 7 man` for more info.

---

What's the groff/an syntax?
How is it different than groff alone?

---

Is roff a markup language or a typesetting language?
What's the difference?

---

In `.SH SYNOPSIS`, `SYNOPSIS` is an argument of `.SH`.

---

Character sequences beginning with a backslash are escape sequences.
These often consist of a left parenthesis followed by two characters.

    Copyright \(co 2005 Quux \fIItalics\fP Inc.
              ├──┘
              └ escape sequence

# ?

The second section gives  a brief synopsis of the command  line that invokes the
program; it begins with the expected heading:

    .\" ========================================================
    .SH SYNOPSIS

and is  followed with a  sometimes lengthy  markup display that  provides mostly
font information:

    .B    pathfind
    [
    .B    \-\^\-all
    ]
    [
    .B    \-\^\-?
    ]
    [
    .B    \-\^\-help
    ]
    [
    .B    \-\^\-version
    ]

The program name, and options, are set in a bold font.

The fontswitching requests, such as `.B` , expect up to six arguments (quoted if
they contain spaces), and then typeset them adjacent to one another.

When there  are multiple arguments, this  means that any spacing  needed must be
explicitly supplied.

Here, the square brackets  are in the default roman font;  in manual pages, they
delimit optional values.

Although  we could  have put  the closing  and opening  brackets of  consecutive
options on the same  line, we prefer not to because  having each option complete
on three consecutive lines facilitates editing.

The font-pair escape  sequences to be introduced shortly could  shrink them to a
single line, but they are rarely used in option lists.

# ?

Study how to write manpages

It's explained in the Appendix A of the "Classic Shell Scripting" book.
To check the formatting of a manual page, run either of these:

    $ groff -man -Tascii program.man | less
    $ groff -man [-Tpdf] program.man | zathura -
             │
             └ shorthand for `-m man`
               include the macro package `man`

To install a manpage, move your `program.man` file in `~/share/man/man1/`.
Name it following this scheme: `<program>.<section>`:

    $ cp program.man ~/share/man/man1/program.1

After the first invocation of `$ man <program>`, the file
`~/share/man/cat1/<program>.<section>.gz` will be created.

Maybe you should invoke  `$ sudo mandb` before the first  invocation of `$ man`,
but I'm not sure it's necessary.

---

Why does `$ man` look into `~/share/man` even though it's not in `$MANPATH`?

    https://askubuntu.com/a/244810/867754
    https://askubuntu.com/a/633924/867754
    man 1 manpath
    man 5 manpath

Update: you can see `~/share/man` in the output of the `$ manpath` command.
`~/share/man` is not used because of some config in `/etc/manpath.config`,
because even after removing all the contents of this file and running `$ sudo mandb`,
`$ manpath` still includes `~/share/man`.

Anyway, version control `~/share/man`.

Also, if you want to draw table in a manpage, you probably need to read `$ man tbl`.
For pictures and equations, see also `$ man pic` and `$ man eqn`.
`tbl`, `pic` and `eqn` are preprocessors.

##
# Reference

[1]: https://en.wikipedia.org/wiki/Typeface#Proportion
[2]: https://www.definitions.net/definition/troff
[3]: https://www.macmillandictionary.com/dictionary/british/run-off
[4]: https://forum.wordreference.com/threads/make-a-copy-of-and-run-off-a-copy-of.1604451/#post-8065490
