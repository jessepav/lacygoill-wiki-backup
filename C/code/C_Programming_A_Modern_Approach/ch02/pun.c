// Purpose: showing how to write a simple program
// Input: none
// Output:
// To C, or not to C: that is the question.
// Brevity is the soul of wit.
// --Shakespeare
// Usage: `pun`
// Reproduction: `$ gcc pun.c -o build/pun -Wall && ./build/pun`
// Reference: page 9

// directive to include C's standard I/O library.
#include <stdio.h>
//       ├───────┘
//       └  header

//┌  the main function returns an integer value
//│      ┌ and it has no arguments
//│      │
int main(void) {
    printf("To C, or not to C: that is the question.\n");
    printf("Brevity is the soul of wit.\n  --Shakespeare\n");
    // returns 0 as a status code
    return 0;
}

