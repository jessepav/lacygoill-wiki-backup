// Purpose: compute output of given `for` statement
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, counter = 0;

    for (i = 10; i >= 1; i /= 2)
    {
        printf("%d ", i++);

        // This `counter` code is not in the original exercise.
        // We add it just to prevent the loop from never ending, killing our CPU
        // in the process.
        ++counter;
        if (counter == 99)
        {
            break;
        }
    }
    //     10 5 3 2 1 1 1 ...
    //                    ^^^
    //
    // Without the  `break` we've purposefully  added, the loop would  never end
    // because the `i++` incrementation prevents `i` from ever reaching 0.  When
    // it reaches  1 after `i /= 2`, it's  incremented back to 2,  and the cycle
    // continues.

    return 0;
}
