// Purpose: Compute an approximation of the Euler's number.{{{
//
// Use this expression:
//
//     1 + 1/1! + 1/2! + 1/3! + ... + 1/n!
//                                      ^^
//                                      factorial n
//
// Where `n` is an integer entered by the user.
//}}}
// GCC Options: -Wno-conversion
// Reference: page 124 (paper) / 149 (ebook)

#include <stdio.h>

    int
main(void)
{
    float e;
    int i, n, factorial;

    printf("Enter a number: ");
    scanf("%d", &n);

    for (e = 1.0f, i = 1, factorial = 1; i <= n; i++)
    {
        factorial *= i;
        e += 1.0f / factorial;
    }

    printf("e ≈ %f\n", e);

    return 0;
}
