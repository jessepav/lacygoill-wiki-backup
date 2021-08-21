// Purpose: print `int` and `float` values in various formats
// Reference: page 40 (paper) / 65 (ebook)

#include <stdio.h>

int main(void)
{
    int i;
    float x;

    i = 40;
    x = 839.21f;

    // These statements will print:
    //
    //     |40|   40|40   |  040|
    //     |   839.210| 8.392e+02|839.21    |
    // Notice that *ordinary* characters in the format strings are simply copied to the output lines. {{{
    //
    //             v  v   v    v     v
    //     printf("|%d|%5d|%-5d|%5.3d|\n", i, i, i, i);
    //     |40|   40|40   |  040|
    //     ^  ^     ^     ^     ^
    //}}}
    // In the general case, a conversion specification has the form `%m.pX`.{{{
    //
    // Where `m` and `p` are integer constants, and `X` a letter.
    //
    // As examples:
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
    // In the  second example, notice  that when `p`  is omitted, the  period is
    // also dropped.
    //}}}
    // `m` is called the "minimum field width".{{{
    //
    // It specifies the minimum number of characters to print.
    // If the value to be printed  requires fewer than `m` characters, a padding
    // of spaces is prepended and the value is right-justified within the field.
    //}}}
    // `p` is called the "precision".{{{
    //
    // Its meaning depends on the choice of `X`.
    // It can result in a truncation, or in a padding.
    //}}}
    printf("|%d|%5d|%-5d|%5.3d|\n", i, i, i, i);
    printf("|%10.3f|%10.3e|%-10g|\n", x, x, x);

    return 0;
}

