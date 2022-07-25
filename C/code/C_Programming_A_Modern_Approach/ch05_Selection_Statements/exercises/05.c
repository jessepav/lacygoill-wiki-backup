// Purpose: Is the following `if` statement legal?{{{
//
//     if (n >= 1 <= 10)
//         printf("n is between 1 and 10\n");
//
// If so, what does it do when `n` is equal to 0.
//}}}
// GCC Options: -Wno-parentheses -Wno-bool-compare
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n = 0;

    // A: Yes, the statement is legal.
    // But the code doesn't do what the reader expects.{{{
    //
    // `>=` and `<=` have the same precedence and are left associative.
    // Thus, the expression is computed like this:
    //
    //     ((n >= 1) <= 10)
    //
    // If `n` is 0:
    //
    //       ((0 >= 1) <= 10)
    //     ⇔
    //       (0 <= 10)
    //     ⇔
    //       1
    //
    // But obviously, 0 is  not between 1 and 10, so the  reader does not expect
    // the message to be printed.
    //}}}
    if (n >= 1 <= 10)
        printf("n is between 1 and 10\n");
        //     n is between 1 and 10

    return 0;
}
