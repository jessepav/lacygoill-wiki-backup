// Purpose: Ask the user for a 24-hour time, then display the time in 12-hour form:{{{
//
//     Enter a 24-hour time: <21:11>
//     Equivalent 12-hour time: <9>:<11> PM
//
// Be careful not to display 12:00 as 0:00.
// For more info, see: https://en.wikipedia.org/wiki/24-hour_clock
//}}}
// Reference: page 95 (paper) / 120 (ebook)

#include <stdio.h>
#include <stdbool.h>

    int
main(void)
{
    int hours, minutes;
    bool am;

    printf("Enter a 24-hour time: ");
    scanf("%2d :%2d", &hours, &minutes);

    if (hours == 0)
    {
        am = true;
        hours = 12;
    }
    else if (hours < 12)
        am = true;
    else if (hours == 12)
        am = false;
    else
    {
        am = false;
        hours -= 12;
    }

    printf("Equivalent 12-hour time: %d:%02d %s\n", hours, minutes, am ? "AM" : "PM");

    return 0;
}
