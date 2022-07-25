// Purpose: study how the `while` statement works
// Reference: page 100 (paper) / 125 (ebook)

#include <stdio.h>

    int
main(void)
{
// Syntax of a `while` statement:
//
//     while (expr) statement;

    int i = 1;
    int n = 10;

    // compute the smallest power of 2 that  is greater than or equal to a given
    // number `n`
    while (i < n)
        i *= 2;
    printf("%d\n", i);
    //     16

    i = 10;
    // Just like  with `if`, we can  use the compound statement  to include more
    // than 1 statement inside a `while`.
    while (i > 0)
    {
        printf("T minus %d and counting\n", i);
        i--;
    }
    //     T minus 16 and counting
    //     T minus 15 and counting
    //     ...
    //     T minus 2 and counting
    //     T minus 1 and counting

    return 0;
}
