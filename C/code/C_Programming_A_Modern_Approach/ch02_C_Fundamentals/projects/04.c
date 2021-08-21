// Purpose: asks the user to enter a dollars-and-cents amount, then displays the amount with 5% tax added
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

int main(void)
{
    float amount, with_tax_added;

    printf("Enter an amount: ");
    scanf("%f", &amount);
    with_tax_added = 1.05f * amount;
    printf("With tax added: $%.2f\n", with_tax_added);

    return 0;
}
