// Purpose: condense the dweight.c program by:{{{
//
//    1. replacing the assignments to `height`, `length`, and `width` with initializers
//    2. removing the `weight` variable, instead calculating `(volume + 165) / 166` within the last `printf()`
//}}}
// Reference: page 33 (paper) / 58 (ebook)

#include <stdio.h>

int main(void)
{
    int a, b, c, d, e;
    float f, g, h, i, j;

    // Notice that printing uninitialized variables can give random values:{{{
    //
    //     21875,-2066854288,32764,0,0
    //     -309.752930,0.000000,0.000000,0.000000,-309.762695
    //
    // Although, occasionally, there might be a 0 or 0.000000.
    //
    // Anyway, that's why you should always initialize your variables.
    //}}}
    printf("%d,%d,%d,%d,%d\n%f,%f,%f,%f,%f\n",
            a, b, c, d, e, f, g, h, i, j);

    return 0;
}
