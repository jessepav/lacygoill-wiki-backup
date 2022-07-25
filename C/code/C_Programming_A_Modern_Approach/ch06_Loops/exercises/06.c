// Purpose: translate the program fragment of Exercise 1 into a single `for` statement
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    //  v---------------------------v
    for (int i = 1; i <= 128; i *= 2)
    {
        printf("%d ", i);
    }
    //     1 2 4 8 16 32 64 128

    return 0;
}
