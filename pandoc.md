# Installation

Download the latest `.deb` here:
<https://github.com/jgm/pandoc/blob/master/INSTALL.md>

Install it:

    $ dpkg -i *.deb

Install any missing dependency:

    $ apt install /usr/bin/rsvg-convert

##
# Usage
## markdown → pdf

    $ pandoc input.md \
         -N \
         --pdf-engine=xelatex \
         --variable mainfont="DejaVu Sans Mono" \
         --variable sansfont="DejaVu Sans Mono" \
         --variable monofont="DejaVu Sans Mono" \
         --variable fontsize=12pt \
         --toc \
         -o output.pdf

Source: <http://pandoc.org/demos.html>

In particular, see the example #14.

##
# Issues
## I'm trying to compile a markdown file into pdf.  It fails with an error message (command unavailable...)!

If the error message looks like this:

        “Command \C unavailable in encoding TU”!

Read the error message to find which part of your original document caused the issue.
Then, quote it using backtick or a code block (indentation = 4 spaces or more).
Try to re-compile.

##
# TODO

Read the user manual:

        https://pandoc.org/MANUAL.pdf

