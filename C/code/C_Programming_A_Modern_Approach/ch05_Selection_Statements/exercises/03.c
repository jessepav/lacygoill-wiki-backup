// Purpose: compute various logical expressions using logical operators with short-circuit behaviors
// GCC Options: -Wno-parentheses
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;

    i = 3;
    j = 4;
    k = 5;
    printf("%d ", i < j || ++j < k);
    printf("%d %d %d\n", i, j, k);
    //      1 3 4 5{{{
    //
    //       (i < j) || ((++j) < k)
    //     ⇔
    //       (3 < 4) || ((++j) < k)
    //     ⇔
    //       (3 < 4)
    //}}}

    i = 7;
    j = 8;
    k = 9;
    printf("%d ", i - 7 && j++ < k);
    printf("%d %d %d\n", i, j, k);
    //     0 7 8 9{{{
    //
    //       (i - 7) && ((j++) < k)
    //     ⇔
    //       (7 - 7) && ((j++) < k)
    //     ⇔
    //       0
    //}}}

    i = 7;
    j = 8;
    k = 9;
    printf("%d ", (i = j) || (j = k));
    printf("%d %d %d\n", i, j, k);
    //     1 8 8 9{{{
    //
    //       (i = j) || (j = k)
    //     ⇔
    //       (i = 8) || (j = k)
    //     ⇔
    //       i = 8
    //}}}

    i = 1;
    j = 1;
    k = 1;
    printf("%d ", ++i || ++j && ++k);
    printf("%d %d %d\n", i, j, k);
    //     1 2 1 1{{{
    //
    //       (++i) || (++j) && (++k)
    //     ⇔
    //       (i = 2) || (++j) && (++k)
    //     ⇔
    //       i = 2
    //}}}

    return 0;
}
