// Purpose: evaluate various arithmetic expressions
// Reference: page 69 (paper) / 94 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;

    i = 7; j = 8;
    i *= j + 1;
    printf("%d %d\n", i, j);
    //     63 8

    i = j = k = 1;
    i += j += k;
    printf("%d %d %d\n", i, j, k);
    //     3 2 1

    i = 1; j = 2; k = 3;
    i -= j -= k;
    printf("%d %d %d\n", i, j, k);
    //     2 -1 3{{{
    //
    // `j -= k` is evaluated first.
    // It decrements `j` by `3`, which gives `j = 2 - 3 = -1`.
    //
    // Then, `i -= j` is evaluated.
    // It decrements `i` by `-1`, which gives `i = 1 - (-1) = 2`.
    //}}}

    i = 2; j = 1; k = 0;
    i *= j *= k;
    printf("%d %d %d\n", i, j, k);
    //     0 0 0
}
