// Purpose: compute output of a given program fragment, which uses a `do` loop
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i = 9384;
    do
    {
        printf("%d ", i);
        i /= 10;
    } while (i > 0);
    //     9384 938 93 9

    return 0;
}
