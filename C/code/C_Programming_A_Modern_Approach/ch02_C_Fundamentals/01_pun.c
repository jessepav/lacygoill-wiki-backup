// Purpose: write a simple program
// Reference: page 9 (paper) / 34 (ebook)

// Directive telling the preprocessor to include information about C's standard I/O library.
#include <stdio.h>
//       ├───────┘
//       └  header file

//┌ the main function returns an integer value
//│      ┌ and it has no arguments
//│      │
int main(void)
{
// Where you put the brace which starts a function's body is a matter of style.{{{
//
// However, it's better  to put it on a  line of its own rather  than joining it
// with the function's header.  Compare:
//
//     int main(
//         int parameterOne,
//         int parameterTwo) {
//         int localOne,
//         int localTwo
//     }
//
// Versus:
//
//     int main(
//         int parameterOne,
//         int parameterTwo)
//     {
//         int localOne,
//         int localTwo
//     }
//
// The second is much more readable.
// See: https://softwareengineering.stackexchange.com/a/2786
//
// This style is also followed by the linux kernel:
// https://www.kernel.org/doc/html/latest/process/coding-style.html?highlight=style#placing-braces-and-spaces
//}}}
    printf("To C, or not to C: that is the question.\n");
    printf("Brevity is the soul of wit.\n  --Shakespeare\n");
    // returns 0 as a status code
    return 0;
}
