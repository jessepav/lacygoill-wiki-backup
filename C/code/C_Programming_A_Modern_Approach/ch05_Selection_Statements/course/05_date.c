// Purpose: Printing a date in legal form.{{{
//
// Contracts and other legal documents are often dated in the following way:
//
//     Dated this ____ day of ____, 20__.
//
// Write a program that displays dates in  this form.  Ask the user to enter the
// date in month/day/year form, then display it in "legal" form:
//
//     Enter date (mm/dd/yy): <7/19/14>
//     Dated this <19>th day of <July>, 20<14>.
//
// Note that the program  should append the correct suffix to  the number of the
// day (i.e. `th`, `st`, `nd`, or `rd`).
//}}}
// Reference: page 89 (paper) / 114 (ebook)

#include <stdio.h>

    int
main(void)
{
    int month, day, year;

    printf("Enter date (mm/dd/yy): ");
    scanf("%2d /%2d /%4d", &month, &day, &year);

    printf("Dated this %d", day);
    switch (day)
    {
        case 1: case 21: case 31:
            printf("st"); break;
        case 2: case 22:
            printf("nd"); break;
        case 3: case 23:
            printf("rd"); break;
        default:
            printf("th"); break;
    }

    printf(" day of ");

    switch (month)
    {
        case 1:
            printf("January"); break;
        case 2:
            printf("February"); break;
        case 3:
            printf("March"); break;
        case 4:
            printf("April"); break;
        case 5:
            printf("May"); break;
        case 6:
            printf("June"); break;
        case 7:
            printf("July"); break;
        case 8:
            printf("August"); break;
        case 9:
            printf("September"); break;
        case 10:
            printf("October"); break;
        case 11:
            printf("November"); break;
        case 12:
            printf("December"); break;
        default:
            break;
    }

    printf(", 20%02d.\n", year);
    //           ^^
    //           make sure to correctly display a single-digit year
}
