// Purpose: The following table shows the daily flights from one city to another:{{{
//
//     ┌────────────────┬──────────────┐
//     │ Departure time │ Arrival time │
//     ├────────────────┼──────────────┤
//     │ 8:00 a.m.      │ 10:16 a.m.   │
//     ├────────────────┼──────────────┤
//     │ 9:43 a.m.      │ 11:52 a.m.   │
//     ├────────────────┼──────────────┤
//     │ 11:19 a.m.     │ 1:31 p.m.    │
//     ├────────────────┼──────────────┤
//     │ 12:47 p.m.     │ 3:00 p.m.    │
//     ├────────────────┼──────────────┤
//     │ 2:00 p.m.      │ 4:08 p.m.    │
//     ├────────────────┼──────────────┤
//     │ 3:45 p.m.      │ 5:55 p.m.    │
//     ├────────────────┼──────────────┤
//     │ 7:00 p.m.      │ 9:20 p.m.    │
//     ├────────────────┼──────────────┤
//     │ 9:45 p.m.      │ 11:58 p.m.   │
//     └────────────────┴──────────────┘
//
// Write a program  that asks the user  to enter a time (expressed  in hours and
// minutes,  using the  24-hour clock).   The  program should  then display  the
// departure and arrival times for the flight whose departure time is closest to
// that entered by the user:
//
//     Enter a 24-hour time: <13>:<15>
//     Closest departure time is <12>:<47> p.m., arriving at <3>:<00> <p>.m.
//
// Hint: Convert the input into a time  expressed in minutes since midnight, and
// compare it to the departure times,  also expressed in minutes since midnight.
// For example, `13:15` is `13 x 60 + 15 = 795` minutes since midnight, which is
// closer to `12:47 p.m.` (767 minutes since midnight)  than to any of the other
// departures.
//}}}
// Reference: page 96 (paper) / 121 (ebook)

#include <stdio.h>

    int
main(void)
{
    int hours, minutes, time_in_minutes,
        t1, t2, t3, t4, t5, t6, t7, t8;

    printf("Enter a 24-hour time: ");
    scanf("%d:%d", &hours, &minutes);
    time_in_minutes = hours * 60 + minutes;

    t1 = 8 * 60;
    t2 = 9 * 60 + 43;
    t3 = 11 * 60 + 19;
    t4 = 12 * 60 + 47;
    t5 = 14 * 60;
    t6 = 15 * 60 + 45;
    t7 = 19 * 60;
    t8 = 21 * 60 + 45;

    if (time_in_minutes < t1 + (t2 - t1) / 2)
        printf("Closest departure time is 8:00 a.m., arriving at 10:16 a.m.\n");
    else if (time_in_minutes < t2 + (t3 - t2) / 2)
        printf("Closest departure time is 9:43 a.m., arriving at 11:52 a.m.\n");
    else if (time_in_minutes < t3 + (t4 - t3) / 2)
        printf("Closest departure time is 11:19 a.m., arriving at 1:31 p.m.\n");
    else if (time_in_minutes < t4 + (t5 - t4) / 2)
        printf("Closest departure time is 12:47 p.m., arriving at 3:00 p.m.\n");
    else if (time_in_minutes < t5 + (t6 - t5) / 2)
        printf("Closest departure time is 2:00 p.m., arriving at 4:08 p.m.\n");
    else if (time_in_minutes < t6 + (t7 - t6) / 2)
        printf("Closest departure time is 3:45 p.m., arriving at 5:55 p.m.\n");
    else if (time_in_minutes < t7 + (t8 - t7) / 2)
        printf("Closest departure time is 7:00 p.m., arriving at 9:20 p.m.\n");
    else
        printf("Closest departure time is 9:45 p.m., arriving at 11:58 p.m.\n");
}
