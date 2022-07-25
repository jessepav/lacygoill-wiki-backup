// Purpose: When studying the `break` statement, we wrote a "prime-testing" loop.
// Make it  more effecient  so that it  doesn't test all  numbers between  up to
// `n - 1`, but only up to `√n`.
// Hint: Don't try to compute the square root of `n`; instead, compare `d * d` with `n`.
// Reference: page 122 (paper) / 147 (ebook)

#include <stdio.h>

    int
main(void)
{
    int d, n;

    printf("Enter a number: ");
    scanf("%d", &n);

    // Original loop:
    //
    //     for (d = 2; d < n; d++)
    //         if (n % d == 0)
    //             break;

    // New optimized loop:
    for (d = 2; d * d <= n; d++)
        if (n % d == 0)
            break;

    // In the original code, the controlling expression is different.{{{
    //
    // Because it relies on this equivalence:
    //
    //     n is prime
    //     ⇔
    //     d == n
    //
    // It worked because  when `n` is prime the original  loop always increments
    // `d` up to `n`.  But that's not true with the new loop.
    //
    // For the latter, we need to rely on a new equivalence:
    //
    //     n is prime
    //     ⇔
    //     d * d > n
    //}}}
    // You could also write `(n % d != 0)`.{{{
    //
    // But it would not work as expected in the special case `n = 2`.
    //
    //     Enter a number: 2
    //     2 is divisible by 2
    //     ^-----------------^
    //              ✘
    //
    // That's because the loop body is not even run once in this case.
    // It only  starts being run from  `n = 4` (because `n` must  be higher than
    // the square of `d` which is initialized with 2).
    //
    // Besides, it  would probably be  more costly (because the  operators which
    // perform  a division,  like  `%`,  are more  costly  than operators  which
    // perform a multiplication).
    //}}}
    if (d * d > n)
        printf("%d is prime\n", n);
    else
        printf("%d is divisible by %d\n", n, d);

    return 0;
}
