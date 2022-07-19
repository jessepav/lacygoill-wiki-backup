// Purpose: Extend the previous program to handle *three*-digit numbers.
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int num, digit1, digit2, digit3;

    printf("Enter a three-digit number: ");
    scanf("%d", &num);
    digit3 = num % 10;
    num /= 10;
    digit2 = num % 10;
    num /= 10;
    digit1 = num % 10;
    printf("The reversal is: %d%d%d\n", digit3, digit2, digit1);
}
