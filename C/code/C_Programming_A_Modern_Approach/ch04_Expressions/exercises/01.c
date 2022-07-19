// Purpose: evaluate various arithmetic expressions
// Reference: page 68 (paper) / 93 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;

    i = 5; j = 3;
    printf("%d %d\n", i / j, i % j);
    //     1 2
    //
    // `5 / 3` = 1 (rounded down)
    // `5 % 3` = 2

    i = 2; j = 3;
    printf("%d\n", (i + 10) % j);
    //     0
    //
    // `(i + 10)` = 12
    // `(i + 10) % j` = 12 % 3 = 0

    i = 7; j = 8, k = 9;
    printf("%d\n", (i + 10) % k / j);
    //     1
    //
    // `(i + 10)` = 17
    // `(i + 10) % k` = 17 % 9 = 8
    // `(i + 10) % k / j` = 8 / 8 = 1

    i = 1; j = 2, k = 3;
    printf("%d\n", (i + 5) % (j + 2) / k);
    //     0
    //
    // `(i + 5)` = 6
    // `(j + 2)` = 4
    // `(i + 5) % (j + 2)` = 6 % 4 = 2
    // `(i + 5) % (j + 2) / k` = 2 / 3 =  0 (rounded down)
}
