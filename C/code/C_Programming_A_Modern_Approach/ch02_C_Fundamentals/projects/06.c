// Purpose: modify the program of 05.c so that the polynomial is rewritten as:
//     (((((3x + 2)x - 5))x - 1)x + 7)x - 6
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

    int
main(void)
{
    float x, result;

    printf("Enter any real number x: ");
    scanf("%f", &x);

    // Notice how this new formula involves much fewer operations.{{{
    //
    // We went from 14 multiplications down to 5.
    // That's more effective.
    //}}}
    // To find this formula, one can use **Horner's method**.{{{
    //
    // Here is how it works:
    //
    //       3x⁵ + 2x⁴ - 5x³ - x² + 7x - 6
    //     =
    //       (3x⁴ + 2x³ - 5x² - x + 7) * x - 6
    //     =
    //       ((3x³ + 2x² - 5x - 1) * x + 7) * x - 6
    //     =
    //       (((3x² + 2x - 5) * x - 1) * x + 7) * x - 6
    //     =
    //       ((((3 * x + 2) * x - 5) * x - 1) * x + 7) * x - 6
    //
    // https://en.wikipedia.org/wiki/Horner%27s_method
    //}}}
    result = ((((3 * x + 2) * x - 5) * x - 1) * x + 7) * x - 6;
    printf("3x⁵ + 2x⁴ - 5x³ - x² + 7x - 6 = %.2f\n", result);
}
