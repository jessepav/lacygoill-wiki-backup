// Purpose: read input from the user
// Reference: page 22 (paper) / 47 (ebook)

// I have an error at compile time!{{{
//
//     ignoring return value of ‘scanf’, declared with attribute warn_unused_result
//
// Problem: The compiler complains that you don't check whether `scanf()` succeeded.
// Solution: Return earlier if `scanf()` is not 1:
//
//     ✘
//     scanf("%d", &i);
//
//     ✔
//     if (scanf("%d", &i) != 1) {
//         return 1;
//     }
//
// See: https://stackoverflow.com/a/7271983
//}}}

#include <stdio.h>

int main(void)
{
    int i;
    float x;

    printf("choose an integer: ");
    // "%d" tells `scanf()` to read input that represents an integer.
    // `&i` tells `scanf()` to write it in the variable `i`.
    scanf("%d", &i);

    // No need to start with a newline, because after pressing Enter to validate
    // the previous input, the cursor has automatically moved to the next line.
    printf("choose a float: ");
    // "%f" tells `scanf()` to look for an input value in `float` format.
    scanf("%f", &x);

    printf("you chose the integer %d and the float %f\n", i, x);

    return 0;
}
