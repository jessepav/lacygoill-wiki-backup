// Purpose: Modify the `UPC.c` program so that it checks whether a UPC is valid.
// After the user enters a UPC, the program should display either VALID or NOT VALID.
// Reference: page 96 (paper) / 121 (ebook)

#include <stdio.h>

    int
main(void)
{
    int d, i1, i2, i3, i4, i5, j1, j2, j3, j4, j5,
        odd_indexed_sum, even_indexed_sum, expected, check_digit;

    printf("Enter first (single) digit: \n");
    scanf("%1d", &d);

    printf("Enter first group of five digits: \n");
    scanf("%1d%1d%1d%1d%1d", &i1,  &i2, &i3, &i4, &i5);

    printf("Enter second group of five digits: \n");
    scanf("%1d%1d%1d%1d%1d", &j1,  &j2, &j3, &j4, &j5);

    printf("Enter the last (single) digit: \n");
    scanf("%1d", &check_digit);

    even_indexed_sum = i1 + i3 + i5 + j2 + j4;
    odd_indexed_sum = d + i2 + i4 + j1 + j3 + j5;
    expected = 9 - (odd_indexed_sum * 3 + even_indexed_sum - 1) % 10;

    if (check_digit == expected)
        printf("VALID\n");
    else
        printf("NOT VALID\n");
}
