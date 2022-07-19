// Purpose: Query the user for a telephone number in this form:{{{
//
//     (xxx) xxx-xxxx
//
// Then, make it display the number in the form:
//
//     xxx.xxx.xxxx
//}}}
// Input: Enter phone number [(xxx) xxx-xxxx]: <(404) 817-6900>
// Output: You entered 404.817.6900
// Reference: page 75 (paper) / 50 (ebook)

#include <stdio.h>

    int
main(void)
{
    int num1, num2, num3;

    printf("Enter phone number [(xxx) xxx-xxxx]: ");
    scanf("(%d) %d-%d", &num1, &num2, &num3);

    printf("You entered: %d.%d.%d\n", num1, num2, num3);
}
