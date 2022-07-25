// Purpose: Find the largest in a series of numbers entered by the user.{{{
// The numbers should be input one by one.
// Display the result when 0 or a negative number is input.
//
//     Enter a number: <60>
//     Enter a number: <38.3>
//     Enter a number: <4.89>
//     Enter a number: <100.62>
//     Enter a number: <75.2295>
//     Enter a number: <0>
//
//     The largest number entered was 100.62
//
// Notice that the numbers aren't necessarily integers.
//}}}
// GCC Options: -Wno-float-equal
// Reference: page 122 (paper) / 147 (ebook)

#include <stdio.h>

    int
main(void)
{
    float f, largest;
    largest = 0.0f;

    do
    {
        printf("Enter a number: ");
        scanf("%f", &f);
        if (f > largest)
            largest = f;
    } while (f != 0);

    printf("\nThe largest number entered was %.2f\n", largest);

    return 0;
}
