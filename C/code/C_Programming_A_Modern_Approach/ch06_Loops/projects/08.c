// Purpose: Print a one-month calendar.{{{
//
// The user specifies the number of days in the month and the day of the week on
// which the month begins:
//
//     Enter number of days in month: <31>
//     Enter starting day of the week (1=Sun, 7=Sat): <3>
//
//      Mo Tu We Th Fr Sa Su
//             1  2  3  4  5
//       6  7  8  9 10 11 12
//      13 14 15 16 17 18 19
//      20 21 22 23 24 25 26
//      27 28 29 30 31
//
// A line  in the  middle of  the calendar starts  from Sunday,  and goes  up to
// Saturday.
//
// Hint: This program isn't as  hard as it looks.  The most  important part is a
// `for` statement that uses a variable `i` to count from 1 to `n`, where `n` is
// the number  of days  in the month,  printing each value  of `i`.   Inside the
// loop, an `if` statement  tests whether `i` is the last day in  a week; if so,
// it prints a newline character.
//}}}
// Reference: page 123 (paper) / 148 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i, n, start;

    printf("Enter number of days in month: ");
    scanf("%d", &n);
    printf("Enter starting day of the week (1=Sun, 7=Sat): ");
    scanf("%d", &start);

    // print some header to make the calendar more readable
    printf("\n Mo Tu We Th Fr Sa Su\n");

    // Print some spaces  so that the first  day of the month is  in the correct
    // column.  Those can be seen as "blank dates".
    for (i = 1; i < start; i++)
        printf("   ");

    // now print the dates
    for (i = 1; i <= n; i++)
    {
        printf("%3d", i);
        // Break the line every time we've printed 7 days.
        // But we can't just use `i % 7 == 0`, because of the initial blank dates.
        if ((i + start - 1) % 7 == 0)
            printf("\n");
    }

    return 0;
}
