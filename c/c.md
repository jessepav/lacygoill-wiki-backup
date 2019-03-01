# How to read “C Programming A Modern Approach”?

> I use a spiral approach, in  which difficult topics are introduced briefly, then
> revisited one or more times later in the book with details added each time.

> Material too advanced or too esoteric to interest the average reader.
> Questions of this nature are marked with an asterisk (*).

> Some  questions in  Q&A  sections  relate directly  to  specific  places in  the
> chapter; these  places are marked  by a special icon  to signal the  reader that
> additional information is available.

# ?

> Most C  compilers provide  language features and  library functions  that aren't
> part of the C89 or C99 standards.
> For portability,  it's best  to avoid using  nonstandard features  and libraries
> unless they're absolutely necessary.

Each compiler provides its nonstandard features not supported by C89/C99.
So, if you want  your C code to works on as many  machines as possible, you need
to stick to C89/C99.

Besides, this shows that the compiler is  to C what the python interpreter is to
Python.
In the  same way  your python3 code  may not work  if you  pass it to  a python2
interpreter, your C99 code may not work if you compile it with an old compiler.

---

The line:

    #include <stdio.h>

is necessary to include information about C's standard I/O library.

`<stdio.h>` is a **header**.
A header contains information about some part of the standard library.

---

A  **library function**  belongs to  a library  of functions  supplied with  the
compiler.

---

**Compound statements** are statements inside curly braces.
They're common in `if` statements and loops.

---

To run the code contained in a C source code file, 3 steps are necessary:

Preprocessing.
The program is given to a **preprocessor**, which obeys commands that begin with
`#` (known as **directives**).
A preprocessor  is a bit like  an editor; it can  add things to the  program and
make modifications.

Compiling.
The  modified program  now  goes to  a **compiler**,  which  translates it  into
machine instructions (**object code**).

Linking.
Finally, a **linker**  combines the object code with any  additional code needed
to yield a complete executable program.
This additional code includes library functions (like `printf`) that are used in
the program.

---

How to compile `pun.c` into `pun`?

    $ gcc -o pun pun.c

---

Since statements can continue over several  lines, it's not always obvious where
they end.  This  is why C requires  that a statement end with  a semicolon, with
the exception  of the compound  statement.  Directives,  on the other  hand, are
normally one line long, and they don't end with a semicolon.

---

The type of a numeric variable  determines the largest and smallest numbers that
the variable  can store; it  also determines whether  or not digits  are allowed
after the decimal point.

What's the typical largest value that a variable of type int can store?

    2^31 - 1

MWE:

    # include <math.h>
    int main(void) {
        var = pow(2, 31) - 1
        ???
    }

##
# Programs and answers

<http://knking.com/books/c2/programs/index.html>
<http://knking.com/books/c2/answers/index.html>
<https://github.com/williamgherman/c-solutions>

# TODO

<http://viewsourcecode.org/snaptoken/kilo/>

Welcome!
This is an instruction booklet that shows you how to build a text editor in C.

The text editor is antirez’s kilo, with some changes.
It’s  about 1000  lines of  C in  a  single file  with no  dependencies, and  it
implements all  the basic features  you expect in a  minimal editor, as  well as
syntax highlighting and a search feature.

This booklet walks you through building the editor in 184 steps.
Each step, you’ll add, change, or remove a few lines of code.
Most steps,  you’ll be  able to observe  the changes you  made by  compiling and
running the program immediately afterwards.

I explain each step along the way, sometimes in a lot of detail.
Feel free to skim or  skip the prose, as the main point of  this is that you are
going to build a text editor from scratch!
Anything you learn along the way is bonus, and there’s plenty to learn just from
typing in the changes to the code and observing the results.

See the appendices  for more information on the tutorial  itself (including what
to do if you get stuck, and where to get help).

If you’re ready to begin, then go to chapter 1!

