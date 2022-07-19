// Purpose: Supply parentheses to show how a C compiler would interpret some given expressions.
// Reference: page 70 (paper) / 95 (ebook)

#include <stdio.h>

    int
main(void)
{
    //     a * b - c * d + e
    //     (a * b) - (c * d) + e
    //     ((a * b) - (c * d)) + e
    //     (((a * b) - (c * d)) + e)
    //     ^-----------------------^

    //     a / b % c / d
    //     (a / b) % c / d
    //     ((a / b) % c) / d
    //     (((a / b) % c) / d)
    //     ^-----------------^

    //     - a - b + c - + d
    //     (-a) - b + c - (+d)
    //     ((-a) - b) + c - (+d)
    //     (((-a) - b) + c) - (+d)
    //     ((((-a) - b) + c) - (+d))
    //     ^-----------------------^

    //     a * - b / c - d
    //     a * (-b) / c - d
    //     (a * (-b)) / c - d
    //     ((a * (-b)) / c) - d
    //     (((a * (-b)) / c) - d)
    //     ^--------------------^
}
