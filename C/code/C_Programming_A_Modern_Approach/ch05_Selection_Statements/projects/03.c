// Purpose: Modify the `broker.c` program by making both of the following changes:{{{
//
// Ask the user  to enter the number of shares and the  price per share, instead
// of the value of the trade.
//
// Add statements  that compute the  commission charged  by a rival  broker ($33
// plus 3¢  per share for fewer  than 2000 shares;  $33 plus 2¢ per  share for
// 2000  shares  or more).   Display  the  rival's  commission  as well  as  the
// commission charged by the original broker.
//}}}
// GCC Options: -Wno-conversion
// Reference: page 96 (paper) / 121 (ebook)

#include <stdio.h>

    int
main(void)
{
    int shares;
    float commission, share_price, traded;

    printf("Enter number of shares: ");
    scanf("%d", &shares);
    printf("Enter price per share: ");
    scanf("%f", &share_price);

    traded = shares * share_price;

    if (traded < 2500.00f)
        commission = 30.00f + 1.7f * traded / 100;
    else if (traded < 6250.00f)
        commission = 56.00f + 0.66f * traded / 100;
    else if (traded < 20000.00f)
        commission = 76.00f + 0.34f * traded / 100;
    else if (traded < 50000.00f)
        commission = 100.00f + 0.22f * traded / 100;
    else if (traded < 500000.00f)
        commission = 155.00f + 0.11f * traded / 100;
    else
        commission = 255.00f + 0.09f * traded / 100;

    if (commission < 39.00f)
        commission = 39.00f;

    printf("Original broker's commission: $%.2f\n", commission);

    if (shares < 2000)
        // $33 plus 3¢ per share for fewer than 2000 shares
        commission = 33.03f * shares;
    else
        // $33 plus 2¢ per share for 2000 shares or more
        commission = 33.02f * shares;
    printf("Rival broker's commission: $%.2f\n", commission);
}
