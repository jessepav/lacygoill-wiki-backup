// Purpose: study arithmetic operators
// GCC Options: -Wno-conversion{{{
//
// This is necessary to suppress an error on this line:
//
//     sum = i + f;
//
//    > Do not warn for explicit casts like "abs ((int) x)" and "ui = (unsigned) -1", [...]
//
// Source: `man gcc /OPTIONS/;/Options to Request or Suppress Warnings/;/-Wconversion`
//
// ---
//
// Alternatively, you could cast the integer into a float:
//
//     sum = (float)i + f;
//           ^-----^
//}}}
// Reference: page 54 (paper) / 79 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;
    float f, division, sum;

    // You can  mix an integer  with a  floating-point operand in  an arithmetic
    // computation.  The result is a floating-point number.
    i = 9;
    f = 2.5f;
    sum = i + f;
    printf("%f\n", sum);
    //     11.500000

    f = 6.7f;
    i = 2;
    division = f / (float)i;
    printf("%f\n", division);
    //     3.350000

    // The result of a division is  always an integer; if necessary, the decimal
    // part is truncated.
    i = 1;
    j = 2;
    printf("%d\n", i / j);
    //     0

    // You can  use parentheses  to make  the implicit  higher precedence  of an
    // operator more explicit:
    k = 3;
    //                 v     v
    printf("%d\n", i + (j * k));
    //     7

    // Or to change the order of the operations:
    //             v     v
    printf("%d\n", (i + j) * k);
    //     9
}
