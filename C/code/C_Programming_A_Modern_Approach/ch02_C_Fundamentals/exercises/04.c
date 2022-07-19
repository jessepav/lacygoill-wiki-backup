// Purpose: study which values are stored in uninitialized variables
// Reference: page 33 (paper) / 58 (ebook)

#include <stdio.h>

    int
main(void)
{
    int a, b, c, d, e;
    float f, g, h, i, j;

    printf("%d,%d,%d,%d,%d\n%f,%f,%f,%f,%f\n",
            a, b, c, d, e, f, g, h, i, j);
}
