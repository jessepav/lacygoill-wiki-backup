// Purpose: Generalize the program from Project  9 Chapter 5, which computes the
// earliest out of 2 dates, so that the user can enter any number of dates.
//
//     Enter a date (mm/dd/yy): <3>/<6>/<08>
//     Enter a date (mm/dd/yy): <5>/<17>/<07>
//     Enter a date (mm/dd/yy): <6>/<3>/<07>
//     Enter a date (mm/dd/yy): <0>/<0>/<0>
//     <5>/<17>/<07> is the earliest date

// Reference: page 124 (paper) / 149 (ebook)

#include <stdio.h>

    int
main(void)
{
    int month1, month2, day1, day2, year1, year2;

    printf("Enter a date (mm/dd/yy): ");
    scanf("%2d /%2d /%2d", &month1, &day1, &year1);

    while (1)
    {
        printf("Enter a date (mm/dd/yy): ");
        scanf("%2d /%2d /%2d", &month2, &day2, &year2);

        if (month2 == 0 && day2 == 0 && year2 == 0)
            break;

        if (year2 < year1
        || (year2 == year1 && month2 < month1)
        || (year2 == year1 && month2 == month1 && day2 < day1))
        {
            month1 = month2;
            day1 = day2;
            year1 = year2;
        }
    }

    printf("%d/%d/%02d is the earliest date\n", month1, day1, year1);

    return 0;
}
