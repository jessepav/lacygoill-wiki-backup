// Purpose: Handle an EAN (European Article Number) in a similar way as you did for a UPC.{{{
//
// European  countries use  a 13-digit  code, known  as an  EAN, instead  of the
// 12-digit UPC found in North America.  Each  EAN ends with a check digit, just
// as  a UPC  does.   The technique  for  calculating the  check  digit is  also
// similar:
//
//    - add the second, fourth, sixth, eighth, tenth, and twelfth digits
//    - add the first, third, fifth, seventh, ninth, and eleventh digits
//    - multiply the first sum by 3 and add it to the second sum
//    - subtract 1 from the total
//    - compute the remainder when the adjusted total is divided by 10
//    - subtract the remainder from 9
//
// For example, consider  Güllüglu Turkish Delight Pistachio  & Coconut, which
// has an EAN of 8691484260008.  The first sum is:
//
//     6 + 1 + 8 + 2 + 0 + 0 = 17
//
// And the second sum is:
//
//     8 + 9 + 4 + 4 + 6 + 0 = 31
//
// Multiplying the first sum by 3 and adding the second yields 82.
// Subtracting 1 gives 81.
// The remainder upon dividing by 10 is 1.
// When the remainder is  subtracted from 9, the result is  8, which matches the
// last digit of the  original code.  Your job is to modify  `UPC.c`, so that it
// calculates the  check digit  for an EAN.   The user will  enter the  first 12
// digits of the EAN as a single number:
//
//     Enter the first 12 digits of an EAN: <869148426000>
//     Check digit: <8>
//}}}
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int odd_indexed_sum, even_indexed_sum, check_digit,
        d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12;

    printf("Enter the first 11 digits of a UPC: \n");
    scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d",
            &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11, &d12);

    even_indexed_sum = d2 + d4 + d6 + d8 + d10 + d12;
    odd_indexed_sum = d1 + d3 + d5 + d7 + d9 + d11;

    check_digit = 9 - (even_indexed_sum * 3 + odd_indexed_sum - 1) % 10;
    printf("Check digit: %d\n", check_digit);
}
