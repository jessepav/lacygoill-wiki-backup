# What are the three steps which must be done before a source code file can be run?

   1. preprocessing
   2. compiling
   3. linking

##
# Compiling
## When do I need to make my code conform to the `c89` standard instead of the `c99` one?

Whenever there's no compiler which is c99-compliant, on the machine where you'll
compile.  It's particularly relevant on  old hardware, embedded systems, and IoT
(Internet of  Things), where  the only  compiler available  might be  old and/or
closed source.

This shows that the compiler is to C what the python interpreter is to Python.
In the  same way your python3  code might not work  if you pass it  to a python2
interpreter,  your C99  code  might not  work  if  you compile  it  with an  old
compiler.

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
# Syntax
## Why does C require that a statement end with a semicolon?

Since statements can continue over several  lines, it's not always obvious where
they end.

### When does C make an exception to this rule?

For compound statements, and directives.

##
## Which influence does the type of a numeric variable have?

It determines the largest and smallest numbers that the variable can store.
It also determines whether or not digits are allowed after the decimal point.

## What's the typical largest value that a variable of type `int` can store?

    2^31 − 1

MRE:
```c
    #include <stdio.h>
    #include <math.h>

    int main(void) {
        int var = pow(2, 31);
        printf("%d\n", var);
    }
```
    c.c: In function ‘main’:
    c.c:5:15: warning: overflow in conversion from ‘double’ to ‘int’ changes value
    ↪                  from ‘2.147483648e+9’ to ‘2147483647’ [-Woverflow]
    5 |     int var = pow(2, 31);
      |               ^~~
    2147483647

Rationale:

You can use 32 bits  to store an integer, and one of them  is used for the sign,
which gives you `2^31` numbers.
But `0` is one of those numbers, so you can go only up to `2^31 − 1`.

## Why is it better to use the type `int` rather than `float` when declaring a numeric variable?

For better performance and accuracy.

Arithmetic on `float` numbers might be slower than arithmetic on `int` numbers.

Also, the  value of  a `float` variable  is often just  an approximation  of the
number that was stored in it.
If you store `0.1` in a `float` variable, you might later find that the variable
has a value such as `0.09999999999999987`, because of rounding error.

##
## When must I write declarations before statements?

In (and only in) C89.

So, this will work in C99, *and* in C89:
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
But this will work only in C99 (not in C89):
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
---

This is true for in a function's body *and* in a block's body:
```c
    #include <stdio.h>

    int main(void) {
        if (1) {
            // declarations mixed with other statements: only works in C99
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
            // declarations before other statements: works in C99 *and* in C89
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

While this will work in C99, *and* in C89:
```c
    #include <stdio.h>

    int main(void) {
        printf("Hello world!");
        return 0;
    }
```
##
# Data Types
## When is the integer type not suitable for a numeric variable?  (2)

When you need a  variable that can store a number with  digits after the decimal
point, or a number that is exceedingly large or small.

##
## floats
### What are the 3 types of floats that C provides?

    ┌─────────────┬───────────────────────────────────┐
    │ float       │ Single-precision floating-point   │
    ├─────────────┼───────────────────────────────────┤
    │ double      │ Double-precision floating-point   │
    ├─────────────┼───────────────────────────────────┤
    │ long double │ Extended-precision floating-point │
    └─────────────┴───────────────────────────────────┘

Each of these corresponds to a different floating-point format.

#### When is each of these suitable?

`float` is  suitable when  the amount of  precision isn't  critical (calculating
temperatures to one decimal point, for example).

`double` provides greater precision – enough for most programs.

`long double` provides even more precision, but is rarely used.

#### How much precision do they provide?

This is not specified by the C standard.
That's  because  different  computers  might  store  floating-point  numbers  in
different ways.

Although, most modern computers follow the specifications in IEEE Standard 754.
The latter provides two primary formats for floating-point numbers:
single precision (32 bits) and double precision (64 bits).

A number is stored in a form of scientific notation, with three parts:

   - a sign
   - an exponent
   - a fraction (aka mantissa)

The number  of bits reserved  for the exponent  determines how large  (or small)
numbers  can  be, while  the  number  of bits  in  the  fraction determines  the
precision.
In single-precision  format, the  exponent is  8 bits  long, while  the fraction
occupies 23 bits.
As a  result, a  single-precision number  has a  maximum value  of approximately
`3.40 x 10^38`, with a precision of about 6 decimal digits.

####
### If a C compiler finds the floating constant `12.34`, how is it stored in memory?

Like a double-precision float.

#### How to force the compiler to use a different floating-point format?

For single precision, put the letter `F` or  `f` at the end of the constant; for
example, `12.34F`.

For extended-precision, put the letter `L` or `l` at the end (`12.34L`).

###
### This snippet doesn't give any error:
```c
    #include <stdio.h>

    int main(void) {
        float x = 12.34;
        printf("%f\n", x);
    }
```
    12.340000

#### But there is a type mismatch in the assignment.  Why no error?

Indeed, `x` is declared as a `float`, while it's assigned a double:

    float x = 12.34;
    ^---^     ^---^
    float  != double

But no  error is given  because a  `double` constant is  automatically converted
into a `float` when necessary (by discarding some bits).

---

Reciprocally, a `float` constant is automatically converted into a `double` when
necessary:
```c
    #include <stdio.h>

    int main(void) {
        double x = 12.34;
        printf("%f\n", x);
    }
```
    12.340000

#### And yet, omitting `f` after a `float` constant is bad.  Why?

It might cause an automatic coercion which is not wanted.

For example:
```c
    #include <assert.h>

    int main(void) {
        // OK: 12.34 is converted from double to float;
        // to match the float type in the declaration
        float x = 12.34;
        // not OK: f is converted from float to double;
        // to match the double type of 12.34
        assert(x == 12.34);
    }
```
    c.c:7: main: Assertion `x == 12.34' failed.

The  second coercion  is problematic,  because the  `float` constant  in `x`  is
simply padded  with 0's.   But this  padding doesn't match  the bits  which were
discarded  in the  previous coercion.   So, both  the assertion  and compilation
fail.

OTOH, everything works if you specify that the second `12.34` is a `float`:

    assert(x == 12.34f);
                     ^

Because it prevents the coercion of the value in `x` from `float` to `double`.
No padding of 0's is added, and both operands around `==` match.

##
# Library functions
## In `scanf()` and `printf()`, what does the "f" stand for?

**F**ormatted.

Indeed, both `scanf()` and `printf()` require  the use of a **format string** to
specify the appearance of the input or output data.

`scanf()` needs to know  what form the input data will  take, just as `printf()`
needs to know how to display output data.

##
# Resources
## Programs and answers

- <https://github.com/williamgherman/c-solutions>
- <http://knking.com/books/c2/programs/index.html>
- <http://knking.com/books/c2/answers/index.html>

##
# Todo
## Would this Vim syntax plugin give us better C syntax highlighting?

<https://github.com/justinmk/vim-syntax-extra>

## Build Your Own Text Editor

<http://viewsourcecode.org/snaptoken/kilo/>
