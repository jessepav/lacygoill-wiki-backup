// Purpose: translate the program fragment of Exercise 2 into a single `for` statement
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    //  v----------------------------v
    for (int i = 9384; i > 0; i /= 10)
    {
        printf("%d ", i);
    }
    //     9384 938 93 9

    return 0;
}
