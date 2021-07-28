# a
## ANSI

American National Standards Institute

It's  a  private  non-profit  organization  that  oversees  the  development  of
voluntary consensus  standards for  products, services, processes,  systems, and
personnel in the United States.
The organization also coordinates U.S. standards with international standards so
that American products can be used worldwide.

These standards ensure that the  characteristics and performance of products are
consistent, that  people use the same  definitions and terms, and  that products
are tested the same way.

## ANSI C, ANSI/ISO C, ISO C

Can mean C89, C99, C11 or C17.

<https://en.wikipedia.org/wiki/ANSI_C>

##
# b
## block

A special case of a compound statement, which contains a mix of declarations and
regular statements.

Example:
```c
    if (i > j) {
        // swap values of i and j
        int temp = i ;
        i = j;
        j = temp;
    }
```
## bounds-checker

C doesn't require  that array subscripts be checked; a  bounds-checker adds this
capability.

##
# c
## C89

Version of the  C language described in the standard  ANSI X3.159-1989, in 1989,
and ISO/IEC 9899:1990, in 1990.

## C99

Version of the C language described in the standard ISO/IEC 9899:1999, in 1999.

- <https://en.wikipedia.org/wiki/C99>
- <https://gcc.gnu.org/c99status.html>

## C11

Version of the C language described in the standard ISO/IEC 9899:2011, in 2011.

- <https://en.wikipedia.org/wiki/C11_%28C_standard_revision%29>
- <https://gcc.gnu.org/wiki/C11Status>

## C17

Version of the C language described in the standard ISO/IEC 9899:2018, in 2018.

<https://en.wikipedia.org/wiki/C18_(C_standard_revision)>

The  wikipedia page  uses the  term `C18`,  but on  the web,  and on  the latest
manpage for GCC, `C17` is used more often.

## GNU C

Version of the C language used by GCC by default.

GNU C provides several language features not found in ISO standard C.

##
## compound statement

A group of statements inside curly braces.
They're common in `if` statements and loops.

##
## constant

A value  which is assigned  to a  variable which will  keep it during  the whole
execution of the program:

    height = 8;
             ^

### What's a magic number?

A value whose meaning is hard to understand from the context.

### How is a constant useful compared to a magic number?

It makes the code more readable:

                        magic number
                        v
    if (password_size > 7)
        ...

                            constant
                            v
    int MAX_PASSWORD_SIZE = 7;
    if (password_size > MAX_PASSWORD_SIZE)
        ...

It also helps if the value is used  in several locations, and you want to change
it in the  future.  Without a constant,  you would have to find  and replace all
occurrences of the value, and avoid:

   - forgetting one of the occurrences
   - replacing an occurrence which was used for a different purpose

<https://stackoverflow.com/questions/47882/what-is-a-magic-number-and-why-is-it-bad#comment3030262_47902>

##
# d
## directive

Statement beginning with `#`, which will be obeyed by the preprocessor.

##
# f
## float

A datatype whose name comes from "floating-point"; the latter is a technique for
storing numbers  in which the  binary point (decimal  point for a  computer) can
"float"; that is, it can be placed anywhere relative to the significant digits.
This position is given by the exponent component.

<https://en.wikipedia.org/wiki/Floating-point_arithmetic>

---

A  float value  is  stored in  2  parts:  the fraction  (aka  mantissa) and  the
exponent.  For example, 12.0 might be stored as:

           exponent
           v
    1.5 x 2³
    ^^^
    fraction

##
# h
## header

It contains information about some part of the standard library.

##
# i
## ISO

International Organization for Standardization

It's an international standard-setting  organization composed of representatives
from various national standards organizations.

It promotes worldwide proprietary, industrial and commercial standards.

## identifier

Name chosen for a variable, function, macro or another similar entity.

An identifier may contain letters, digits, and underscores.
But it cannot start with a digit.

An identifier must not match a keyword.

Since C is case-sensitive, the case of the chosen name matters.
For example, each of these names identify a different variable:

    job
    JOB
    jOb
    ...

---

Here are some examples of **legal** identifiers:

    times10
    get_next_char
    _done

Here are some examples of **illegal** identifiers:

    get-next-char
       ^    ^
       not a letter, nor a digit, nor an underscore

    10times
    ^
    a digit is allowed, but not at the start

---

In case you wonder whether it was a good or bad choice for C to be case
sensitive, read this: <https://softwareengineering.stackexchange.com/a/10010>

## initializer

First value assigned to a declared variable.

    int height = 8;
                 ^
                 initializer of the variable `height`

##
# k
## K&R C

Original version  of C  standardized by  the book  “The C  Programming Language”
written by Brian Kernighan and Dennis Ritchie.

## keyword

A token which has a special meaning in  the C language (and thus, cannot be used
as an identifier).  C only recognizes 32 keywords:

    auto
    break
    case
    char
    const
    continue
    default
    do
    double
    else
    enum
    extern
    float
    for
    goto
    if
    int
    long
    register
    return
    short
    signed
    sizeof
    static
    struct
    switch
    typedef
    union
    unsigned
    void
    volatile
    while

---

The C99 standard adds 5 new keywords to this list:

    inline
    restrict
    _Bool
    _Complex
    _Imaginary

##
# l
## leak-finder

A leak-finder helps locate memory leaks.

## linker

The linker combines the  object code with any additional code  needed to yield a
complete executable program.
This additional code includes library functions (like `printf`) that are used in
the program.

## literal

Synonym of constant.

##
# m
## macro

A fragment of code  which has been given a name with a `#define` directive.
Whenever the name is used, the preprocessor replaces it with its contents.

There  are two  kinds of  macros.  They  differ mostly  in what  they look  like
when  they  are used.   Object-like  macros  resemble  data objects  when  used,
function-like macros resemble function calls.

Source: <https://gcc.gnu.org/onlinedocs/cpp/Macros.html>

---

Warning: Try to use macros sparingly.
They  are hard  to  debug,  can have  unexpected  side-effects,  and don't  have
namespaces.

Source: <https://stackoverflow.com/a/14041847>

## memory leak

Blocks of memory that are dynamically allocated but never deallocated.

##
# o
## object code

Machine instructions obtained after the compiler has translated your source code file.

##
# p
## preprocessor

The preprocessor obeys the directives found in a source code file.
It's  a bit  like an  editor; it  can add  things to  the source  code and  make
modifications.

##
# t
## token

A group of characters that can't be split up without changing their meaning.

Tokens can be:

   - identifiers
   - keywords
   - operators
   - punctuation marks (like commas and semicolons)
   - string literals

As an example, this statement:

    printf("Height: %d\n", height);

can be split into these 7 tokens:

   1. `printf`
   2. `(`
   3. `"Height: %d\n"`
   4. `,`
   5. `height`
   6. `)`
   7. `;`

`1.` and `5.` are identifiers.
`2.`, `4.`, `6.` and `7.` are punctuation marks.
`3.` is a string literal.

##
# u
## uninitialized

This is said of a variable which has been declared, but not assigned any value.  yet.

