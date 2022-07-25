// Purpose: print escape sequences
// Reference: page 41 (paper) / 66 (ebook)

#include <stdio.h>

    int
main(void)
{
    // `a` is not printed because `\b` moves the cursor back 1 position
    printf("a\bb\n");
    //     b

    // `\t` moves the cursor to the next tab stop
    printf("a\tb\n");
    //     a      b

    // an embedded double quote must be escaped
    //       v
    printf("a\"b\n");
    //     a"b

    // an embedded percent must be doubled
    printf("a%%b\n");
    //     a%b

    return 0;
}
