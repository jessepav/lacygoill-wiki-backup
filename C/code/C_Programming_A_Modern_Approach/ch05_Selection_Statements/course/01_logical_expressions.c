// Purpose: study how logical expressions are built
// GCC Options: -Wno-parentheses -Wno-tautological-compare -Wno-conversion
// Reference: page 74 (paper) / 99 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k, m;
    float f;

    // Expressions using  relational operators don't yield  booleans; they yield
    // boolean *numbers*.
    i = 1;
    j = 2;
    printf("%d %d\n", i < j, i > j);
    //     1 0

    // same thing for equality operators
    printf("%d %d\n", i == j, i != j);
    //     0 1


    // Relational operators  are allowed  to compare  operands with  mixed types
    // (e.g. an integer and a floating-point number).
    f = 2.5;
    printf("%d %d\n", i < f, i > f);
    //     1 0

    // The relational operators have lower precedence than the arithmetic operators.{{{
    //
    // For example:
    //
    //       i + j < k - 1
    //     ⇔
    //       (i + j) < (k - 1)
    //}}}
    k = 3;
    printf("%d %d %d\n",
             i + j  <  k - 1,
            (i + j) < (k - 1),
             i + (j < k) - 1);
    //     0 0 1
    //     ^ ^
    //     identical

    // The equality operators have lower precedence than the relational operators.{{{
    //
    // For example:
    //
    //       i < j == j < k
    //     ⇔
    //       (i < j) == (j < k)
    //}}}
    k = 1;
    printf("%d %d %d\n",
             i < j  ==  j < k,
            (i < j) == (j < k),
            i < (j == j) < k);
    //     0 0 1
    //     ^ ^
    //     identical


    // Logical operators accept any integer as operands; not just 0 and 1.
    i = 2; j = 3; k = 4;
    printf("%d %d %d\n", i && j, i || j, !k);
    //     1 1 0

    // Both `&&` and `||` perform "short-circuit" evaluation of their operands.{{{
    //
    // They first  evaluate their  left operand,  and if  the latter's  value is
    // enough  to deduce  the  value of  the whole  expression,  then the  right
    // operand is *not* evaluated.
    //}}}
    // This feature is useful to refactor a simple `if` statement into a logical expression:{{{
    //
    //       if (expr1)
    //           expr2;
    //
    //     ⇔
    //
    //       (expr1) && expr2;
    //}}}
    // It works because `&&` and `||` impose a sequence point.
    i = 0; j = 0;
    printf("%d ", i > 0 && ++j > 0);
    printf("%d\n", j);
    //     0 0
    //       ^
    // Here, we can see that `j` has not been incremented as a side effect of evaluating `++j`.{{{
    //
    // Because the  latter was on the  right of `&&`, which  has short-circuited
    // the evaluation of  its right operand because its left  one evaluated to 0
    // (`i > 0` is false).
    //}}}

    // The  logical  operators  have  lower precedence  than  the  equality  and
    // relational operators.
    i = 1; j = 2; k = m = 3;
    printf("%d %d\n",
            (i < j) && (k == m),
             i < j  &&  k == m);
    //     1 1
    // Note: All these logical operators are binary and left associative.
    // Except `!`, which is unary and right associative.


    // The syntax of a conditional expression is:{{{
    //
    //     expr1 ? expr2 : expr3
    //
    // It  relies  on  the  (ternary)  conditional  operator  which  has  a  low
    // precedence.   Only  the assignments  and  comma  operators have  a  lower
    // precedence.
    //
    // It's evaluated in 2 stages.
    // First, `expr1`, then depending on the result (zero or non zero), `expr2` or `expr3`.
    //}}}
    k = i > j ? i : j; // k is now 2
    k = (i >= 0 ? i : 0) + j; // k is now 3

    // If  the operands  have mixed  types, one  being an  integer, the  other a
    // `float`, the result is a `float`.
    printf("%f\n", i > 0 ? i : f);
    //     1.000000
}
