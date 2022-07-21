// Purpose: Find the largest and smallest of 4 integers entered by the user:{{{
//
//     Enter four integers: <21> <43> <10> <35>
//     Largest: 43
//     Smallest: 10
//
// Use as few `if` statements as possible.  Hint: 4 `if` statements are sufficient.
//}}}
// Reference: page 96 (paper) / 121 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n1, n2, n3, n4, min1, max1, min2, max2, min, max;

    printf("Enter four integers: ");
    scanf("%d%d%d%d", &n1, &n2, &n3, &n4);

    // round 1: first match
    if (n1 < n2)
    {
        min1 = n1;
        max1 = n2;
    }
    else
    {
        min1 = n2;
        max1 = n1;
    }

    // round 1: second match
    if (n3 < n4)
    {
        min2 = n3;
        max2 = n4;
    }
    else
    {
        min2 = n4;
        max2 = n3;
    }

    // round 2: losers' final
    if (min1 < min2)
        min = min1;
    else
        min = min2;

    // round 2: winners' final
    if (max1 > max2)
        max = max1;
    else
        max = max2;

    printf("Largest: %d\nSmallest: %d\n", max, min);
}
