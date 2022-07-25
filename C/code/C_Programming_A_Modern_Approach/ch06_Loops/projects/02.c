// Purpose: Compute and display the greatest common divisor (GCD) of 2 input numbers.{{{
//
//     Enter two integers: <12 28>
//     Greatest common divisor: <4>
//
// Hint: The  classic  algorithm  for  computing  the  GCD,  known  as  Euclid's
// algorithm, goes as follows:
//
// Let `m`  and `n` be  variables holding  the two numbers.   If `n` is  0, then
// stop: `m` is  the GCD.  Otherwise, compute the remainder  when `m` is divided
// by `n`.  Copy `n` into `m` and copy the remainder into `n`.  Then, repeat the
// process, starting with testing whether `n` is 0.
//}}}
// Reference: page 122 (paper) / 147 (ebook)

#include <stdio.h>

    int
main(void)
{
    int m, n, r, gcd;

    printf("Enter two integers: ");
    scanf("%d%d", &m, &n);

    while (n != 0)
    {
        r = m % n;
        m = n;
        n = r;
    }

    gcd = m;
    printf("Greatest common divisor: %d\n", gcd);

    return 0;
}
