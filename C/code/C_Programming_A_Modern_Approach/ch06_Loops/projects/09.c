// Purpose: Modify the  program from Project 8  in Chapter 2 so  that instead of
// asking for 3  monthly payments, it asks for an  arbitrary number of payments,
// and then displays the balance remaining after each of these payments.

// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    // New: `i` and `n` are 2 new variables (not in project 8 chapter 2)
    int i, n;
    float loan, rate, payment;

    printf("Enter amount of loan: ");
    scanf("%f", &loan);

    printf("Enter interest rate: ");
    scanf("%f", &rate);

    printf("Enter monthly payment: ");
    scanf("%f", &payment);

    // New: prompt user for number of payments
    printf("Enter number of payments: ");
    scanf("%d", &n);

    rate = rate / 12 / 100;
    ++rate;

    // New: iterate to print `n` balances
    for (i = 1; i <= n; i++)
    {
        loan = loan * rate - payment;
        printf("Balance remaining after payment %d: $%.2f\n", i, loan);
    }

    return 0;
}
