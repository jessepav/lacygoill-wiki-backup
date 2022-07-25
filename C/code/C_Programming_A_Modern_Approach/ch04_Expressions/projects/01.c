// Purpose: Reverse the digits in a number.{{{
//
// Write a program that asks the user to enter a two-digit number, then
// prints  the number  with its  digits reversed.   A session  with the  program
// should have the following appearance:
//
//     Enter a two-digit number: <28>
//     The reversal is: <82>
//
// Read the number using `%d`, then break it into two digits.
// Hint: If  `n` is  an integer,  then `n % 10`  is the  last digit  in `n`  and
// `n / 10` is `n` with the last digit removed.
//}}}
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, digit1, digit2;

    printf("Enter a two-digit number: ");
    scanf("%d", &n);
    digit1 = n / 10;
    digit2 = n % 10;
    printf("The reversal is: %d%d\n", digit2, digit1);

    return 0;
}
