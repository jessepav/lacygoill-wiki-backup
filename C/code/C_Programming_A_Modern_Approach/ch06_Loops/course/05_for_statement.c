// Purpose: study how the `for` statement works
// GCC Options: -Wno-shadow
// Reference: page 105 (paper) / 130 (ebook)

#include <stdio.h>

    int
main(void)
{
// Syntax of a `for` statement:{{{
//
//     for (expr1; expr2; expr3) statement;
//          │      │      │
//          │      │      └ expected to have a side-effect making the test fail at some point
//          │      └ test which needs to succeed for next iteration to run
//          └ initialization
//}}}
//   This is often equivalent to this `while` statement:{{{
//
//     expr1;
//     while (expr2)
//     {
//         statement;
//         expr3;
//     }
//
// But not  always.  For  example, suppose `statement`  is a  compound statement
// containing  a `continue`  in  a  nested `if`.   Whenever  `continue` is  run,
// `expr3` will be skipped  in the `while` loop; that would  never happen in the
// `for` loop.
//
// IOW, you have the guarantee that  `expr3` will always be evaluated after each
// iteration in a `for` loop; but you have no such guarantee in a `while` loop.
//}}}

    int i, sum, N;

    for (i = 10; i > 0; i--)
        printf("T minus %d and counting\n", i);

    printf("---\n");


    // `expr1` can be omitted (by moving the assignment before)
    i = 10;
    for (; i > 0; i--)
    //   ^
    // but  you still  need the  separating semicolon,  so that  `expr2` is  not
    // wrongly parsed as `expr1`
        printf("T minus %d and counting\n", i);

    printf("---\n");


    // `expr3` can be omitted too.
    // In which case, the loop body  is responsible for making sure `expr2` gets
    // false at some point.
    for (i = 10; i > 0;)
        printf("T minus %d and counting\n", i--);
        //                                   ^^
        // To compensate for omitting `expr3`, we decrement `i` in the loop body.

    printf("---\n");


    // Even `expr2` can be omitted.
    // In which case, it  defaults to an implicit true value,  and the loop body
    // is responsible  for breaking the  loop at some  point.  In fact,  *all* 3
    // expressions can be omitted simultaneously.
    i = 10;
    for (;;)
    // ----^
    // equivalent to `while (1)`
    {
        printf("T minus %d and counting\n", i--);
        if (i <= 0)
            break;
    }

    printf("---\n");


    // In C99, `expr1` can be replaced by a declaration.
    i = 10;
    for (int i = 10; i > 0; i--)
    //       ^
    // This `i`  variable is only  **visible** inside  the loop body,  i.e. it's
    // local to this  `for` block.  It **shadows** the `i`  variable declared at
    // the start of the function.
        printf("T minus %d and counting\n", i);

    printf("i = %d\n", i);
    //     i = 10
    //         ^^
    // The value  of the  function-local `i`  did not  change, because  the loop
    // decremented the block-local `i`.

    printf("---\n");


    // You can *assign* several variables, using the comma operator, which has these properties:{{{
    //
    //    - it has the lowest precedence of all operators (so there should  be
    //      no need to put parentheses  around the operands no matter which
    //      operators they contain)
    //
    //    - it is left-associative
    //    - it evaluates its left operand *before* its right one
    //
    //    - it yields the value of its right operand (the left one is expected
    //      to have a side effect, because its value is always discarded)
    //
    //    - it can be chained multiple times to evaluate more than
    //      2 expressions
    //}}}
    // More generally, wherever you need to evaluate several expressions but the
    // syntax only  allows 1, you  can use  the **comma operator** to  make them
    // form a  single expression.  In  that regard,  the comma operator  is very
    // similar to the compound statement.
    N = 5;
    //   comma expression
    //   v------------v
    for (sum = 0, i = 1; i <= N; i++)
    //          ^
    //   comma operator
        sum += i;
    printf("%d\n", sum);
    //     15

    printf("---\n");


    // You can also  *declare* several variables in place  of `expr1`.  Provided
    // that they all have the same type, and only in C99.
    for (int i = 1, j = 3; i < j; i++)
    //   ^--------------^
        printf("%d\n", i);
    //     1
    //     2


    return 0;
}
