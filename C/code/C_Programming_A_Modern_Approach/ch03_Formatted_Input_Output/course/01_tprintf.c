// Purpose: print `int` and `float` values in various formats
// Reference: page 40 (paper) / 65 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i;
    float x;

    i = 40;
    x = 839.21f;

    // In the general case, a conversion specification has the form `%m.pX`.{{{
    //
    // Where `m` and `p` are integer constants, and `X` a letter.
    //
    // Examples:
    //
    //     %10.2f
    //      ^^ ^^
    //      m  pX
    //
    //
    //        X
    //        v
    //     %10f
    //      ^^
    //      m
    //
    //
    //        X
    //        v
    //     %.2f
    //       ^
    //       p
    //
    // In the second example,  notice that when `p` is omitted,  the dot is also
    // dropped.
    //}}}
    //   `m` is called the "minimum field width".{{{
    //
    // It specifies the minimum number of characters to print.
    // If the value to be printed  requires fewer than `m` characters, a padding
    // of spaces is prepended and the value is right-justified within the field.
    //}}}
    //   `p` is called the "precision".{{{
    //
    // Its meaning depends on the choice of `X`.
    // It can result in a truncation, or in a padding.
    //}}}
    // Notice that *ordinary* characters in the format strings are simply copied to the output lines. {{{
    //
    //             v  v   v    v     v
    //     printf("|%d|%5d|%-5d|%5.3d|\n", i, i, i, i);
    //     |40|   40|40   |  040|
    //     ^  ^     ^     ^     ^
    //}}}
    printf("|%d|%5d|%-5d|\n", i, i, i);
    //     |40|   40|40   |


    // `%g` behaves like `%e` for big values
    x = 1234567.89f;
    printf("|%g|\n", x);
    //     |1.23457e+06|

    // and like `%f` for small ones
    x = 123.456f;
    printf("|%g|\n", x);
    //     |123.456|


    // Note  that the  precision is  not  interpreted in  the same  way for  all
    // conversion specifications.
    // For `%g`, the precision controls the number of significant digits.{{{
    //
    // So far, it's the only noticeable difference with Vim:
    //
    //     :echo printf('%.3g', 12345678.91)
    //     |1.235e7|
    //        ^^^
    // In Vim,  the precision of  `%g` controls the  number of digits  after the
    // decimal point, just like the precision of `%e` and `%f`.
    //}}}
    x = 1234567.89f;
    printf("|%.3g|\n", x);
    //     |1.23e+06|
    //      ^ ^^

    // For `%f` (and `%e`) it controls the number of digits after the decimal point:
    x = 123.456789f;
    printf("|%.4f|\n", x);
    //     |123.4568|
    //          ^--^

    // And for `%d`, it controls the  minimum number of digits, adding a padding
    // of leading 0s if necessary:
    printf("|%5.3d|\n", i);
    //        v
    //     |  040|
    //        ^^^
}
