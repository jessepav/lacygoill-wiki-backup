// Purpose: condense the dweight.c program by:{{{
//
//    1. replacing the assignments to `height`, `length`, and `width` with
//       initializers inside declarations
//    2. removing the `weight` variable; instead calculate `(volume + 165) / 166`
//       within the last `printf()`
//}}}
// Reference: page 33 (paper) / 58 (ebook)

#include <stdio.h>

    int
main(void)
{
    // Notice how you can put line breaks inside a statement. {{{
    //
    // It can be useful to vertically align some identifiers; here, variables in
    // an assignment.  This is possible (without continuation symbols) thanks to
    // the semicolon which clearly indicates where the statement ends.
    //}}}
    int length = 12,
        width = 10,
        height = 8;

    int volume = length * width * height;

    printf("Dimensions: %dx%dx%d\n", length, width, height);
    printf("Volume (cubic inches): %d\n", volume);
    printf("Dimensional weight (pounds): %d\n", (volume + (166 - 1)) / 166);

    return 0;
}
