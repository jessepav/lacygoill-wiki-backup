// Purpose: Extend the previous program to handle *three*-digit numbers.
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, digit1, digit2, digit3;

    printf("Enter a three-digit number: ");
    scanf("%d", &n);
    digit3 = n % 10;
    n /= 10;
    digit2 = n % 10;
    n /= 10;
    digit1 = n % 10;
    printf("The reversal is: %d%d%d\n", digit3, digit2, digit1);

    return 0;
}
