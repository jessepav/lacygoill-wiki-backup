// Purpose: compute output of given program fragment
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, sum;

    sum = 0;
    for (i = 0; i < 10; i++)
    {
        if (i % 2)
            continue;
        sum += i;
    }
    printf("%d\n", sum);
    //     20
    // The loop sums all even integers below 10:
    //
    //     0 + 2 + 4 + 6 + 8 = 20

    return 0;
}
