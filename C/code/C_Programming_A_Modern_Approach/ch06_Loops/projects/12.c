// Purpose: Same as  Project 11, but this  time continue adding terms  until the
// current  term  becomes  less  than  `epsilon`, where  `epsilon`  is  a  small
// (floating-point) number entered by the user.

// GCC Options: -Wno-conversion
// Reference: page 124 (paper) / 149 (ebook)

#include <stdio.h>

    int
main(void)
{
    float e, epsilon, term;
    int i, factorial;

    printf("Enter an epsilon floating-point number: ");
    scanf("%f", &epsilon);

    for (e = 1.0f, term = 1.0f, i = 1, factorial = 1; term > epsilon; i++)
    {
        factorial *= i;
        term = 1.0f / factorial;
        e += term;
    }

    printf("e ≈ %f\n", e);

    return 0;
}
