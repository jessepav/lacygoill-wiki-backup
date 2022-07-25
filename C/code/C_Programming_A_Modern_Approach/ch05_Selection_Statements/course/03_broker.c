// Purpose: Calculate a broker's commission.{{{
//
// When stocks are  sold or purchased through a broker,  the broker's commission
// is often computed  using a sliding scale  that depends upon the  value of the
// stocks traded.   Let's say  that a  broker charges the  amounts shown  in the
// following table:
//
//     ┌──────────────────┬─────────────────┐
//     │ Transaction size │ Commission rate │
//     ├──────────────────┼─────────────────┤
//     │ Under $2,500     │ $30 + 1.7%      │
//     ├──────────────────┼─────────────────┤
//     │ $2,500-$6,250    │ $56 + 0.66%     │
//     ├──────────────────┼─────────────────┤
//     │ $6,250-$20,000   │ $76 + 0.34%     │
//     ├──────────────────┼─────────────────┤
//     │ $20,000-$50,000  │ $100 + 0.22%    │
//     ├──────────────────┼─────────────────┤
//     │ $50,000-$500,000 │ $155 + 0.11%    │
//     ├──────────────────┼─────────────────┤
//     │ Over $500,000    │ $255 + 0.09%    │
//     └──────────────────┴─────────────────┘
//
// The minimum  charge is  $39.  Write a  program asking the  user to  enter the
// amount to trade, and make it display the amount of the commission:
//
//     Enter value of trade: <30000>
//     Commission: <$166.00>
//}}}
// Reference: page 81 (paper) / 106 (ebook)

#include <stdio.h>

    int
main(void)
{
    float commission, trade;

    printf("Enter value of trade: ");
    scanf("%f", &trade);

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

    printf("Commission: $%.2f\n", commission);

    return 0;
}
