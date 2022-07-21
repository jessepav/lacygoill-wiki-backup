// Purpose: Only one of the expressions `++i` and `i++` is exactly the same as `(i += 1);`.
// Which is it?  Justify your answer.
// Reference: page 70 (paper) / 95 (ebook)

#include <stdio.h>

    int
main(void)
{
    // A: Only `++i` is equivalent to `(i += 1);`.
    //
    // `(i += 1)` increments `i`, and evaluates to the new incremented value.
    //
    // Both `++i` and  `i++` increment `i`, but only `++i`  evaluates to the new
    // incremented  value.  `i++`  evaluates  to  the  old  value,  because  the
    // incrementation is  performed *after*  the expression  is read  (hence why
    // `++` is written after the variable name).

    int i;
    i = 123;
    printf("%d\n", i += 1);
    //     124

    i = 123;
    printf("%d\n", ++i);
    //     124

    i = 123;
    printf("%d\n", i++);
    //     123
}
