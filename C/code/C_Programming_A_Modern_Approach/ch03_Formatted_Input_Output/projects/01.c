// Purpose: Query  a date  from  the  user in  the  form  `mm/dd/yyyy` and  then
// displays it in the form `yyyymmdd`.

// Input: Enter a date (mm/dd/yyyy): <2/17/2011>
// Output: You entered the date <20110217>

// Reference: page 75 (paper) / 50 (ebook)

#include <stdio.h>

    int
main(void)
{
    int month, day, year;

    printf("Enter a date (mm/dd/yyyy): ");
    scanf("%d /%d /%d", &month, &day, &year);
    printf("You entered the date %04d%02d%02d\n", year, month, day);

    return 0;
}
