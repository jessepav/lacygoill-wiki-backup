// Purpose: write calls of `printf()` that display a `float` variable `x` in various formats
// Reference: page 49 (paper) / 74 (ebook)

#include <stdio.h>

    int
main(void)
{
    float x = 123.456789f;

    // (a) Exponential notation;
    // left-justified in a field of size 8;
    // one digit after the decimal point
    printf("|%-8.1e|\n", x);

    // (b) Exponential notation;
    // right-justified in a field of size 10;
    // six digits after the decimal point
    printf("|%10.6e|\n", x);

    // (c) Fixed decimal notation;
    // left-justified in a field of size 8;
    // three digits after the decimal point
    printf("|%-8.3f|\n", x);

    // (d) Fixed decimal notation;
    // right-justified in a field of size 6;
    // no digits after the decimal point
    printf("|%6.0f|\n", x);

    return 0;
}
