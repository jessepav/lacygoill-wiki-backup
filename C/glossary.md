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

Synonym for compound statement.

## bounds-checker

C doesn't  require array subscripts  to be  checked; a bounds-checker  adds this
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

The Wikipedia page  uses the term `C18`, but  on the web, and on  the latest man
page for GCC, `C17` is used more often.

## GNU C

Version of the C language used by GCC by default.

GNU C provides several language features not found in ISO standard C.

##
## compound assignment operator

Assignment operator  of the  form `X=`,  where `X` is  a binary  operator, which
first  performs the  operation of  `X` on  both operands,  before assigning  the
result to the left operand.

For example:

    i += 3
      ^^

Here, before assigning  anything to `i`, the code performs  the `+` operation on
both operands:

    the operands around +=
    v   v
    i + 3
      ^
      the operator at the start of +=

Then, the result is assigned to `i`.

---

Other examples of compound assignment operators include:

    -=
    *=
    /=
    %=

---

Compound and simple assignment operators are similar.
They are both right-associative.
They both yield the lvalue as it is after the assignment.

## compound statement

Groups  several statements  into a  single statement  (by surrounding  them with
curly  braces).   The compound  statement  is  commonly  used in  selection  and
iteration statements, where the syntax only allows for 1 statement, but where we
might need more.

Example:
```c
    if (i > j)
    {
        // swap values of i and j
        int temp = i ;
        i = j;
        j = temp;
    }
```
##
## constant

Number that appear in the text of a program; not read, written, or computed.

    height = 8;
             ^

## controlling expression

Expression evaluated by a control flow statement.

For example, it  can be an expression  tested by a `switch`  statement to decide
where control  should jump.  Or an  expression evaluated by a  `for`, `while` or
`do` loop, to decide whether it should run its next iteration.

## conversion specification

`%x` token which can be included inside a format string passed to
`printf()`/`scanf()`, and is meant to be replaced with some value.

Once replaced, the result is written:

   - on the program stdout in the case of `printf()`
   - in a variable in the case of `scanf()`

---

The information that follows `%` *specifies* how the value is *converted*:

   - from its internal form (binary) to printed from (characters) in the case of `printf()`
   - from its inputted form (characters) to internal form (binary) in the case of `scanf()`

That's where the term "conversion specification" comes from.

For example, the  conversion specification `%d` specifies that  `printf()` is to
convert an `int` value to a string of decimal digits.

---

In `%x`,  `x` is  called conversion  specifier.  It determines  the type  of the
value which is meant to replace `%x`.

---

In the case of `printf()`, the expression can be formatted according to optional
information located between `%` and `x`:

    printf("%10.3f", x);
             ^--^
             controls how to print the float

##
# d
## dangling else

A nested `else` preceded by a simple (!= compound) statement.

It's ambiguous because you might think that  such an `else` belongs to the outer
`if`,  while  in  reality it  belongs  to  the  nested  one (especially  if  its
indentation is wrong).

The compiler can warn you against this pitfall:
```c
    #include <stdio.h>

        int
    main(void)
    {
        int i = 1, j = 2;
        if (j != 0)
            if (i != 0)
                j = i / j;
        else
            printf("Error: j is equal to 0\n");
    }
```
    error: suggest explicit braces to avoid ambiguous ‘else’ [-Werror=dangling-else]
                                                                      ^-----------^

Putting braces around the nested `if` might be necessary:
```c
    #include <stdio.h>

        int
    main(void)
    {
        int i = 1, j = 2;
        if (j != 0)
        {
            if (i != 0)
                j = i / j;
        }
     // ^
     // terminate the nested `if` early so that the subsequent `else` belongs to the
     // outer `if`
        else
            printf("Error: j is equal to 0\n");
    }
```

## directive

Statement beginning with `#`, which will be obeyed by the preprocessor.

##
# e
## expression statement

Any expression turned into a statement with an appended semicolon.

The value of such an expression is discarded.
Thus, it's only useful if it has a side effect.

Examples:

    i++;
       ^

    i = 1;
         ^

Here, `i++` and `i = 1` are both expressions, which evaluate to the new value of `i`.
They remain useful even when turned  into statements, because they have the side
effect of changing the value of `i`.

OTOH, this expression statement is useless:

    i * j - 1;
             ^

Because it has no side effect.

##
# f
## fetch

Retrieving the value of a variable from memory to perform some computation which
refers to it.

A variable typically  lives in RAM, while  a fetched value is copied  into a CPU
register.  The two values are independent.  In particular, changing the value of
a variable has no effect on a prior copy living in a CPU register.

## float

A datatype whose name comes from "floating-point"; the latter is a technique for
storing numbers  in which the  binary point (decimal  point for a  computer) can
"float"; that is, it can be placed anywhere relative to the significant digits.
This position is given by the exponent component.

For more info: <https://en.wikipedia.org/wiki/Floating-point_arithmetic>

---

A  float value  is  stored in  2  parts:  the fraction  (aka  mantissa) and  the
exponent.  For example, 12.0 might be stored as:

           exponent
           v
    1.5 x 2³
    ^^^
    fraction

## format string

First string argument passed to `printf()` or `scanf()`.

It controls how  `printf()` formats printed text, and how  `scanf()` reads input
text.

## function prototype

Declaration of a function that declares the types of its parameters.

##
# g
## GPR

General Purpose Register

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

##
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

## implementation

The  software needed  to compile,  link, and  execute programs  on a  particular
platform.

## implementation-defined behavior

The C standard  deliberately leaves parts of the language  unspecified, with the
understanding that an implementation will fill in the details.

For example, the behavior of the `/`  and `%` operators for negative operands in
C89 is implementation-defined.

---

The C standard requires any implementation-defined behavior to be documented.

---

To  make  your code  portable  across  platforms,  you  should avoid  making  it
dependent on an  implementation-defined behavior.  If you can't,  then read your
implementation's manual to be sure to understand how your code will work.

## initializer

First value assigned to a declared variable.

    int height = 8;
                 ^
                 initializer of the variable `height`

##
## integer
### signed

Integer whose  leftmost bit encodes  a sign: 0 if the  number is positive,  1 if
it's strictly negative.

### unsigned

Integer with no sign  bit (its leftmost bit is considered  part of the integer's
magnitude).

##
# k
## K&R C

Original version  of C  standardized by  the book  “The C  Programming Language”
written by Brian Kernighan and Dennis Ritchie.

##
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
## label

Identifier placed at the beginning of a statement:

    identifier: statement;
    ^--------^

A statement might have more than 1 label:

    foo: bar: statement;
    ^^^^ ^^^^

You can use a label name in a  `goto` statement to jump right below the location
of that label:

    goto foo;
         ^^^

## leak-finder

A leak-finder helps locate memory leaks.

## linker

The linker combines the  object code with any additional code  needed to yield a
complete executable program.
This additional code includes library  functions (like `printf()`) that are used
in the program.

## (string) literal

Sequence of zero  or more multibyte characters enclosed in  double-quotes, as in
"xyz".

Also known as "character string literal".

## logical expression

Expression which can be tested by an `if` statement or a conditional operator.

It's built from relational, equality, and logical operators.

## lvalue

Object stored in memory.

A variable name and an array subscript are lvalues.
Constants such as `123`, and expressions such as `i * 2` are not.

BTW, it's pronounced "L-value".

##
# m
## macro

A fragment of code  which has been given a name with a `#define` directive.
Whenever the name is used, the preprocessor replaces it with its contents.

There  are two  kinds of  macros.  They  differ mostly  in what  they look  like
when  they  are used.   Object-like  macros  resemble  data objects  when  used;
function-like macros resemble function calls.

Source: <https://gcc.gnu.org/onlinedocs/cpp/Macros.html>

---

Warning: Try to use macros sparingly.
They  are hard  to  debug,  can have  unexpected  side-effects,  and don't  have
namespaces.

Source: <https://stackoverflow.com/a/14041847>

## magic number

Number whose meaning is hard to understand from the context.

## memory leak

Blocks of memory that are dynamically allocated but never deallocated.

##
# n
## null statement

Special case of an expression statement, where there is no expression.

Example:

    2 assignments
    v----v   v----v
    i = 0; ; j = 1;
           ^
           1 null statement

Another (less contrived) example:

    // look for the smallest divisor d of n
    for (d = 2; d < n && n % d != 0; d++)
      ;
      ^

##
# o
## object code

Machine instructions obtained after the compiler has translated your source code file.

##
## operator associativity

Property  of an  operator  which determines  how operations  are  grouped in  an
expression containing  several operators  of equal  precedence, adjacent  to the
same operand, and without parentheses.

An operator can be:

   - associative: the operations can be grouped arbitrarily

   - left-associative: the operations must be grouped from left to right
   - right-associative: the operations must be grouped from right to left

   - non-associative: the operations cannot be chained;
     often because the output type is incompatible with the output types

Grouping from left  to right means that  we first group the  operands around the
leftmost  operator.  Here  is an  abstract example  where `Op`  stands for  some
operator, and `a`, `b`, `c` are operands:

    a Op b Op c

If `Op` is left-associative, the operations are grouped like this:

    (a Op b) Op c

Because the leftmost operation is the first one.

If `Op` is right-associative, the operations are grouped like this:

    a Op (b Op c)

Because the rightmost operation is the last one.

---

Real  examples of  left-associative operators  are: `*`,  `/`, `%`,  `+` (binary
version), `-` (binary version).  Consequently:

      i - j - k
    ⇔
      (i - j) - k

      i * j / k
    ⇔
      (i * j) / k

Examples of  right-associative operators  are: `+`  (unary version),  `-` (unary
version).  Consequently:

      - + i
    ⇔
      -(+i)

## operator precedence

Property  of an  operator  which determines  how operations  are  grouped in  an
expression containing several operators, and without parentheses.

For example, in this expression:

    i + j * k

The operations are grouped like this:

    i + (j * k)
        ^     ^

Not like this:

    (i + j) * k
    ^     ^

Because the `*` operator has a higher precedence than `+`.

## operators families
### conditional

`?:`

### equality

`==` and `!=`

### logical

`!`, `&&`, and `||`

### relational

`<`, `<=`, `>`, and `>=`

##
# p
## preprocessor

The preprocessor obeys the directives found in a source code file.
It's  a bit  like an  editor; it  can add  things to  the source  code and  make
modifications.

##
# r
## remainder

Result of a `%` operation.

For example, `3` is the remainder of `7 % 4`.

## round toward 0

For an inexact division whose result is positive: round down (`floor()`).
For an inexact division whose result is negative: round up (`ceil()`).

## round toward -∞

Round down.

##
## rvalue

An  expression which  can appear  on the  RHS  of an  assignment.  It  can be  a
variable, a constant, or a more complex expression.

##
# s
## scope

Region of program text within which an identifier is visible (i.e. can be used).

There are four kinds of scopes:

   - block
   - function
   - function prototype
   - file

For  the same  identifier to  designate different  entities, it  must either  be
written  in different  scopes (e.g.  block vs  function), or  in different  name
spaces (e.g. 2 different files).

The scope of an identifier is determined by the placement of its declaration.
Except  a label  name, which  always has  function scope,  no matter  where it's
declared.

## selection statement

A statement which selects a code path out of several possibilities, like `if` or
`switch`.

## sequence point

Some location in the code where it is guaranteed that at runtime:

   - all side effects of some previous evaluations will have been performed
   - no side effects from some subsequent evaluations will have yet been performed

---

Adding more sequence  points is sometimes necessary to make  an expression valid
and  predictable  (by enforcing  a  single  valid  order  of evaluation  of  its
subexpressions).

The absence  of any  sequence point  between 2  subexpressions which  share some
state (i.e. whose values both depend on the same object), and whose execution of
evaluations can overlap, might cause a UB.

For example:

    (a = 123) + (b = a)

Here, there is no sequence point  between `(a = 123)` and `(b = a)`, which means
it's possible for `(b = a)`  to be evaluated in the middle  of the evaluation of
`(a = 123)`.  That is, in the middle of the process writing the bits of `123` in `a`:

    123 in binary
    v-----v
    1111011
       ^--^

Only the last  4 bits `1011` might  have been assigned to `a`  when `(b = a)` is
evaluated.   If that  happens, `b`  will be  assigned `00001011`  (decimal `11`)
instead  of `11111011`  (decimal `123`).   In effect,  `b` might  be assigned  a
meaningless value.

---

There are various kinds of sequence points.

The `;` terminating an expression statement  is one of them.  Before a statement
can be executed, the previous one must have been fully executed.  In particular,
all its increments and decrements must have been performed.

The logical `&&`/`||`, the ternary conditional `?:`, and the comma operator also
impose a sequence point.

So do function calls:  a function's body is not entered  until all the arguments
in the call have been fully evaluated.
Although,  there is  no requirement  on  the order  in which  the arguments  are
evaluated.  For example, in `f(a, b)`, `b`  might be evaluated before, after, or
at the same time as `a`.
Similarly, there is no requirement between several function calls.
For example:

    f(i++) + g(j++)

We have the guarantee that:

   - `i` is incremented before `f()`'s body is entered
   - `j` is incremented before `g()`'s body is entered

But there is *no* guarantee that:

   - `i` is incremented before `j`
   - `i` is incremented before `g()`'s body is entered
   - `f()` returns before `g()`'s body is entered

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
## undefined behavior (aka UB)

According to the C standard, some statements such as:

    a = b / 0;
    c = (b = a + 2) - (a = 1);
    j = i * i++

cause  **undefined  behavior**.  If  the  code  of  a  program contains  such  a
statement, all bets are off; the program might:

   - not compile at all
   - compile, but not run
   - compile, run, but crash or behave unexpectedly

And for a particular  UB, there is not even any  guarantee of consistency across
compilers.  For example, a statement causing UB might:

   - not compile with a compiler A
   - compile, but not run with a compiler B
   - compile, run, but crash or behave unexpectedly with a compiler C

That's why you should avoid writing a statement causing UB.

---

UB is not the same thing as implementation-defined behavior.

With UB, anything can happen.
With an implementation-defined behavior, the implementation has to document what
should happen.  Obviously it should also  respect its own documentation; i.e. if
it  *says* "A"  should  happen,  then, *in  practice*,  "A"  should happen;  not
something else.

## uninitialized

This is said of a variable which has been declared, but not yet assigned any value.

