// Purpose: Generalize Project 1 in Chapter 4 so that it can reverse any number,
// regardless of how many digits it contains.
// Hint: Use a `do` loop that repeatedly divides the number by 10, stopping when
// it reaches 0.

// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n;

    printf("Enter a number: ");
    scanf("%d", &n);

    printf("The reversal is: ");
    // A  `do` statement  is better  than a  `while` one,  because it  correctly
    // handles the special case `n = 0`.
    do
    {
        printf("%d", n % 10);
        n /= 10;
    } while (n != 0);

    return 0;
}
