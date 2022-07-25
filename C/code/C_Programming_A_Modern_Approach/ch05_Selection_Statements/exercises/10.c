// Purpose: What output does the following program fragment produce?
// Assume that `i` is an integer variable.
// GCC Options: -Wno-switch-default -Wno-implicit-fallthrough
// Reference: page 95 (paper) / 120 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i = 1;
    switch (i % 3)
    {
        case 0: printf("zero");
        case 1: printf("one");
        case 2: printf("two");
    }
    //     onetwo{{{
    //
    // `i % 3` evaluates  to 1, so  control jumps to  the label `1`,  and prints
    // "one".  But  there is  no `break` statement  right afterward,  so control
    // falls through to the first statement of the next case which prints "two".
    //}}}

    return 0;
}
