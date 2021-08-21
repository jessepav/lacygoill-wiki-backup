// Purpose: calculate the remaining balance on a loan after the 1st, 2nd, and 3rd monthly payments{{{
//
// Let the user input the:
//
//    - amount of the loan
//    - yearly interest rate
//    - monthly payment
//
// ---
//
// Each month, the balance is first increased by the balance times the *monthly*
// interest rate, then decreased by the amount of the payment.
// The monthlhy rate is given by:
//
//     monthly_rate = yearly_rate / 12
//
// ---
//
// Display each balance with 2 digits after the decimal point.
//}}}
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

int main(void)
{
    float loan, rate, payment;

    printf("Enter amount of loan: ");
    scanf("%f", &loan);

    printf("Enter interest rate: ");
    scanf("%f", &rate);

    printf("Enter monthly payment: ");
    scanf("%f", &payment);

    // convert the yearly rate into a monthly one
    rate = rate / 12 / 100;
    // increment now so that we don't have to do it in each of the next computations
    ++rate;

    loan = loan * rate - payment;
        printf("Balance remaining after first payment: $%.2f\n", loan);
    loan = loan * rate - payment;
        printf("Balance remaining after second payment: $%.2f\n", loan);
    loan = loan * rate - payment;
        printf("Balance remaining after third payment: $%.2f\n", loan);

    return 0;
}
