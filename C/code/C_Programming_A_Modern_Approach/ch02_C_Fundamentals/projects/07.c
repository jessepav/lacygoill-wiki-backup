// Purpose: show how to pay a  user-inputted amount using the smallest number of
// $20, $10, $5, and $1 bills
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

    int
main(void)
{
    int amount;
    // We could get away without any of these variables.{{{
    //
    //     printf("$20 bills: %d\n", amount / 20);
    //     amount -= 20 * (amount / 20);
    //
    //     printf("$10 bills: %d\n", ten_bills);
    //     amount -= 10 * (amount / 10);
    //
    //     ...
    //
    // But I find they make the code more readable.
    // For example, we might think that the compiler simplifies this:
    //
    //     amount -= (amount / 20) * 20;
    //
    // into this:
    //
    //     amount -= amount;
    //
    // Which would be wrong.  But that's not what happens; because, `amount / 20`
    // is computed separately, and is rounded to the nearest integer.
    //
    // In any case, with our current  implementation, there is no doubt that the
    // code works; we would not break it while trying to simplify it.
    //}}}
    int twenty_bills, ten_bills, five_bills, one_bills;

    printf("Enter a dollar amount: ");
    scanf("%d", &amount);

    twenty_bills = amount / 20;
    amount -= twenty_bills * 20;

    ten_bills = amount / 10;
    amount -= ten_bills * 10;

    five_bills = amount / 5;
    amount -= five_bills * 5;

    one_bills = amount;

    printf("$20 bills: %d\n", twenty_bills);
    printf("$10 bills: %d\n", ten_bills);
    printf(" $5 bills: %d\n", five_bills);
    printf(" $1 bills: %d\n", one_bills);
}
