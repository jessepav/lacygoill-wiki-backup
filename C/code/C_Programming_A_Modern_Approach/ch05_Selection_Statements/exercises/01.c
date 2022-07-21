// Purpose: compute various logical expressions using relational and equality operators
// GCC Options: -Wno-parentheses
// Reference: page 93 (paper) / 118 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;

    i = 2;
    j = 3;
    k = i * j == 6;
    printf("%d\n", k);
    //     1{{{
    //
    //       k = ((i * j) == 6)
    //     ⇔
    //       k = (6 == 6)
    //     ⇔
    //       k = 1
    //}}}

    i = 5;
    j = 10;
    k = 1;
    printf("%d\n", k > i < j);
    //     1{{{
    //
    //       (k > i) < j
    //     ⇔
    //       (1 > 5) < 10
    //     ⇔
    //       0 < 10
    //}}}

    i = 3;
    j = 2;
    k = 1;
    printf("%d\n", i < j == j < k);
    //     1{{{
    //
    //       (i < j) == (j < k)
    //     ⇔
    //       (3 < 2) == (2 < 1)
    //     ⇔
    //       0 == 0
    //}}}

    i = 3;
    j = 4;
    k = 5;
    printf("%d\n", i % j + i < k);
    //     0{{{
    //
    //       ((i % j) + i) < k
    //     ⇔
    //       ((3 % 4) + 3) < 5
    //     ⇔
    //       (3 + 3) < 5
    //     ⇔
    //       6 < 5
    //}}}
}
