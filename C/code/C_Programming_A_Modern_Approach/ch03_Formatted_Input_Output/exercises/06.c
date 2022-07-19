// Purpose: Modify  `addfrac.c` so that the  user is allowed to  enter fractions
// that contain spaces before and after each `/` character.
// Reference: page 49 (paper) / 74 (ebook)

#include <stdio.h>

    int
main(void)
{
    int num1, denom1, num2, denom2, result_num, result_denom;

    printf("Enter first fraction: ");
    scanf("%d /%d", &num1, &denom1);
    //       ^
    // We only need  to add this space to account  for possible input whitespace
    // before an input slash.
    printf("Enter second fraction: ");
    scanf("%d /%d", &num2, &denom2);
    //       ^
    // Same thing here.

    result_num = num1 * denom2 + num2 * denom1;
    result_denom = denom1 * denom2;
    printf("The sum is %d/%d\n", result_num, result_denom);
}
