// Purpose: study the `if` statement
// Reference: page 76 (paper) / 101 (ebook)

#include <stdio.h>

    int
main(void)
{
// Syntax of an `if` statement:{{{
//
//                        not part of `statement`, but needed to indicate where `if` ends
//                        v
//     if (expr) statement;
//        ^    ^
//        part of the if statement (not part of `expr`)
//}}}

    int i, j, k, n, max;

    i = 1;
    n = 2;

    // If we want an `if` statement to  control 2 statements or more, we need to
    // group them via  a compound statement, which the compiler  will treat as a
    // single statement.
    if (0 < i && i < n)
 // v
    {
        printf("%d is between 0 and %d\n", i, n);
        printf("another statement guarded by the ‘if’\n");
        //     1 is between 0 and 2
        //     another statement guarded by the ‘if’
    }
 // ^
    // Notice that inside the compound statement we still need to terminate each
    // statement  with a  semicolon.   But we  don't  need to  do  that for  the
    // compound statement itself.


    // Optionally an `if` statement can include an `else` clause:{{{
    //
    //     if (expr) statement else statement;
    //                         ^------------^
    //}}}


    // An `if` statement can be nested inside another `if` statement.
    // Aligning an `else` with its matching `if` is not required.{{{
    //
    // But makes the code  easier to read, because the nesting  is easier to see
    // that way.
    //}}}
    // We don't need a compound statement for the nested `if`s.{{{
    //
    // That's because  splitting a statement  on multiple lines  doesn't require
    // that  we  put braces  around.   Those  are  only necessary  for  multiple
    // *statements*; not for multiple *lines*.
    //}}}
    j = 2, k = 3;
    if (i > j)
        if (i > k)
            max = i;
        else
            max = k;
    else
        if (j > k)
            max = j;
        else
            max = k;
    printf("%d\n", max);
    //     3


    // When an `else` clause includes a nested `if`, the two are commonly written on the same line.{{{
    //
    // And the indentation level of the rest of the `else` clause is decremented
    // by 1 to align the statements of all the clauses.
    //
    // Because it's easier to read this:
    //
    //     if (cond)
    //         statement;
    //     else if (cond)
    //         statement;
    //     else if (cond)
    //         statement;
    //     else if (cond)
    //         statement;
    //
    // Than this:
    //
    //     if (cond)
    //         statement;
    //     else
    //         if (cond)
    //             statement;
    //         else
    //             if (cond)
    //                 statement;
    //             else
    //                 if (cond)
    //                     statement;
    //
    // In particular, the second form is  too hard to read/write when the number
    // of tests increases, and the indentation level moves the code too far away
    // from the start of the lines.
    //}}}
    if (n < 0)
        printf("n i sless than 0\n");
    else if (n == 0)
        printf("n is equal to 0\n");
    else
        printf("n is greater than 0\n");
    //     n is greater than 0

    return 0;
}
