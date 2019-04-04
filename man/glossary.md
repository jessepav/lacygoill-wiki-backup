# c
## command

There are two kinds of roff commands, possibly with arguments:
requests and escape sequences.

##
# e
## escape sequence

In-line – or even in-word – formatting element or function which can modify text
lines.

It's recognized by a leading backslash.

##
# l
## control Line vs text Line

There are only two kinds of lines in a groff document:
control lines and text lines.

The control  lines start  with a  control character,  by default  a period  or a
single quote; all other lines are text lines.

They  represent commands,  optionally  with arguments,  and  have the  following
syntax:

    .command_name arg1 arg2 ...

Text lines represent the parts that is printed.

##
# m
## macro

The user can define their own formatting commands using the `de` request.
These commands are called macros, but they are used exactly like requests.

For more info about the `de` request,  run `$ info gtroff`, then search the node
“gtroff Reference”, then the subnode “Writing Macros”.

## macro package

Pre-defined set of macros written in the groff language.

##
# r
## request

Roff command written on its own line, starting with a dot or a single quote.

## roff, nroff, troff, groff

roff is  the general  name for a  set of text  formatting programs,  known under
names like  nroff, troff,  groff, ditroff,  etc.  A roff  system consists  of an
extensible  text formatting  language and  a set  of programs  for printing  and
converting to other text formats.

The most common  roff system today is groff, which  implements the look-and-feel
and functionality of troff, with many extensions.

