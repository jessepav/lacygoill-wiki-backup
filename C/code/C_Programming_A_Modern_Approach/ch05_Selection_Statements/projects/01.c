// Purpose: Write a program that calculates how many digits a number contains:{{{
//
//     Enter a number: <374>
//     The number <374> has <3> digits
//
// You can assume that the number has no more than four digits.
//
// Hint: Use `if` statements to test the  number.  For example, if the number is
// between 0 and 9, it has 1 digit.  If  the number is between 10 and 99, it has
// 2 digits.
//}}}
// Reference: page 95 (paper) / 120 (ebook)

#include <stdio.h>

    int
main(void)
{
    int num, digits_count;
    printf("Enter a number: ");
    scanf("%4d", &num);
    if (num < 10)
        digits_count = 1;
    else if (num < 100)
        digits_count = 2;
    else if (num < 1000)
        digits_count = 3;
    else
        digits_count = 4;

    printf("The number %d has %d digits\n", num, digits_count);
}
