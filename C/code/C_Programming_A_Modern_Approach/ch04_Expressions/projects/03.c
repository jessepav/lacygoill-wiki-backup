// Purpose: Rewrite the  previous program so  that it  prints the reversal  of a
// three-digit number without using arithmetic to split the number into digits.
// Hint: See the `UPC.c` program.
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int digit1, digit2, digit3;

    printf("Enter a three-digit number: ");
    scanf("%1d%1d%1d", &digit1, &digit2, &digit3);
    printf("The reversal is: %d%d%d\n", digit3, digit2, digit1);

    return 0;
}
