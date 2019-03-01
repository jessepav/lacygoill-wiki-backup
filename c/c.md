# What are the three steps which must be done before a source code file can be run?

   1. preprocessing
   2. compiling
   3. linking

##
# Compiling
## When do I need to make my code conform to the `c89` standard instead of the `c99` one?

Whenever there's  no compiler,  on the  machine where  you'll compile,  which is
c99-compliant.
It's particularly relevant on old  hardware, embedded systems, and IoT (Internet
of Things), where the only compiler available may be old and/or closed source.

This shows that the compiler is to C what the python interpreter is to Python.
In the  same way  your python3 code  may not work  if you  pass it to  a python2
interpreter, your C99 code may not work if you compile it with an old compiler.

##
## What are C extensions?

Language features and library functions provided by a compiler, and not found in
ISO standard C.

### Where can I find information about the C extensions provided by GCC?

<https://gcc.gnu.org/onlinedocs/gcc/C-Extensions.html#C-Extensions>

### When and why should I avoid them?

Those extensions are specific to a compiler.
If you're concerned by the portability of your program, you need to stick to C89
(or maybe C99).

From “C Programming A Modern Approach”, page 7:

> Most C  compilers provide  language features and  library functions  that aren't
> part of the C89 or C99 standards.
> For portability,  it's best  to avoid using  nonstandard features  and libraries
> unless they're absolutely necessary.

##
## How to compile `pun.c` into `pun`?

    $ gcc -o pun pun.c

### How to specify `c89` as the standard to which the code should conform?

Use the `-std=c89` option:

    $ gcc -std=c89 -o pun pun.c
          ^^^^^^^^

### How to issue all the mandatory diagnostics listed in the C standard?

Use the `-pedantic` option:

    $ gcc -std=c89 -pedantic -o pun pun.c
                   ^^^^^^^^^

Or the `-pedantic-errors` option, if you  want to turn the mandatory diagnostics
into errors:

    $ gcc -std=c89 -pedantic-errors -o pun pun.c
                   ^^^^^^^^^^^^^^^^

##
# Syntax
## Why does C require that a statement end with a semicolon?

Since statements can continue over several  lines, it's not always obvious where
they end.

### When does C make an exception to this rule?

For compound statements, and directives.

##
## What does `#include <stdio.h>` do?

It tells the preprocessor to include information about C's standard I/O library.

### What's the name of `<stdio.h>`?

A header.

##
## How to declare a variable?

Specify its type then its name:

    int height;
    float profit;

## How to declare several variables of the same type?

Combine their declarations on a single line:

    int height, length, width, volume;
    float profit, loss;

##
## Which influence does the type of a numeric variable have?

It determines the largest and smallest numbers that the variable can store.
It also determines whether or not digits are allowed after the decimal point.

## What's the typical largest value that a variable of type `int` can store?

    2^31 - 1

MWE:

    #include <stdio.h>
    #include <math.h>

    int main(void) {
        int var = pow(2, 31);
        printf("%d\n", var);
    }

    c.c: In function ‘main’:~
    c.c:9:11: warning: overflow in implicit constant conversion [-Woverflow]~
         var = pow(2, 31);~
               ^~
    2147483647~

Rationale:

You can use 32 bits  to store an integer, and one of them  is used for the sign,
which gives you `2^31` numbers.
But `0` is one of those numbers, so you can go only up to `2^31 - 1`.

## Why is it better to use the type `int` rather than `float` when declaring a numeric variable?

For better performance and accuracy.

Arithmetic on `float` numbers may be slower than arithmetic on `int` numbers.

Also, the  value of  a `float` variable  is often just  an approximation  of the
number that was stored in it.
If you store `0.1`  in a `float` variable, you may later  find that the variable
has a value such as `0.09999999999999987`, because of rounding error.

##
## When must I separate statements and declarations?

In (and only in) C89.

So this will work in C99, but not in C89:
```c
    #include <stdio.h>

    int main(void) {
        int var1 = 123;
        printf("%d\n", var1);

        int var2 = 456;
        printf("%d\n", var2);

        return 0;
    }
```

While this will work in C89, *and* in C99:
```c
    #include <stdio.h>

    int main(void) {
        int var1 = 123;
        int var2 = 456;

        printf("%d\n", var1);
        printf("%d\n", var2);

        return 0;
    }
```

---

This is true for functions *and* for blocks:
```c
    #include <stdio.h>

    int main(void) {
        if (1) {
            int var1 = 123;
            printf("%d\n", var1);

            int var2 = 456;
            printf("%d\n", var2);
        }
        return 0;
    }
```
```c
    #include <stdio.h>

    int main(void) {
        if (1) {
            int var1 = 123;
            int var2 = 456;

            printf("%d\n", var1);
            printf("%d\n", var2);
        }
        return 0;
    }
```
## When must my function end with a `return` statement?

In (and only in) C89.

So this will work in C99, but not in C89:
```c
    #include <stdio.h>

    int main(void) {
        printf("Hello world!");
    }
```

While this will work in C89, *and* in C99:
```c
    #include <stdio.h>

    int main(void) {
        printf("Hello world!");
        return 0;
    }
```
##
# Resources
## Programs and answers

<http://knking.com/books/c2/programs/index.html>
<http://knking.com/books/c2/answers/index.html>
<https://github.com/williamgherman/c-solutions>

##
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

