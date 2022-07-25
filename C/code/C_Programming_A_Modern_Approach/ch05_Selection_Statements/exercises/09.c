// Purpose: Are the following `if` statements equivalent?  If not, why not?
// Reference: page 95 (paper) / 120 (ebook)

#include <stdio.h>

    int
main(void)
{
    int score;

    if (score >= 90)
        printf("A");
    else if (score >= 80)
        printf("B");
    else if (score >= 70)
        printf("C");
    else if (score >= 60)
        printf("D");
    else
        printf("F");

    if (score < 60)
        printf("F");
    else if (score < 70)
        printf("D");
    else if (score < 80)
        printf("C");
    else if (score < 90)
        printf("B");
    else
        printf("A");

    // A: Yes, they are equivalent.
    // They print the same grade no matter the score.

    return 0;
}
