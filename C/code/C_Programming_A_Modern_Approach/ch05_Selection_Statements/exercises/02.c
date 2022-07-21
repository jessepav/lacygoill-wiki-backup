// Purpose: compute various logical expressions using logical operators
// GCC Options: -Wno-logical-not-parentheses -Wno-parentheses
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;

    i = 10;
    j = 5;
    printf("%d\n", !i < j);
    //     1{{{
    //
    //       (!i) < j
    //     ⇔
    //       (!10) < 5
    //     ⇔
    //       0 < 5
    //}}}

    i = 2;
    j = 1;
    printf("%d\n", !!i + !j);
    //     1{{{
    //
    //       (!(!i)) + (!j)
    //     ⇔
    //       (!(!2)) + (!1)
    //     ⇔
    //       (!0) + 0
    //     ⇔
    //       1 + 0
    //}}}

    i = 5;
    j = 0;
    k = -5;
    printf("%d\n", i && j || k);
    //     1{{{
    //
    //       (i && j) || k
    //     ⇔
    //       (5 && 0) || -5
    //     ⇔
    //       0 || -5
    //            ^^
    //            any non-zero value is true; including a negative one
    //}}}

    i = 1;
    j = 2;
    k = 3;
    printf("%d\n", i < j || k);
    //     1{{{
    //
    //       (i < j) || k
    //     ⇔
    //       (1 < 2) || 3
    //     ⇔
    //       1 || 3
    //}}}
}
