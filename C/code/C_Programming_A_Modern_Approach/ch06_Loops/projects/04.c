// Purpose: Add a loop to the `broker.c` program (in chapter 5) so that the user can enter more than one trade.{{{
//
// Calculate the commission for each trade.
// Terminate when the user enters 0 as the trade value:
//
//     Enter value of trade: 30000
//     Commission: $166.00
//
//     Enter value of trade: 20000
//     Commission: $144.00
//
//     Enter value of trade: 0
//}}}
// GCC Options: -Wno-float-equal
// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    float commission, trade;

    // You could also test `trade != 0.0f` and get rid of the `break`.{{{
    //
    // But then, you would need to write a duplicate `printf()` and `scanf()` *before* the loop:
    //
    //     printf("Enter value of trade: ");
    //     scanf("%f", &trade);
    //
    // If you don't want code duplication, then `break` seems necessary.
    // And if you  use `break`, then the controlling  expression doesn't matter;
    // the most efficient to test is a simple `1`.
    //}}}
    while (1)
    {
        printf("Enter value of trade: ");
        scanf("%f", &trade);
        if (trade == 0)
            break;

        if (trade < 2500.00f)
            commission = 30.00f + 1.7f * trade / 100;
        else if (trade < 6250.00f)
            commission = 56.00f + 0.66f * trade / 100;
        else if (trade < 20000.00f)
            commission = 76.00f + 0.34f * trade / 100;
        else if (trade < 50000.00f)
            commission = 100.00f + 0.22f * trade / 100;
        else if (trade < 500000.00f)
            commission = 155.00f + 0.11f * trade / 100;
        else
            commission = 255.00f + 0.09f * trade / 100;

        if (commission < 39.00f)
            commission = 39.00f;

        printf("Commission: $%.2f\n\n", commission);
    }

    return 0;
}
