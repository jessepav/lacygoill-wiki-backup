// Purpose: Read an integer entered by the user and display it in octal:{{{
//
//     Enter a number between 0 and 32767: <1953>
//     In octal, your number is: <03641>
//
// The output  should be displayed using  five digits, even if  fewer digits are
// sufficient.
//
// Hint: To convert the number to octal, first  divide it by 8; the remainder is
// the  last digit  of the  octal number  (1, in  this case).   Then divide  the
// original number  by 8 and  repeat the process  to arrive at  the next-to-last
// digit.
// `printf()`  is  capable  of  displaying  numbers in  base  8  (via  the  `%o`
// conversion specification), as we'll see in  Chapter 7, so there's actually an
// easier way to write this program.
//}}}
// Reference: page 71 (paper) / 96 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, digit1, digit2, digit3, digit4, digit5;

    printf("Enter a number between 0 and 32767: ");
    scanf("%5d", &n);

    digit5 = n % 8;
    n /= 8;

    digit4 = n % 8;
    n /= 8;

    digit3 = n % 8;
    n /= 8;

    digit2 = n % 8;
    n /= 8;

    digit1 = n % 8;

    printf("In octal, your number is: %d%d%d%d%d\n", digit1, digit2, digit3, digit4, digit5);
    // Alternative:
    //
    //                                                v
    //     printf("In octal, your number is: %05o\n", n);
    //                                       ^--^

    return 0;
}
