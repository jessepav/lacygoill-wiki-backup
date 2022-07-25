// Purpose: study the `switch` statement
// Reference: page 86 (paper) / 111 (ebook)

#include <stdio.h>

    int
main(void)
{
// Syntax of a `switch` statement:{{{
//
//     switch (controlling-expression)
//     {
//         case label-constant-expression:
//             statement;
//             statement;
//             ...
//         case label-constant-expression:
//             statement;
//             statement;
//             ...
//         ...
//         default:
//             statement;
//             statement;
//             ...
//     }
//}}}

    int grade = 4;

    // To compare an expression against a  series of values, and act differently
    // upon each of them, we can write a cascaded `if` statement.
    // For example, suppose we want to print the English word that corresponds to a numerical grade:{{{
    //
    //     if (grade == 4)
    //         printf("Excellent");
    //     else if (grade == 3)
    //         printf("Good");
    //     else if (grade == 2)
    //         printf("Average");
    //     else if (grade == 1)
    //         printf("Poor");
    //     else if (grade == 0)
    //         printf("Failing");
    //     else
    //         printf("Illegal grade");
    //}}}

    // But  a `switch`  statement is  easier to  read, and  more efficient  (its
    // controlling  expression is  evaluated only  once).   If one  of the  case
    // labels matches `grade`, control will jump to that case label.
    switch (grade)
    {
        case 4:
            printf("Excellent");
            // `break` is necessary to prevent control from falling through to the first statement of the next `case`.{{{
            //
            // That is,  we don't want  the remaining statements in  the `case`s
            // below to be  executed.  We want control to jump  to the statement
            // after the `switch`, as soon as a `case` has been executed; not to
            // flow from one `case` into the next.
            //
            // ---
            //
            // This pitfall is  caused by the fact that a  `switch` statement is
            // nothing  more  than a  computed  jump.   The computing  algorithm
            // being:
            //
            //    - evaluate the controlling expression
            //
            //    - compare the result to each case label
            //      (which might also be an expression to evaluate; e.g. `1 + 2`)
            //
            //    - jump to the location of the first label for which a match
            //      is found
            //
            // Consequently, the case labels are matched against the controlling
            // expression only once.  Afterward, they  are ignored.  So, even if
            // `grade` did not match `3`, its statements would be still executed
            // if we forgot to put a `break` before.
            //}}}
            // Another jump statement like `return` can fulfill the same role.
            // If for some reason, you really need the next statements to be executed, write `// FALLTHROUGH`.{{{
            //
            // Because it's unusual, and someone  unfamiliar with the code might
            // be tempted to "fix" the `case` by adding a `break`.
            //
            //     case ...:
            //         printf("do something");
            //         // FALLTHROUGH
            //         ^------------^
            //     case ...:
            //}}}
            break;
        case 3:
            printf("Good");
            break;
        case 2:
            printf("Average");
            break;
        case 1:
            printf("Poor");
            break;
        case 0:
            printf("Failing");
            break;
        default:
            printf("Illegal grade");
            // not necessary but useful in case we move `default` before, or add
            // another `case` after it
            break;
    }

    // Allowed:
    // The statements inside a `case` don't need to be grouped via a compound statement.
    // The order of the `case`s can be chosen arbitrarily.{{{
    //
    // That includes the `default` one.
    // If no case label matches the controlling expression, control will jump to
    // the `default` label, wherever it might be inside the `switch`.
    //}}}
    // Several consecutive `case` labels can precede the same group of statements.{{{
    //
    //     switch (grade)
    //     {
    //         case 4:
    //         case 3:
    //         case 2:
    //         case 1:
    //             printf("Passing");
    //             break;
    //         case 0:
    //             printf("Failing");
    //             break;
    //         default:
    //             printf("Illegal grade");
    //             break;
    //     }
    //}}}
    // The `default` case can be omitted.{{{
    //
    // Unless you pass `-Wswitch-default -Werror` to `gcc(1)`.
    // If no  case label matches,  control simply  passes to the  next statement
    // after the `switch`.
    //}}}

    // Disallowed:
    // The controlling expression must be an integer.{{{
    //
    // A string or a floating-point number would cause an error:
    //
    // //  v---v
    //     float f;
    //     switch (f) default: ;
    //     error: switch quantity not an integer˜
    //
    // A character would be OK, because C treats any character as an integer.
    //}}}
    // Duplicate case labels are not allowed.{{{
    //
    //     switch (grade)
    //     {
    //         //   v
    //         case 3: ;
    //         //   v
    //         case 3: ;
    //         default: ;
    //     }
    //     error: duplicate case value˜
    //}}}
    // No variable or function call is allowed in a constant expression used in a label.{{{
    //
    // Otherwise it wouldn't be a constant.
    // These are constants:
    //
    //     5
    //     5 + 10
    //
    // This is not:
    //
    //     n + 10
    //}}}
    //   And must reduce to an integer.{{{
    //
    // Which  makes sense;  it's meant  to  be matched  against the  controlling
    // expression which itself must be an integer.
    //
    //     switch (grade)
    //     {
    //         //   v--v
    //         case 1.23: printf("Special");
    //         default: ;
    //     }
    //     error: case label does not reduce to an integer constant˜
    //}}}

    return 0;
}
