// Purpose: study assignment operators
// GCC Options: -Wno-conversion
// Reference: page 58 (paper) / 83 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, j, k;
    float f;

    // In a `v = e` assignment, if the type of the expression `e` does not match
    // the  one  of  the  variable  `v`, it's  automatically  converted  into  a
    // different value whose type matches.
    i = 72.99f; // `i` is now 72
    f = 136; // `f` is now 136.000000
    printf("i = %d, f = %f\n", i, f);
    //     i = 72, f = 136.000000


    // In many programming languages, an assignment is a *statement*.
    // In C, however, an assignment is an *expression* using the `=` operator.
    // The evaluation of this expression is the value held by the variable after
    // having been assigned.
    printf("The assignment expression \"i = 3\" evaluates to: %d\n", i = 3);
    //     The assignment expression "i = 3" evaluates to: 3
    //                                                     ^
    // This means that the `=` operator has a *side effect*.{{{
    //
    // Not only does it yield a value, it also changes the value of a variable.
    //
    // In  mathematics,  operators  don't  have side  effects;  same  thing  for
    // functions (which are  said to be "pure").  Most C  operators have no side
    // effects either.  In that regard, `=` is special.
    //}}}


    // Since `=` is an operator, several assignments can be chained together.
    // Note that `=` is right-associative, so this assignment is equivalent to:{{{
    //
    //     i = (j = (k = 0));
    //}}}
    i = j = k = 0;

    // Multiple type coercions can occur in a chained assignment.
    f = i = 33.3f;
    printf("i = %d, f = %f\n", i, f);
    //     i = 33, f = 33.000000
    //
    // `i= 33.3f` is the first assignment to be computed.
    // It coerces the float  `33.3f` into the integer `33` to  match the type of
    // `i`.  The result is `33`.
    //
    // `f = ...` is the second assignment to be computed.
    // It coerces  the integer `33`  (result of  the first assignment)  into the
    // float `33.000000` to match the type of `f`.


    // An assignment `v = e` can be written anywhere an expression with the same
    // type as `v` is allowed.
    i = 1;
    k = 1 + (j = i);
    printf("%d %d %d\n", i, j, k);
    //     1 1 2
    //
    // Although, such an "embedded assignment" can  be hard to read, and lead to
    // subtle bugs.  Avoid it.


    // The assignment operator `=` requires its left operand to be an lvalue.{{{
    //
    // Any other kind of expression on the LHS is disallowed:
    //
    //     12 = i;     // WRONG
    //     i + j = 0;  // WRONG
    //     -i = j;     // WRONG
    //
    // If you try to compile such an invalid assignment, GCC will give an error:
    //
    //     error: lvalue required as left operand of assignment
    //}}}

    return 0;
}
