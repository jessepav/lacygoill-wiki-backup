// Purpose: Calculate the number of digits in an integer.{{{
//
//     Enter a nonnegative integer: <60>
//     The number has 2 digit(s).
//
// Divide the user's  input by 10 repeatedly  until it becomes 0;  the number of
// divisions performed is the number of digits.
//}}}
// Reference: page 104 (paper) / 129 (ebook)

#include <stdio.h>

    int
main(void)
{
    int digits = 0, n;

    printf("Enter a nonnegative integer: ");
    scanf("%d", &n);

    // Here, `do` is better than `while`, because it makes it easier to handle the special case `n = 0`.{{{
    //
    //     while (n > 0)
    //     {
    //         n /= 10;
    //         digits++;
    //     }
    //
    // The body of  the latter loop would never run,  causing `digits` to remain
    // 0, which is not what we want (the number 0 has 1 digit, not 0).
    //}}}
    do
    {
        n /= 10;
        digits++;
    } while (n > 0);

    printf("The number has %d digit(s).\n", digits);

    return 0;
}
