// Purpose: define macro
// Reference: page 24 (paper) / 49 (ebook)

// We can use a macro definition to name a constant:{{{
//
//     #define INCHES_PER_POUND = 166
//
// When the  code is  compiled, the  preprocessor replaces  each macro  with the
// value it represents.  For example, with the previous `#define` directive, the
// preprocessor will automatically replace this statement:
//
//     weight = (volume + INCHES_PER_POUND - 1) / INCHES_PER_POUND;
//
// With this one:
//
//     weight = (volume + 166 - 1) / 166;
//
// That's the code which will actually be compiled.
//
// ---
//
// Notice that the name of the macro uses only upper-case letters.
// This is a well-established convention, which you should follow.
//}}}
// The value of a macro can be an expression:{{{
//
//     #define RECIPROCAL_OF_PI (1.0f / 3.14159f)
//}}}
//   But if it contains an operator, you want to wrap it inside parentheses:{{{
//
// Otherwise, you have no guarantee that the compiler will treat it as a whole.
// That's because, after  the replacement, the rules of  operator precedence and
// associativity might be applied in ways you didn't expect.
//
// Consider this code:
//
//                    no parens around the expression
//                    v         v
//     #define TWO_PI 2 * 3.14159
//     ...
//     conversion_factor = 360 / TWO_PI;
//
// During preprocessing, the last statement is replaced with:
//
//     conversion_factor = 360 / 2 * 3.14159
//
// Which is equivalent to:
//
//     conversion_factor = (360 / 2) * 3.14159
//
// That's not what you wanted.  You wanted this:
//
//     conversion_factor = 360 / (2 * 3.14159)
//}}}

#include <stdio.h>
#define RECIPROCAL_OF_PI (1.0f / 3.14159f)

int main(void)
{
    printf("%f", RECIPROCAL_OF_PI);
}
