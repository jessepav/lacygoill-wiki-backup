// Purpose: Prompt the  user to enter two  dates, then indicate which  one comes
// earlier on the calendar.
//
//     Enter first date (mm/dd/yy): <3>/<6>/<08>
//     Enter second date (mm/dd/yy): <5>/<17>/<07>
//     <5>/<17>/<07> is earlier than <3>/<6>/<08>
//
// Reference: page 97 (paper) / 122 (ebook)

#include <stdio.h>

    int
main(void)
{
    int month1, month2, day1, day2, year1, year2;

    printf("Enter first date (mm/dd/yy): ");
    scanf("%2d/%2d/%2d", &month1, &day1, &year1);

    printf("Enter second date (mm/dd/yy): ");
    scanf("%2d/%2d/%2d", &month2, &day2, &year2);

    if (year1 < year2
            || (year1 == year2 && month1 < month2)
            || (year1 == year2 && month1 == month2 && day1 < day2))
        printf("%d/%d/%02d is earlier than %d/%d/%02d\n",
                month1, day1, year1, month2, day2, year2);
    else if year1 == year2
        && month1 == month2
        && day1 == day2
        printf("%d/%d/%02d is the same date as %d/%d/%02d\n",
                month1, day1, year1, month2, day2, year2);
    else
        printf("%d/%d/%02d is earlier than %d/%d/%02d\n",
                month2, day2, year2, month1, day1, year1);
}
