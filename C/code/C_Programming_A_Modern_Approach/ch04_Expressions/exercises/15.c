// Purpose: Give the values of `i` and `j` after some given expression statements have been executed.
// GCC Options: -Wno-unused-value
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j;

    i = 1;
    j = 2;
    i += j;
    printf("%d %d\n", i, j);
    //     3 2

    i = 1;
    j = 2;
    i--;
    printf("%d %d\n", i, j);
    //     0 2

    i = 1;
    j = 2;
    i * j / i;
    printf("%d %d\n", i, j);
    //     1 2

    i = 1;
    j = 2;
    i % ++j;
    printf("%d %d\n", i, j);
    //     1 3

    return 0;
}
