// Purpose: rewrite a given loop so that its body is empty
// Reference: page 122 (paper) / 147 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, m;
    m = 128;

    // Original loop:
    //
    //     for (n = 0; m > 0; n++)
    //         m /= 2;

    // New loop with empty body:
    //
    for (n = 0; m > 0; n++, m /= 2)
    //                    ^------^
        ;

    printf("%d", n);
    //     8
    //
    // 8 because 128 can be divided by 2 seven times, and `n` is incremented one
    // more time at the end of the last iteration.

    return 0;
}
