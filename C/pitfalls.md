# Behavior
## Implementation-Defined Behavior
### `%` operator
#### How does it work?

`a % b` satisfies this equality:

    a % b = a - I(a/b) * b

The issue is that C89 and C99 don't define `I(a/b)` in the same way.
For C99,  it's simple: `I(a/b)`  is the algebraic  quotient with  any fractional
part discarded.

   > When integers  are divided, the result  of the / operator  is the algebraic
   > quotient with any fractional part discarded.

For example, the algebraic quotient of `9 / 4` is `2.25`.
In `2.25`, the fractional part is `.25`; if we remove it, we get `2`.
So, in C99, `I(9/4)` is `2`.

For C89, it's more complex, because it distinguishes 2 cases:
`a` and `b` can be both positive, or one of them can be negative.

If `a` and  `b` are positive, then  C89 defines `I(a/b)` as  the largest integer
less than the algebraic quotient:

   > When integers are divided and the division is inexact, if both operands are
   > positive the result of the / operator  is the largest integer less than the
   > algebraic quotient

The  wording  is  different,  but  the result  is  the  same: C89  discards  the
fractional part.

OTOH, if at least one of `a` or `b` is negative, then C89 defines `I(a/b)` like so:

   > If either operand is negative, whether the  result of the / operator is the
   > largest integer  less than the  algebraic quotient or the  smallest integer
   > greater than the algebraic quotient is implementation-defined

This means  that the implementation can  decide whether it rounds  the algebraic
quotient up or down.

#### What's the name of this `%` operator
##### in C?

It's not named explicitly in the standard.

Although, the result of `a % b` has a name: the remainder.

   > the result of the % operator is the remainder

##### in Python?

It's the modulo operator.

##### in other programming languages?

It depends on the language:
<https://en.wikipedia.org/wiki/Modulo_operation#In_programming_languages>

It seems the 2 most popular algorithms are:

   - truncation (aka rounding toward 0)
   - rounding down

####
#### I'm working on a different language than C.  How does `%` work over there?

`a % b` probably satisfies the same equality as in C.  The issue is to determine
how `a / b` is handled.  Different languages might use different definitions:
<https://en.wikipedia.org/wiki/Modulo_operation#Variants_of_the_definition>

Make some test with  a negative operand.  If the result of  `a % b` has the same
sign as  `a`, the fractional part  of `a / b` was probably  discarded during the
computation; if it has the same sign as `b`, `a / b` was probably rounded down.

#### How should I test whether a number is odd?

Like this:

    if (num % 2 != 0)

But not like this:

    if (num % 2 == 1)

The second  form is  only reliable  if you  have the  guarantee that  `a / b` is
rounded down.  If  it's rounded toward 0, and `num`  is negative, then `num % 2`
is -1, not 1.  The first form should work no matter what.

###
### What is the result of
#### `-8 /  5`

`-8 / 5` could evaluate to either `-1` (rounding up) or `-2` (rounding down).

This is a direct consequence of how CPUs work: some of them yield `-1` when `-8`
is divided by `5`, while others  produce `-2`.  The C89 standard simply reflects
that.

---

OTOH, in C99, `-8 / 5` always evaluates to `-1` (fractional part discarded).

####  `8 / -5`

It also contains a negative operand; so the result is the same as `-8 / 5`.

#### `-8 / -5`

It contains 2 negative signs, which cancel out.
Thus, the result is positive.

But remember that the C89 standard says that if any operand is negative, it's up
to the implementation to decide how to  round the result, while C99 discards the
fractional part.

So, in C89, the result can be `1` or `2`, while in C99 it's always `1`.

####
#### `-8 %  5`

The C89 standard does not state what `a % b` is directly.
However, whatever standard you're using, it  always gives you the guarantee that
this equality is satisfied:

    (a / b) * b + (a % b) = a
     ^---^         ^---^

From this equality, we can derive `a % b`:

    a % b = a - (a / b) * b

If we plug `a = -8` and `b = 5` into this, we get:

    -8 % 5 = -8 - (-8 / 5) * 5

Now, either your program follows the C89 standard, or a standard above.

If it follows C89, then `-8 / 5` is `-1` or `-2`.
If it's `-1`:

    -8 % 5 = -8 - (-1) * 5
           = -8 + 5
           = -3
             ^^

If it's `-2`:

    -8 % 5 = -8 - (-2) * 5
           = -8 + 10
           = 2
             ^

So, `-8 % 5` is `-3` or `2`.

OTOH, if your program follows C99 or above, `-8 % 5` is always `-3`.
Remember C99 states that `a % b` always has the same sign as `a`.

#### ` 8 % -5`

If your program follows C89, then `-8 / 5` is `-1` or `-2`.
If it's `-1`:

    8 % -5 = 8 - (-1) * (-5)
           = 8 - 5
           = 3
             ^

If it's `-2`:

    8 % -5 = 8 - (-2) * (-5)
           = 8 - 10
           = -2
             ^^

So, `8 % -5` is `3` or `-2`.

OTOH, if your program follows C99 or above, `8 % -5` is always `3`.

#### `-8 % -5`

If your program follows C89, then `-8 / -5` is `1` or `2`.
If it's `1`:

    -8 % -5 = -8 - 1 * (-5)
            = -8 + 5
            = -3
              ^^

If it's `2`:

    -8 % -5 = 8 - 2 * (-5)
            = -8 + 10
            = 2
              ^

So, `-8 % -5` is `-3` or `2`.

OTOH, if your program follows C99 or above, `-8 % -5` is always `-3`.

###
## Undefined Behavior
### In `(a + b) * (c - d)`, which subexpression is evaluated first:  `(a + b)` or `(c - d)`?

There is no way to know in the general case, because C doesn't define the order.

The rules of  operator precedence and associativity only tell  us how operations
are **grouped** in a C expression; they don't tell us how they are **ordered**.

###
### Why should I avoid writing an embedded assignment expression inside a larger expression?

It might cause a UB.

Let's say the embedded assignment assigns a value into the variable `v`.
If another subexpression inside the larger expression tries to read the value of
`v`, you get a UB.  Example:
```c
    // GCC Options: -Wno-sequence-point
    #include <stdio.h>
        int
    main(void)
    {
        int a, b, c;
        a = 5;
        c = (b = a + 2) - (a = 1);
        printf("c = %d\n", c);
    }
```
    c = 6

On  our  machine,  `c`  is  assigned `6`.   This  means  that `(b = a + 2)`  is
evaluated before  `(a = 1)`.  But on  a different machine,  these subexpressions
might be  evaluated in the reverse  order; in which  case `c` would be  set with
`2`.

Instead, write the assignments separately, in their own dedicated statements:
```c
    #include <stdio.h>
        int
    main(void)
    {
        int a, b, c;
        a = 5;
        b = a + 2;
        a = 1;
        c = b - a;
        printf("c = %d\n", c);
    }
```
    c = 6

---

Same kind of issue  if you try to assign to the same  variable twice in the same
expression:
```c
    // GCC Options: -Wno-sequence-point
    #include <stdio.h>
        int
    main(void)
    {
        int a, b;
        b = (a = 2) - (a = 1);
        printf("b = %d\n", b);
    }
```
    b = 0

On our machine, `b` is assigned `0`, which is unexpected.  It should be `1` (`2 - 1`).
The issue comes from the `b` assignment which causes a similar UB.
It's possible that the execution of the two embedded assignments overlap at some
point in time, which would explain the meaningless `b`.

#### What should I make sure of before using `++`/`--` inside a larger expression?

The larger expression should not depend on a particular order of evaluation.  In
particular, if you increment/decrement a variable  `i`, don't refer to that same
variable anywhere else.

Here is an example of bad usage:
```c
    // GCC Options: -Wno-sequence-point
    #include <stdio.h>
        int
    main(void)
    {
        int i, j;
        i = 2;
        j = i * i++;
        printf("j = %d\n", j);
    }
```
    j = 6

We don't know whether `i++` is evaluated before or after the multiplication.
On our machine, it's evaluated after, which is why `j` is assigned `6`.
But on another machine, it might be evaluated before; in which case `j` would be
assigned `4`.

IOW, `j = i * i++` causes a UB.

Notice how this is yet another case of an expression which simultaneously writes
to and reads from the same variable.   The first `i` subexpression reads a value
from the  `i` variable, while the  second `i++` subexpression writes  a value to
that same `i` variable.

###
### When should I prefer a compound assignment operator over the simple `=`?

When evaluating your lvalue has a side effect.

With `v += e`, `v` is only evaluated once.
With `v = v + e`, `v` is evaluated twice.

Whether the side effect occurs once or twice might matter.
For example:

    a[i++] = a[i++] + 2;

The value of `i`  is changed as well as used elsewhere in  the statement, so the
effect of executing the statement is undefined.

To  avoid this,  you could  use `+=`  instead of  `=` so  that `a[i++]`  is only
evaluated once:

    a[i++] += 2;

##
# Data Types
## Why should I always append "f" to a constant with a decimal point if it's assigned to a `float` variable?

An omission might cause a problematic coercion.

                  not recommended, but OK
                  v
    float x = 12.34;
    assert(x == 12.34);
                    ^
                    ✘

In  the first  assignment, `12.34`  is converted  from an  implicit `double`  to
`float`, to  match the type specification  on the LHS.  Then,  in the assertion,
the  evaluation of  `x` is  converted  from `float`  to `double`  (to match  the
`double` on the RHS of `==`), by adding a padding of 0's.  This padding will not
match the  bits which  were discarded  in the previous  coercion.  So,  both the
assertion and compilation fail.

This would be better:

                   v
    float x = 12.34f;
    assert(x == 12.34f);
                     ^

---

GCC will complain if you compile with `-Wfloat-equal`:

    comparing floating point with == or != is unsafe [-Werror=float-equal]

But that's a different issue.
The point is: don't forget the `f` suffix to a `float` constant.

##
# Declarations
## Why should I always initialize a variable?

If  you  don't,   it  will  be  assigned  a  random   value,  making  your  code
unpredictable.

## Which names should I avoid?

Names which are reserved.

This includes  any name starting  with an underscore  and followed by  either an
uppercase letter, or another underscore.

   > -- All identifiers that begin with an underscore and either an uppercase letter or another
   >      underscore are always reserved for any use.

For example, C99 provides the `_Bool` type.  Don't use this name in your code.

#
# Expressions
## I want to test whether `j` is between `i` and `k`.  Why shouldn't I write `i < j < k`?

It does not yield 1 if `i < j` and `j < k`.

Since `<` is left associative, the subexpressions are grouped like this:

    ((i < j) < k)

`i < j` always evaluates to 0 or 1; afterward, the result (`r`) is compared to `k`:

    (r < k)
     ^
     // 0 if i < j
     // 1 if i > j

Because of that, if:

    i = 1
    j = 4
    k = 3

Then `i < j < k` evaluates to 1, even though  you might expect it evaluates to 0
because `j < k` is false here (`4 < 3` is false).
```c
    // GCC Options: -Wno-parentheses
    #include <stdio.h>
        int
    main(void)
    {
        int i, j, k;
        i = 1;
        j = 4;
        k = 3;
        printf("%d\n", i < j < k);
    }
```
    1

---

Instead, write this:

    i < j && j < k

##
# Functions
## `printf()`
### Which subtle difference exists between `printf("%05d", n)` and `printf("%.5d", n)`?

They don't print a negative integer in the same way:
```c
    #include <stdio.h>
        int
    main(void)
    {
        int n = -123;
        printf("%%05d:  %05d\n", n);
        printf("%%.5d: %.5d\n", n);
    }
```
    %05d:  -0123
    %.5d: -00123

That's because, `%05d` says:

   > I want 5 **characters**; if you don't have enough, pad the number with 0s

While, `%.5d` says:

   > I want 5 **digits**; if you don't have enough, pad the number with 0s

And the negative sign *is* a character, but not a digit.

###
## `scanf()`
### I'm calling `scanf()`.  It doesn't return after I press Enter!

Make sure you didn't write a trailing whitespace at the end of the format:

    scanf("%d\n", &i);
             ^^
             ✘

    scanf("%d\t", &i);
             ^^
             ✘

    scanf("%d ", &i);
             ^
             ✘

Such a trailing whitespace causes `scanf()` to look for a non-whitespace.
When you press Enter, you produce a newline which is a whitespace; but `scanf()`
wants  a *non*-whitespace.   To terminate  the call,  input some  non-whitespace
(e.g. `x`).  Then, fix your format.

### Why `%i` should be avoided to read an integer in a `scanf()` format?

    scanf("%i", &i);
           ^^

It  can give  unexpected results,  because it  can match  an integer  written in
decimal, hexadecimal, or octal, depending on how the input number starts.

For example, the input `0123` reads the decimal number `83`.
And the input `0x123` reads the decimal number `291`.

Prefer `%d`.

##
# Macros
## If an expression used to define a macro contains an operator, why should I wrap it inside parentheses?

Otherwise, you have no guarantee that the compiler will treat it as a whole.
That's  because, after  the replacement,  the rules  of operator  precedence and
associativity might be applied in ways you didn't expect.

Consider this code:

                   no parens around the expression
                   v         v
    #define TWO_PI 2 * 3.14159
    ...
    conversion_factor = 360 / TWO_PI;

During preprocessing, the last statement is replaced with:

    conversion_factor = 360 / 2 * 3.14159

Which is equivalent to:

    conversion_factor = (360 / 2) * 3.14159

That's not what you wanted.  You wanted this:

    conversion_factor = 360 / (2 * 3.14159)

##
# Statements
## What's the difference between `for (;;)` and `while (1)`?

There should be no  difference: they both start an infinite  loop (whose body is
responsible for breaking out of via a `break` or `return` statement).

Some programmers prefer `for (;;)` because it  might be more efficient with some
(very?)  old compilers,  which needlessly  test  the `1`  condition before  each
iteration.

##
## Why should I use the `goto` statement sparingly?

It can make the code harder to understand and modify.

It gets harder to read because `goto`  can jump in either direction: backward or
forward (in contrast,  `break` and `continue` can only jump  forward).  This can
force the  reader to jump back  and forth when  reading the code, which  is less
natural than always reading forward.

It gets harder to  modify because it makes it possible for a  section of code to
be reached in different ways: by  "falling through" from the previous statement,
or by executing some `goto`(s) which  could be written anywhere in the function.
Before changing the  code below a label  (which a `goto` jumps  to), you'll have
to:

   - look for all the other `goto`s which can jump to it
   - make sure that the change is OK for all these `goto`s
   - make sure that the change is OK with the code above (for when control
     simply "falls through" the previous statement)

---

A code which  gets too difficult to read/maintain because  of an excessive usage
of `goto`s  is often called  "spaghetti code", because  its control flow  can be
compared with a bowl of spaghetti: twisted and tangled.

### When is it OK to use `goto`?

To break  out of  a nested construct  (e.g. a  nested loop, or  a loop  inside a
`switch`).  In that  case, `break` is not  enough; it can only break  out of the
innermost construct.

