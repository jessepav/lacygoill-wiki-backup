// Purpose: ask the user to enter a value for `x`, then display the value of:
//     3x⁵ + 2x⁴ - 5x³ - x² + 7x - 6
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

    int
main(void)
{
    float x, result;

    printf("Enter any real number x: ");
    scanf("%f", &x);

    result = 3 * (x * x * x * x * x)
           + 2 * (x * x * x * x)
           - 5 * (x * x * x)
           - (x * x)
           + 7 * x
           - 6;
    printf("3x⁵ + 2x⁴ - 5x³ - x² + 7x - 6 = %.2f\n", result);
}
