// Purpose: The following `if` statement is unnecessarily complicated.  Simplify it as much as possible.
// Hint: The entire statement can be replaced by a single assignment.
// Reference: page 94 (paper) / 119 (ebook)

#include <stdio.h>
#include <stdbool.h>

    int
main(void)
{
    int age;
    bool teenager;
    // Complicated Code:
    //
    //     if (age >= 13)
    //         if (age <= 19)
    //             teenager = true;
    //         else
    //             teenager = false;
    //     else if (age < 13)
    //         teenager = false;

    // Simplified Code:
    //
    //     teenager = age >= 13 && age <= 19;

    // Tests:
    age = 10;
    teenager = age >= 13 && age <= 19;
    printf("%d\n", teenager);
    //     0

    age = 15;
    teenager = age >= 13 && age <= 19;
    printf("%d\n", teenager);
    //     1

    return 0;
}
