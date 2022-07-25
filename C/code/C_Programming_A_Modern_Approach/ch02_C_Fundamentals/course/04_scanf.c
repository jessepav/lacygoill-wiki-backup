// Purpose: read input from the user
// Reference: page 22 (paper) / 47 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i;
    float x;

    // Notice that we *need* an extra `printf()`.{{{
    //
    // We can't merge it with `scanf()`.
    // IOW, `scanf()` can only  do 1 thing: ask for the user  input and write it
    // in  a  variable.   It can  *not*  also  print  a  prompt.  That's  a  big
    // difference with `input()` in VimL.
    //}}}
    printf("choose an integer: ");
    // `"%d"` tells `scanf()` to read input that represents an integer.
    // `&i` tells `scanf()` to write that integer input in the variable `i`.
    scanf("%d", &i);

    // No need to start with a newline, because after pressing Enter to validate
    // the previous input, the cursor has automatically moved to the next line.
    printf("choose a float: ");
    // `"%f"` tells `scanf()` to look for a floating-point number input.
    scanf("%f", &x);

    printf("you chose the integer %d and the float %f\n", i, x);

    return 0;
}
