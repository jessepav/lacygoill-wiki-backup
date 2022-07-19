// Purpose: Compute the "check digit" for an arbitrary UPC.{{{
//
// UPC stands for Universal Product Code.
// It's a twelve-digit number printed below a bar code; it identifies a product,
// as well as its manufacturer.
//
// The first digit identifies the type of item.
// The subequent  2 groups of five  digits identify resp. the  manufacturer, and
// the product.
// The last digit (aka the check digit) can be used to find most UPCs containing
// an error.
//
// The check digit must satisfy this relationship:
//
//     check digit = 9 - ((sum of odd-indexed digits) * 3 + (sum of even-indexed digits) - 1) % 10
//
// For example: if a `UPC` is `0 13800 15173 5`:
//
//     sum of odd-indexed digits = 0 + 3 + 0 + 1 + 1 + 3 = 8
//     sum of even-indexed digits =  1 + 8 + 0 + 5 + 7 = 21
//
//     ⇒
//
//       9 - ((sum of odd-indexed digits) * 3 + (sum of even-indexed digits) - 1) % 10
//     =
//       9 - (8 * 3 + 21 - 1) % 10
//     =
//       9 - 44 % 10
//     =
//       9 - 4
//     =
//       5
//       ^
//       ✔
//
// The result matches the  check digit, which means that the  UPC is unlikely to
// contain an error.
//}}}
// Reference: page 56 (paper) / 81 (ebook)

#include <stdio.h>

    int
main(void)
{
    int d, i1, i2, i3, i4, i5, j1, j2, j3, j4, j5,
        odd_indexed_sum, even_indexed_sum, check_digit;

    printf("Enter first (single) digit: \n");
    scanf("%1d", &d);

    // Notice how we can specify a limit to a read number:{{{
    //
    //     scanf("%1d", &i);
    //             ^
    //
    // It  doesn't matter  how long  the number  you input  is; when  processing
    // `%1d`, `scanf()` will only read its first digit.
    //}}}
    //   Here, we use this syntax to read each group as five *one*-digit numbers; instead of a *five*-digit number.{{{
    //
    // First, it's more convenient for our next computations.
    // We're not interested in the number as a whole, but in its digits.
    //
    // Second, some old  compilers limit the maximum value of  an `int` variable
    // to 32767.  Which  means we wouldn't be  able to process a  number such as
    // 55555, with  these compilers.  OTOH, if  we only read the  digits, we can
    // handle any five-digit number (even 99999) regardless of the compiler.
    //}}}
    printf("Enter first group of five digits: \n");
    scanf("%1d%1d%1d%1d%1d", &i1,  &i2, &i3, &i4, &i5);

    printf("Enter second group of five digits: \n");
    scanf("%1d%1d%1d%1d%1d", &j1,  &j2, &j3, &j4, &j5);

    // remember that the first digit is not `i1`, but `d`
    even_indexed_sum = i1 + i3 + i5 + j2 + j4;
    odd_indexed_sum = d + i2 + i4 + j1 + j3 + j5;

    check_digit = 9 - (odd_indexed_sum * 3 + even_indexed_sum - 1) % 10;
    printf("Check digit: %d\n", check_digit);

    // Tests:
    //
    //    - for `0 51500 24128`, the check digit should be 8
    //    - for `0 31200 01005`, the check digit should be 6
}
