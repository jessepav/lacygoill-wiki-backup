// Purpose: study integer types
// Reference: page 125 (paper) / 150 (ebook)

#include <stdio.h>
#include <math.h>

    int
main(void)
{
    // The integer types are divided into 2 categories: signed and unsigned.

    signed short int a = pow(2, 15) - 1;
    printf("the largest 16-bit integer is: %d\n", a);
    //     the largest 16-bit integer is: 32767
    //                                    ^---^
    // Its binary representation is:
    //
    //     sign bit (here, positive)
    //     v
    //     0111111111111111
    //     ^--------------^
    //         16 bits

    signed int b = pow(2, 31) - 1;
    printf("the largest 32-bit integer is: %d\n", b);
    //     the largest 32-bit integer is: 2147483647
    //                                    ^--------^
    // Its binary representation is:
    //
    //     sign bit (here, positive)
    //     v
    //     01111111111111111111111111111111
    //     ^------------------------------^
    //                 32 bits

    return 0;
}
