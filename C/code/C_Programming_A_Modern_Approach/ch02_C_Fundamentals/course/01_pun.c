// Purpose: write a simple program
// Reference: page 9 (paper) / 34 (ebook)

// Directive telling the preprocessor to  include information about C's standard
// I/O library.
#include <stdio.h>
//        ^-----^
//       header file

//the main function returns an integer value
    int
// and it has no arguments
main(void)
{
    printf("To C, or not to C: that is the question.\n");
    printf("Brevity is the soul of wit.\n  --Shakespeare\n");

    // Returns 0 as a status code.
    // Mandatory in C89; optional in C99.
    return 0;
}
