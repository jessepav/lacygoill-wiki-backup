// Purpose: Translate the `for` statement of Exercise 8 into an equivalent `while` statement.
// You'll need one statement in addition to the `while` loop itself.

// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, counter = 0;

    i = 10;
    while (i >= 1)
    {
        printf("%d ", i++);
        i /= 2;

        ++counter;
        if (counter == 99)
        {
            break;
        }
    }

    return 0;
}
