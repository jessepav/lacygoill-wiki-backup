// Purpose: compute output of a given program fragment, which uses a `for` loop
// GCC Options: -Wno-unused-value -Wno-strict-overflow
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j;

    //                     useless, because no side effect, and discarded value
    //                     v---v
    for (i = 5, j = i - 1; i > 0, j > 0; --i, j = i - 1)
        printf("%d ", i);
    //     5 4 3 2
    // Evolution of `(i, j)` across all iterations:{{{
    //
    //     (i, j) = (5, 4)
    //     (i, j) = (4, 3)
    //     (i, j) = (3, 2)
    //     (i, j) = (2, 1)
    //     (i, j) = (1, 0)
    //                  ^
    //
    // `j = 0` prevents the fifth iteration from being run.
    //}}}

    return 0;
}
