// Purpose: Print all even squares between 1 and input number.{{{
//
// For example, if the user enters 100, the program should print the following:
//
//     4
//     16
//     36
//     64
//     100
//}}}
// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, i;

    printf("Enter a number: ");
    scanf("%d", &n);
    for (i = 2; i * i <= n; i += 2)
        printf("%d\n", i * i);

    return 0;
}
