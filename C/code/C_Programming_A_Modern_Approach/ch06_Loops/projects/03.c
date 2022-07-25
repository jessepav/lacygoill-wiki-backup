// Purpose: Reduce an input fraction to lowest terms.
//
//     Enter a fraction: <6/12>
//     In lowest terms: <1/2>

// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    int numerator, denominator, m, n, r, gcd;

    printf("Enter a fraction: ");
    scanf("%d /%d", &numerator, &denominator);

    // let's compute the GCD of the fraction's numerator and denominator
    m = numerator;
    n = denominator;

    while (n != 0)
    {
        r = m % n;
        m = n;
        n = r;
    }

    gcd = m;

    // let's divide both the numerator and  denominator by the GCD to reduce the
    // fraction to its lowest terms
    printf("In lowest terms: %d/%d\n", numerator / gcd, denominator / gcd);

    return 0;
}
