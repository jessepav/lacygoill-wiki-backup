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

