// Purpose: study the `break` statement
// Reference: page 111 (paper) / 136 (ebook)

#include <stdio.h>

    int
main(void)
{
    int d, n;
    printf("Enter a number: ");
    scanf("%d", &n);

    // In `for` and `while` loops, the **exit point** is before the loop body.
    // In `do` loops, it's after.
    // But if you want the exit point to be in the middle, you need `break`.
    // As an example, the purpose of this loop is to test whether a given number
    // is prime.
    for (d = 2; d < n; d++)
        if (n % d == 0)
            break;
            // ^^
            // We exit the loop as soon as we find a divisor of `n`.

    // If we didn't find a divisor, `d` will go up to `n - 1`, and at the end of
    // the last iteration, it will be incremented to `n`.
    if (d == n)
        printf("%d is prime\n", n);
    else
        printf("%d is divisible by %d\n", n, d);


    // `break` transfers control out of the *innermost* enclosing `while`, `do`,
    // `for`, or `switch` statement (just past  its end).  Thus, when the latter
    // statements are nested, `break` can only escape 1 level of nesting.
    //
    //     while (...)
    //     {
    //         switch (...)
    //         {
    //             ...
    //             break;
    //             ...
    //         }
    //     }
    //
    // Here,  `break` transfers control out  of the `switch` statement,  but not
    // out of the `while` loop.
    //
    // If you want to  escape *all* levels of nesting, you  can refactor out the
    // nested statements into a function, and call it.  Inside the function, use
    // `return` instead  of `break`. `return`  will exit the function  no matter
    // the level of nesting.
    //
    // If you want escape *some* levels of nesting, you can use `goto`.
    return 0;
}
