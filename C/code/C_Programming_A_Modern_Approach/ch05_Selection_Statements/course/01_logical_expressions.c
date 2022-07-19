// Purpose: study how logical expressions are built
// Reference: page 74 (paper) / 99 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;
    float f;

    // Expressions using  relational operators don't yield  booleans; they yield
    // boolean *numbers*.
    i = 1;
    j = 2;
    printf("%d %d\n", i < j, i > j);
    //     1 0

    // Relational operators  are allowed  to compare  operands with  mixed types
    // (e.g. an integer and a floating-point number).
    f = 2.5;
    printf("%d %d\n", i < f, i > f);
    //     1 0

    // The precedence of the relational operators is lower than that of the arithmetic operators.{{{
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
}
