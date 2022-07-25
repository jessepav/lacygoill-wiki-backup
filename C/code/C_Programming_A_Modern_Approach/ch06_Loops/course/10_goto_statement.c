// Purpose: study the `goto` statement
// Reference: page 113 (paper) / 138 (ebook)

#include <stdio.h>

    int
main(void)
{
    // `goto`  lets  you  jump  from  one arbitrary  statement  to  another,  by
    // transferring control to the name of a label.

    int d, n;
    printf("Enter a number: ");
    scanf("%d", &n);
    for (d = 2; d < n; d++)
        if (n % d == 0)
            goto done;
    done: ;
    if (d == n)
        printf("%d is prime\n", n);
    else
        printf("%d is divisible by %d\n", n, d);
    // In practice, the `break`, `continue`,  and `return` statements (which are
    // essentially `goto`s restricted to specific jump locations) as well as the
    // `exit()` function make `goto` rarely useful.
    // However it can be useful to escape nested control flow statements.{{{
    //
    // For example, a `switch` inside a `while`:
    //
    //     while (...)
    //     {
    //         switch (...)
    //         {
    //             ...
    //             goto loop_done;
    //          // ^--^
    //             ...
    //         }
    //     }
    //     loop_done: ;
    //
    // Here, `break` wouldn't work as intended,  because it would only exit from
    // the `switch`; not from the `while`.
    //}}}

    return 0;
}
