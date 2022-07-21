// Purpose: compute various arithmetic expressions
// GCC Options: -Wno-float-conversion -Wno-sequence-point
// Reference: page 70 (paper) / 95 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j;

    i = 6;
    j = i += i;
    printf("%d %d\n", i, j);
    //     12 12
    // There is no UB here.{{{
    //
    // Even though we have an expression which has a side effect (`i += i`), and
    // which refers to the same variable twice.
    // The reading  of `i`, and the  computing of `i + i` does  not overlap with
    // the assignment of `i`.
    // }}}

    i = 5;
    j = (i -= 2) + 1;
    printf("%d %d\n", i, j);
    //     3 4

    i = 7;
    j = 6 + (i = 2.5);
    printf("%d %d\n", i, j);
    //     2 8

    i = 2; j = 8;
    j = (i = 6) + (j = 3);
    printf("%d %d\n", i, j);
    //     6 9
    // TODO: Why does the compiler complain without `-Wno-sequence-point`?{{{
    //
    //     operation on ‘j’ may be undefined [-Werror=sequence-point]
    //
    // How could the `j` assignment cause a UB?
    // The execution  of the embedded  `j = 3` assignment would need  to overlap
    // with the outer `j` assignment.  But that can't happen, right?
    // Before assigning an expression to a variable, it's fully computed, right?
    // And why didn't `j = i += i` gave a similar warning earlier?
    //}}}
}
