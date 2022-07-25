// Purpose: study the `continue` statement
// Reference: page 112 (paper) / 137 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, n, sum;

    // `continue`  lets you  skip  part  of a  loop  iteration, by  transferring
    // control just *before* the end of the  loop body.  Its name can be read as
    // in: "continue after the end of this iteration".
    n = 0;
    sum = 0;
    while (n < 5)
    {
        scanf("%d", &i);
        // ignore zero as an input number
        if (i == 0)
            continue;
        sum += i;
        n++;
        // `continue` jumps to here
    }
    printf("the sum of all numbers is: %d\n", sum);

    // If `continue` were not available, you could have written this instead:
    //
    //     n = 0;
    //     sum = 0;
    //     while (n < 5)
    //     {
    //         scanf("%d", &i);
    //         if (i != 0)
    //         {
    //             sum += i;
    //             n++;
    //         }
    //     }
    //     printf("the sum of all numbers is: %d\n", sum);
    //
    // The downside  is that you need  to increase the indentation  level of all
    // the skipped  lines (to nest them  inside an `if` block),  making the code
    // harder to read.  In that regard, `continue` is better.

    return 0;
}
