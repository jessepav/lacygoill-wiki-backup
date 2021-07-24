// Purpose: showing how to declare a variable and assign it a value
// Input: none
// Output: none
// Usage: `variables`
// Reproduction: `$ gcc variables.c -o build/variables -Wall && ./build/variables`
// Reference: page 17

# include <stdio.h>

int main(void) {
    // int height;
    float profit;
    // height = 123;
    profit = 12.3;
    // printf("height is: %d\n", height);
    printf("profit is: %.6f\n", profit);
    return 0;
}

