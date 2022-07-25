// Purpose: Format product information input by the user.
// Input:{{{
//
//     Enter item number: <583>
//     Enter item price: <13.5>
//     Enter purchase date (mm/dd/yyyy): <10/24/2010>
//}}}
// Output:{{{
//
//     Item            Unit            Purchase
//                     Price           Date
//     583             $  13.50        10/24/2010
//
// ---
//
// The item number should be left justified.
// The unit price should be right justified.
// Allow dollar amounts up to $9999.99.  Hint: Use tabs to line up the columns.
//}}}
// Reference: page 75 (paper) / 50 (ebook)

#include <stdio.h>

    int
main(void)
{
    int number;
    float price;
    int month, day, year;

    printf("Enter item number: ");
    scanf("%d", &number);
    printf("Enter item price: ");
    scanf("%f", &price);
    printf("Enter purchase date (mm/dd/yyyy): ");
    scanf("%d /%d /%d", &month, &day, &year);

    // Notice how we use tab characters to align fields.{{{
    //
    // It works because when the OS is  asked to print a tab character, it moves
    // the  cursor to  the next  multiple of  8 cells.   Note that  this is  not
    // guaranteed by  the C  standard (it's  just how  OSes usually  interpret a
    // tab).
    //}}}
    printf("\nItem\t\tUnit\t\tPurchase\n");
    printf("\t\tPrice\t\tDate\n");
    printf("%d\t\t$%7.2f\t%02d/%02d/%04d\n", number, price, month, day, year);

    return 0;
}
