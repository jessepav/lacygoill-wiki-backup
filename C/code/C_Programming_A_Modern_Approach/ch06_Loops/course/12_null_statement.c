// Purpose: study the `null` statement
// Reference: page 116 (paper) / 141 (ebook)

#include <stdio.h>

    int
main(void)
{
    int d, n;
    n = 123;

    // The null statement is the statement devoid of any symbol.
    // Although, like  most statement, it  still needs  to be terminated  with a
    // semicolon.
    //
    //     i = 0; ; j = 1;
    //           ^
    //           null statement


    // The null statement is primarily used to write a loop whose body is empty.
    // For example,  here is a  loop which looks for  the smallest divisor  of a
    // given number (to test whether it's prime):
    for (d = 2; d < n; d++)
    {
        if (n % d == 0)
        {
            break;
        }
    }

    // If  we move  the  `n %  d ==  0`  condition from  the  loop  body to  its
    // controlling expression, the loop body becomes empty.
    for (d = 2; d < n && n % d != 0; d++)
    //                   ^--------^
    //                   found a divisor of n
        ;


    // It's good practice to write the null statement on a line by itself.
    // If you join it with the  previous statement, the code might get confusing
    // for the reader:
    for (d = 2; d < n && n % d != 0; d++);
    //                                   ^
    // Here a careless  reader might think that  this `if` block is  part of the
    // `for` body, while in reality it's outside the loop.  Putting the previous
    // null statement on a line alone would avoid any confusion.
    if (d < n)
        printf("%d is divisible by %d\n", n, d);

    // Another reason not to join the  null statement with a previous statement,
    // is that  it can terminate a  control flow statement like  `if`, `for`, or
    // `while` too early.
    //
    //     if (d == 0);
    //                ^
    //                ✘
    //                whatever comes afterward is not guarded by this `if`
    //
    //     i = 10
    //     while (i > 0);
    //                  ^
    //                  ✘
    //                  whatever comes afterward is not in the loop body,
    //                  preventing the loop from ever ending


    // To avoid any  confusion, the null statement can be  replaced with a dummy
    // `continue` or an empty compound statement:
    //
    //     for (d = 2; d < n && n % d != 0; d++)
    //         continue;
    //         ^-------^
    //
    //     for (d = 2; d < n && n % d != 0; d++)
    //         {}
    //         ^^


    // The only (rare)  case where the null statement can't  be avoided, is when
    // you need to write a label at the end of a compound statement.
    // Because a label must  be followed by a statement; but if  it's at the end
    // of a compound  statement, then it's followed by the  closing `}` which is
    // not a statement.
    {
        goto foo;
        printf("\n");
        foo: ;
        //   ^
        // to suppress "label at end of compound statement" error
    }


    // A loop with an empty body is usually no more efficient than a loop with a
    // non-empty one;  so don't go  out of your way  to refactor your  loops and
    // make them empty.  That being said, it can be handy to read character data
    // (as we'll see in the next chapter).

    return 0;
}
