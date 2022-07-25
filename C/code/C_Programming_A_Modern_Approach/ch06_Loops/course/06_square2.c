// Purpose: improve `square.c` by converting its `while` loop with a `for` one
// Reference: page 110 (paper) / 135 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, n;

    printf("This program prints a table of squares.\n");
    printf("Enter number of entries in table: ");
    scanf("%d", &n);

    for (i = 1; i <= n; i++)
        printf("%10d%10d\n", i, i * i);

    return 0;
}
