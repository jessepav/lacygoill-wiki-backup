// Purpose: What does the following statement print if `i` has the value 17?{{{
//
//     printf("%d\n", i >= 0 ? i : -i);
//
// And what if `i` has the value -17?
//}}}
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i;

    i = 17;
    printf("%d\n", i >= 0 ? i : -i);
    //     17{{{
    //
    // If `i` is  17, the first operand is true,  and the conditional expression
    // evaluates to the second operand, which is `i`, which is 17.
    //}}}

    i = -17;
    printf("%d\n", i >= 0 ? i : -i);
    //     17{{{
    //
    // If `i` is -17, the first operand is false, and the conditional expression
    // evaluates to the  third operand, which is `-i`, which  is `-(-17)`, which
    // is 17.
    //}}}

    return 0;
}
