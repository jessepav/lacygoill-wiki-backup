// Purpose: fix a given broken program fragment
// Reference: page 122 (paper) / 147 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n = 8;

    // Broken program fragment:
    //
    //                    the null statement
    //                    v
    //     if (n % 2 == 0);
    //         printf("n is is even\n");
    //
    // The code is broken because the indentation makes it look like the call to
    // `printf()` is guarded by the `if`  statement; but it's not because of the
    // previous null statement which terminated `if` prematurely.

    // We can fix the error simply by removing the null statement:
    if (n % 2 == 0)
        printf("n is is even\n");

    return 0;
}
