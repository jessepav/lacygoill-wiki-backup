// Purpose: Rearrange the `square3.c` program so that the `for` loop initializes
// `i`,  tests  `i`,  and  increments   `i`.   Don't  rewrite  the  program;  in
// particular, don't use any multiplications.

// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, odd;

    printf("This program prints a table of squares.\n");
    printf("Enter number of entries in table: ");
    scanf("%d", &n);

    odd = 3;
    for (int i = 1, square = 1; i <= n; i++, odd += 2)
    //       ^---^              ^----^  ^^^
    {
        printf("%10d%10d\n", i, square);
        square += odd;
    }
    return 0;
}
