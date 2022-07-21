// Purpose: Write a single expression whose value  is either `-1`, `0`, or `+1`,
// depending  on whether  `i`  is less  than,  equal to,  or  greater than  `j`,
// respectively.
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j;

    // `i < j`
    i = 12;
    j = 34;
    //             v-------------------------v
    printf("%d\n", i < j ? -1 : i == j ? 0 : 1);
    //     -1

    // `i == j`
    i = 123;
    j = 123;
    //             v-------------------------v
    printf("%d\n", i < j ? -1 : i == j ? 0 : 1);
    //     0

    // `i > j`
    i = 34;
    j = 12;
    //             v-------------------------v
    printf("%d\n", i < j ? -1 : i == j ? 0 : 1);
    //     1


    // Alternative: `(i > j) - (i < j)`
    // Here is how you could retrieve it.{{{
    //
    // We're  looking  for  a  logical expression  which  encodes  the  relative
    // position of `i` compared to `j`.  The simplest expression we can think of
    // is `i > j`.  Let's check  out its value in the three  cases which we care
    // about:
    //
    //     ┌────────┬────────────────┐
    //     │ case   │ value of i > j │
    //     ├────────┼────────────────┤
    //     │ i > j  │ 1              │
    //     ├────────┼────────────────┤
    //     │ i == j │ 0              │
    //     ├────────┼────────────────┤
    //     │ i < j  │ 0              │
    //     └────────┴────────────────┘
    //
    // The values are all good, except the last one.
    // We need to subtract something to make it `-1`.
    // But whatever we subtract, it must not alter the first two values.
    // IOW, we need something with these values:
    //
    //     ┌────────┬────────────┐
    //     │ case   │ value of ? │
    //     ├────────┼────────────┤
    //     │ i > j  │ 0          │
    //     ├────────┼────────────┤
    //     │ i == j │ 0          │
    //     ├────────┼────────────┤
    //     │ i < j  │ 1          │
    //     └────────┴────────────┘
    //
    // `i < j` produces exactly those values, so that's what we need to subtract:
    //
    //     (i > j) - (i < j)
    //             ^-------^
    //}}}
}
