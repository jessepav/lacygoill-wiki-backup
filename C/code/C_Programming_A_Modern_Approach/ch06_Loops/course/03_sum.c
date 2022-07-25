// Purpose: Sum a series of integers entered by the user.
//
//     This program sums a series of integers
//     Enter integers (0 to terminate): <8 23 71 5 0>
//     The sum is: <107>

// Reference: page 102 (paper) / 127 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, sum;

    printf("This program sums a series of integers\n");
    printf("Enter integers (0 to terminate): ");

    sum = 0;
    // It's often hard to avoid repeating the same code when using `while`.
    // Here, we have to write the same call to `scanf()` twice.{{{
    //
    // Although,  I guess  we could  remove the  first call,  if we  assigned an
    // arbitrary non-zero  value to  `n` (e.g. `n = 1;`)  before the  loop.  But
    // that would force the  loop body to be run at least  once, which might not
    // always be what we want (e.g. for some unexpected input).
    //
    // Also, that  would force  us to  increment the  sum *after*  the `scanf()`
    // call, so that our arbitrary 1 is immediately reset with a number input by
    // the  user.   But  moving  the  incrementation  after  `scanf()`  is  less
    // efficient.   Indeed, we  would needlessly  sum 0  in the  last iteration.
    // Obviously,  the difference  would not  be noticeable  in this  particular
    // case, but it might be in other cases.
    //
    // In general, whatever  alters the controlling expression should  be at the
    // very end of the loop body.
    //}}}
    scanf("%d", &n);
    while (n != 0)
    {
        sum += n;
        // Remember that `scanf()` does not ask for the user input, like `input()` does in VimL.
        // Instead, it:{{{
        //
        //    - reads the input buffer
        //
        //    - only consumes what it reads; whatever is not read remains in
        //      the input buffer
        //
        //    - returns as soon  as it has read  enough characters from the
        //      input buffer to assign values to the given variable(s)
        //
        // If the  user inputs  several numbers, the  input buffer  will contain
        // them all.   Each of  them will be  read by a  `scanf()` call  in each
        // iteration of the loop.  If one of them happens to be 0, the loop will
        // exit  (leaving the  remaining numbers  in the  input buffer,  if any,
        // available to a possible future `scanf()` call after the loop).
        //}}}
        scanf("%d", &n);
    }

    printf("The sum is: %d\n", sum);
    return 0;
}
