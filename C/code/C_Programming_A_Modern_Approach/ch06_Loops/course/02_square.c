// Purpose: Print a table of squares (1, 4, 9, 16, 25, ...).{{{
//
// First, ask the user to enter a number `n`.
// Then print `n` lines of output, with  each line containing a number between 1
// and `n` together with its square:
//
//     This program prints a table of squares.
//     Enter number of entries in table: <5>
//              1         1
//              2         4
//              3         9
//              4        16
//              5        25
//}}}
// Reference: page 102 (paper) / 127 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, n;

    printf("This program prints a table of squares.\n");
    printf("Enter number of entries in table: ");
    scanf("%d", &n);

    i = 1;
    while (i <= n)
    {
        printf("%10d%10d\n", i, i * i);
        i++;
    }

    return 0;
}
