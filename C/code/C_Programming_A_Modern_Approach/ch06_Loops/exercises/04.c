// Purpose: Out of these 3 `for` loops, find the one which is not equivalent to the other two:{{{
//
//     for (i = 0; i < 10; i++) {...}
//     for (i = 0; i < 10; ++i) {...}
//     for (i = 0; i++ < 10;) {...}
//}}}
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    // A: It's the 3rd loop:
    //
    //     for (i = 0; i++ < 10;) {...}
    //
    // Because it  increments `i` before  the loop  body, while the  other loops
    // increment `i` after.
    //
    // ---
    //
    // In all the loops, before the 10th iteration, `i` is 9.
    // In the  first 2 loops, `i < 0`  must be true;  and it is before  the 10th
    // iteration.  In  the 3rd  loop, `i++ < 0`  must be true;  but it  is *not*
    // before the 10th iteration, because `i++` evaluates to 10.
    // IOW, the first 2 loops have 10 iterations, while the 3rd one only has 9.
    return 0;
}
