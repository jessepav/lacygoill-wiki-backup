// Purpose: show how to replace a `continue` statement by an equivalent `goto` statement
// Reference: page 121 (paper) / 146 (ebook)

#include <stdio.h>

    int
main(void)
{
    // Let's write an example of a loop with a `continue` statement.
    // This one prints all the odd integers below 10:
    for (int i = 0; i < 10; i++)
    {
        if (i % 2 == 0)
            continue;
            // -----^
        printf("%d\n", i);
    }
    //     1 3 5 7 9

    printf("\n");

    // Now, let's re-write it replacing the `continue` statement with a `goto` one:
    for (int i = 0; i < 10; i++)
    {
        if (i % 2 == 0)
            goto end_of_body;
            // -------------^
        printf("%d\n", i);
        end_of_body: ;
        //           ^
        // necessary null statement, because a  label must always be followed by
        // a statement
    }
    //     1 3 5 7 9

    return 0;
}
