// Purpose: Print a table of squares using an odd method (odd as in "not even"; not as in "weird").{{{
//
// Use a  `for` loop  which initializes one  variable (`square`),  tests another
// (`i`), and increments a third (`odd`).
//
// `i` is the number to be squared, `square`  is the square of `i`, and `odd` is
// the  odd  number  that must  be  added  to  the  current square  to  get  the
// next  square (allowing  the program  to compute  consecutive squares  without
// performing any multiplications).
//
// This algorithm  relies on  the fact that  the difference  between consecutive
// squares is the set of odd numbers, in their increasing order.
//
//       (n + 1)² - n²
//     = (n² + 2n + 1) - n²
//     = 2n + 1
//
// Consequently, to jump from square 1 to square 4, you can add the odd number 3.
// To jump from square 4 to square 9, you can add the next odd number 5.
// Etc.
//}}}
// Reference: page 110 (paper) / 135 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, n, odd, square;

    printf("This program prints a table of squares.\n");
    printf("Enter number of entries in table: ");
    scanf("%d", &n);

    i = 1;
    odd = 3;
    // This illustrates that  the 3 expressions in a `for`  statement don't have
    // to use the same variable(s).
    for (square = 1; i <= n; odd += 2)
    {
        printf("%10d%10d\n", i, square);
        i++;
        square += odd;
    }

    return 0;
}
