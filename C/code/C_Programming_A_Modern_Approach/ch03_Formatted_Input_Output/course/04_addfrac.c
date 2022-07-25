// Purpose: add two fractions

// Input: 2 fractions (e.g. 5/6 and 3/4)
// Output: the sum of the 2 input fractions (e.g. 38/24)
// Don't try to reduce the resulting fraction to the lowest denominator.

// Reference: page 46 (paper) / 71 (ebook)

#include <stdio.h>

    int
main(void)
{
    int num1, denom1, num2, denom2, result_num, result_denom;

    printf("Enter first fraction: ");
    scanf("%d /%d", &num1, &denom1);
    printf("Enter second fraction: ");
    scanf("%d /%d", &num2, &denom2);

    result_num = num1 * denom2 + num2 * denom1;
    result_denom = denom1 * denom2;
    printf("The sum is %d/%d\n", result_num, result_denom);

    return 0;
}
