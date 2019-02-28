/* directive to include C's standard I/O library. */
#include <stdio.h>
/*       ├───────┘ */
/*       └  header */

/*┌  the main function returns an integer value */
/*│      ┌ the main function has no arguments */
/*│      │ */
int main(void) {
    printf("To C, or not to C: that is the question.\n");
    /* returns 0 as a status code */
    return 0;
}
