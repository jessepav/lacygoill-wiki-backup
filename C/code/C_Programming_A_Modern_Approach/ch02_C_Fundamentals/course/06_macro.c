// Purpose: define macro
// Reference: page 24 (paper) / 49 (ebook)

// We can use a macro definition to name a constant:{{{
//
//     #define INCHES_PER_POUND = 166
//
// When the  code is  compiled, the preprocessor  replaces each  macro reference
// with  the value  it represents.   For  example, with  the previous  `#define`
// directive, the preprocessor will automatically replace this statement:
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
// Notice that the name of the macro only uses upper-case letters.
// This is a well-established convention, which you should follow.
//}}}
// The value of a macro can be an expression:{{{
//
//     #define RECIPROCAL_OF_PI (1.0f / 3.14159f)
//}}}

#include <stdio.h>

#define RECIPROCAL_OF_PI (1.0f / 3.14159f)

    int
main(void)
{
    printf("%f", RECIPROCAL_OF_PI);
}
