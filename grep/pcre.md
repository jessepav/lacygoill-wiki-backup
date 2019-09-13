# Installation

Download the latest release from here: <https://ftp.pcre.org/pub/pcre/>
If the link is dead, try to find a new one from here: <https://www.pcre.org/>

Note that you can compile two different programs: pcre and pcre2.
Choose pcre2, as it's probably more powerful.

Once the archive is downloaded, check its authenticity, extract it, then:

    $ ./configure
    $ make
    $ make check
    $ sudo rlwrap checkinstall

Installing the package is useful to get the manpages documenting the PCRE syntax.

## pcre2-utils

You may be interested in installing the package pcre2-utils.

    Description: New Perl Compatible Regular Expression Library - utilities

     This is  PCRE2, the new implementation  of PCRE, a library  of functions to
     support  regular expressions  whose syntax  and semantics  are as  close as
     possible to those of the Perl 5 language.
     New projects  should use this library  in preference to the  older library,
     confusingly called pcre3 in Debian.

     This  package  contains  the  utilities pcre2grep  (like  grep  with  PCRE)
     and  pcre2test  (a test  program  for  the  library,  but also  useful  for
     experimenting with regular expressions).
     Both programs are also useful examples of programming with libpcre2.

##
# What are the differences between PCRE2 and Perl regexes?

    man pcre2compat

##
# Documentation

For a quick reference, read:

    man pcre2syntax

For a complete reference, read:

    man pcre2pattern

Don't read these manpages as tutorials.
They're references.
If you  need a better  understanding of PCRE, learn  Perl regexes with  the book
“Mastering Regular Expressions”.

> Perl's  regular expressions are described in its own documentation, and
> regular expressions in general are covered in a number of  books,  some
> of  which  have  copious  examples. Jeffrey Friedl's "Mastering Regular
> Expressions", published by  O'Reilly,  covers  regular  expressions  in
> great  detail.  This  description  of  PCRE2's  regular  expressions is
> intended as **reference** material.

