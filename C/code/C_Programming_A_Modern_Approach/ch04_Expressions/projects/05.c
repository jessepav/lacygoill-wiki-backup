// Purpose: Rewrite `UPC.c` so that the user enters 11 digits at one time.{{{
//
// Instead  of entering  one  digit, then  five digits,  and  then another  five
// digits.
//
//     Enter the first 11 digits of a UPC: <01380015173>
//     Check digit: 5
//}}}
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int odd_indexed_sum, even_indexed_sum, check_digit,
        d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11;

    printf("Enter the first 11 digits of a UPC: \n");
    scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d",
            &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11);

    even_indexed_sum = d2 + d4 + d6 + d8 + d10;
    odd_indexed_sum = d1 + d3 + d5 + d7 + d9 + d11;

    check_digit = 9 - (odd_indexed_sum * 3 + even_indexed_sum - 1) % 10;
    printf("Check digit: %d\n", check_digit);

    // Tests:
    //
    //    - for `0 51500 24128`, the check digit should be 8
    //    - for `0 31200 01005`, the check digit should be 6
}
