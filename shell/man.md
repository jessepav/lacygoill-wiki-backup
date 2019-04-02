# ?

Where does the name “roff” come from?

[From the expression “to run off a copy”][1].

[Which means “to quickly print a copy of something”][2].

[“off” is used because the copy comes off the machine][3].

# ?

roff is  the general  name for a  set of text  formatting programs,  known under
names like  troff, nroff,  ditroff, groff,  etc.  A roff  system consists  of an
extensible  text formatting  language and  a set  of programs  for printing  and
converting to other text formats.

The most common roff system today  is the free software implementation GNU roff,
groff, which  implements the look-and-feel  and functionality of  its ancestors,
with many extensions.

# ?

Although nroff was  developed before troff, from the user's  point of view, both
systems are similar: ditroff and groff each emulate both of them.

# ?

Study how to write manpages

It's explained in the Appendix A of the "Classic Shell Scripting" book.
To check the formatting of a manual page, run either of these:

    $ groff -man -Tascii program.man | less
    $ groff -man [-Tpdf] program.man | zathura -
             │
             └ shorthand for `-m man`
               include the macro package `man`

To install a  manpage, move your `program.man` file (containing  the source code
in groff) in `~/share/man/man1/`.
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

Update: you can see `~/share/man` in the output of `$ manpath`.
`~/share/man` is not used because of some config in `/etc/manpath.config`,
because even after removing all the contents of this file and running `$ sudo mandb`,
`$ manpath` still includes `~/share/man`.

Anyway, version control `~/share/man`.

Also, if you want to draw table in a manpage, you probably need to read `$ man tbl`.
For pictures and equations, see also `$ man pic` and `$ man eqn`.


##
# Reference

[1]: https://www.definitions.net/definition/troff
[2]: https://www.macmillandictionary.com/dictionary/british/run-off
[3]: https://forum.wordreference.com/threads/make-a-copy-of-and-run-off-a-copy-of.1604451/#post-8065490
