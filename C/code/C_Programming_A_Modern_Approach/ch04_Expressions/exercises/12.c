// Purpose: compute various arithmetic expressions
// Reference: page 70 (paper) / 95 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j;

    i = 5;
    j = ++i * 3 - 2;
    printf("%d %d\n", i, j);
    //     6 16

    i = 5;
    j = 3 - 2 * i++;
    printf("%d %d\n", i, j);
    //     6 -7

    i = 7;
    j = 3 * i-- + 2;
    printf("%d %d\n", i, j);
    //     6 23

    i = 7;
    j = 3 + --i * 2;
    printf("%d %d\n", i, j);
    //     6 15

    return 0;
}
