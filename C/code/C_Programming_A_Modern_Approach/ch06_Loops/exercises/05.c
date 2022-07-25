// Purpose: Out of these 3 loops, find the one which is not equivalent to the other two:{{{
//
//     while (i < 10) {...}
//     for (; i < 10;) {...}
//     do {...} while (i < 10)
//}}}
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    // A: It's the 3rd loop:
    //
    //     do {...} while (i < 10)
    //
    // Because  it  always  executes  its  body  at  least  once,  even  if  its
    // controlling expression (`i < 10`) is initially false.
    // In contrast,  if `i < 10` is  false, the  other loops will  never execute
    // their body (not even once).

    return 0;
}
