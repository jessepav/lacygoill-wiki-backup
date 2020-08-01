# Introduction

Markdown is a text-to-HTML conversion tool for web writers.
Markdown lets you write using  an easy-to-read, easy-to-write plain text format,
then convert it to structurally valid XHTML (or HTML).

Thus, “Markdown” is two things:

        - a plain text formatting syntax

        - a software tool, written in Perl, that converts the plain text
          formatting to HTML.

See the Syntax page for details pertaining to Markdown's formatting syntax.
You can try it out, right now, using the online Dingus.

The overriding  design goal for  Markdown's formatting syntax  is to make  it as
readable as possible.
The idea is  that a Markdown-formatted document should be  publishable as-is, as
plain text,  without looking like  it's been marked  up with tags  or formatting
instructions.
While Markdown's  syntax has  been influenced  by several  existing text-to-HTML
filters, the single  biggest source of inspiration for Markdown's  syntax is the
format of plain text email.

The best way to get a feel for Markdown's formatting syntax is simply to look at
a Markdown-formatted document.
For example, you can view the Markdown  source for the article text on this page
here:

        http://daringfireball.net/projects/markdown/index.text

You  can use  this ‘.text'  suffix trick  to view  the Markdown  source for  the
content of each of the pages in this section, e.g. the Syntax and License pages.

##
# Installation and Requirements

Markdown requires Perl 5.6.0 or later.
Markdown also  requires the standard  Perl library module Digest::MD5,  which is
probably already installed on your server.

## Blosxom

Markdown works with Blosxom version 2.0 or later.

 1. Rename the “Markdown.pl” plug-in to “Markdown” (case is important).
    Blosxom forbids plug-ins to  have a “.pl” extension.

 2. Copy the “Markdown” plug-in file to your Blosxom plug-ins folder.
    If you're  not sure where your  Blosxom plug-ins folder is,  see the Blosxom
    documentation for information.

 3. That's it.
    The entries in your weblog will now automatically be processed by Markdown.

 4. If you'd  like to apply  Markdown formatting  only to certain  posts, rather
    than  all of  them,  Markdown can  optionally be  used  in conjunction  with
    Blosxom's Meta plug-in.

    First, install the Meta plug-in.

    Next,  open  the  Markdown plug-in  file  in  a  text  editor, and  set  the
    configuration variable $g_blosxom_use_meta to 1.

    Then, simply  include a  “meta-markup: Markdown” header line  at the  top of
    each post you compose using Markdown.

##
# Configuration

By default, Markdown produces XHTML output for tags with empty elements.
E.g.:

<br />

Markdown can be configured to produce HTML-style tags; e.g.:

<br>

## Command-Line

Use the --html4tags command-line switch to produce HTML output from a Unix-style
command-line.

E.g.:

    % perl Markdown.pl --html4tags foo.text

Type perldoc Markdown.pl,  or read the POD documentation  within the Markdown.pl
source code for more information.

##
# Utilities
## html2text

Utility for turning HTML into Markdown-formatted plain text.

https://github.com/Alir3z4/html2text/
https://github.com/Alir3z4/html2text/blob/master/docs/usage.md

## Blosxom

https://en.wikipedia.org/wiki/Blosxom

---

https://github.com/zakame/blosxom

        Blosxom - the Zen of Blogging, resurrected

https://github.com/mattn/blogo

        blosxom like blog server

https://github.com/pyblosxom/pyblosxom

        Pyblosxom file-based blogging engine

