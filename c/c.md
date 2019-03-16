# ?

The term floating point refers to the fact that a number's binary point (decimal
point for a computer)  can “float”; that is, it can  be placed anywhere relative
to the significant digits of the number.
This position is indicated as the exponent component.

<https://en.wikipedia.org/wiki/Floating-point_arithmetic>

---

The integer types aren't suitable for all applications.
Sometimes we'll  need variables  that can  store numbers  with digits  after the
decimal point, or numbers that are exceedingly large or small.
Numbers like  these are stored in  floating-point format.
C provides three floating types, corresponding to different floating-point formats:

    ┌─────────────┬───────────────────────────────────┐
    │ float       │ Single-precision floating-point   │
    ├─────────────┼───────────────────────────────────┤
    │ double      │ Double-precision floating-point   │
    ├─────────────┼───────────────────────────────────┤
    │ long double │ Extended-precision floating-point │
    └─────────────┴───────────────────────────────────┘

`float` is  suitable when  the amount of  precision isn't  critical (calculating
temperatures to one decimal point, for example).
`double` provides greater precision – enough for most programs.
`long double` provides even more precision, but is rarely used.

The C standard doesn't state how much precision the `float`, `double`, and `long double`
types provide,  since different  computers may  store floating-point  numbers in
different ways.

Most modern computers follow the specifications in IEEE Standard 754.
It provides two primary formats  for floating-point numbers:
single precision (32 bits) and double precision (64 bits).
Numbers are  stored in a  form of scientific  notation, with each  number having
three parts: a **sign**, an **exponent**, and a **fraction**.
The number  of bits reserved  for the exponent  determines how large  (or small)
numbers  can  be, while  the  number  of bits  in  the  fraction determines  the
precision.
In single-precision  format, the  exponent is  8 bits  long, while  the fraction
occupies 23 bits.
As a  result, a  single-precision number  has a  maximum value  of approximately
`3.40 x 10^38`, with a precision of about 6 decimal digits.

The standard doesn't specify the number of bits in these formats, although it requires
that the single extended type occupy at least 43 bits

---

By default, floating constants are stored as double-precision numbers.
IOW, when a C  compiler finds the constant `57.0` in a  program, it arranges for
the number to be stored in memory in the same format as a `double` variable.
This  rule generally  causes no  problems, since  `double` values  are converted
automatically to `float` when necessary.

On occasion,  it may  be necessary  to force  the compiler  to store  a floating
constant in `float` or `long double` format.
To indicate that only single precision is  desired, put the letter `F` or `f` at
the end of the constant; for example, `57.0F`.
To indicate that  a constant should be  stored in `long double`  format, put the
letter `L` or `l` at the end (`57.0L`).

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

Combine their declarations on a single line, and separate their names with commas:

    int height, length, width, volume;
    float profit, loss;

##
## Which influence does the type of a numeric variable have?

It determines the largest and smallest numbers that the variable can store.
It also determines whether or not digits are allowed after the decimal point.

## What's the typical largest value that a variable of type `int` can store?

    2^31 − 1

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
But `0` is one of those numbers, so you can go only up to `2^31 − 1`.

## Why is it better to use the type `int` rather than `float` when declaring a numeric variable?

For better performance and accuracy.

Arithmetic on `float` numbers may be slower than arithmetic on `int` numbers.

Also, the  value of  a `float` variable  is often just  an approximation  of the
number that was stored in it.
If you store `0.1`  in a `float` variable, you may later  find that the variable
has a value such as `0.09999999999999987`, because of rounding error.

##
## When must I separate statements from declarations?

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

