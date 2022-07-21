// Purpose: Is the following `if` statement legal?{{{
//
//     if (n == 1-10)
//         printf("n is between 1 and 10\n");
//
// If so, what does it do when `n` is equal to 5.
//}}}
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n = 5;

    // A: Yes, the statement is legal.
    // But the code doesn't do what the reader expects.{{{
    //
    // The expression is computed like this:
    //
    //       n == (1-10)
    //
    // If `n` is 5:
    //
    //       n == (1-10)
    //     ⇔
    //       5 == -9
    //     ⇔
    //       0
    //
    // And obviously, 5 *is*  between 1 and 10, so the  reader *does* expect the
    // message to be printed.  But nothing will be printed.
    //}}}
    if (n == 1-10)
        printf("n is between 1 and 10\n");
}
