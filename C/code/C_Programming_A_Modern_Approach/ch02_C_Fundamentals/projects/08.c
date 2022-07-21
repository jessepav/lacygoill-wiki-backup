// Purpose: compute the remaining balance on a loan after the 1st, 2nd, and 3rd monthly payments{{{
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
// interest rate, then decreased by the amount of the payment.  The monthly rate
// is given by:
//
//     monthly_rate = yearly_rate / 12
//
// ---
//
// Display each balance with 2 digits after the decimal point.
//}}}
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

    int
main(void)
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
    // We need to add 1 to the rate, because the interest is added to the current balance. {{{
    //
    // Suppose the current balance is 200, and the rate is 3%.
    //
    // After adding the interest, the new balance is:
    //
    //       200 + 3/100 * 200
    //     = 200 * (1 + 3 / 100)
    //              ^
    //
    // Notice that we add 1 to the rate.
    //
    // ---
    //
    // We  add 1  now  so that  we don't  have  to do  it  in each  of the  next
    // computations.
    //}}}
    ++rate;

    loan = loan * rate - payment;
    printf("Balance remaining after first payment: $%.2f\n", loan);

    loan = loan * rate - payment;
    printf("Balance remaining after second payment: $%.2f\n", loan);

    loan = loan * rate - payment;
    printf("Balance remaining after third payment: $%.2f\n", loan);
}
