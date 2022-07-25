// Purpose: study how the `do` statement works
// Reference: page 103 (paper) / 128 (ebook)

#include <stdio.h>

    int
main(void)
{
// Syntax of a `do` statement:
//
//     do statement while (expr);

    int i;

    i = 10;
    // `do` is very similar to `while`.{{{
    //
    // The only difference is that `do` tests its controlling expression *after*
    // each execution of its body; `while` tests it before.
    //
    // This implies that **its body is always executed at least once**.
    // In contrast, the body of a `while` loop might never be executed.
    //}}}
    do
    // always put  braces around the  body, so that  a careless reader  does not
    // mistake the `while` word for the start of a `while` statement (instead of
    // the end of a `do` one)
    {
        printf("T minus %d and counting\n", i);
        --i;
    } while (i > 0);

    return 0;
}
