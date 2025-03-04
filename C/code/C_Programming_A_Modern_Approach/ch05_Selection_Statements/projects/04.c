// Purpose: Ask the user to enter a wind speed (in knots), then display the corresponding description.{{{
//
// Use this simplified version of the  Beaufort scale, which is used to estimate
// wind force:
//
//     ┌───────────────┬─────────────┐
//     │ Speed (knots) │ Description │
//     ├───────────────┼─────────────┤
//     │ Less than 1   │ Calm        │
//     ├───────────────┼─────────────┤
//     │ 1-3           │ Light air   │
//     ├───────────────┼─────────────┤
//     │ 4-27          │ Breeze      │
//     ├───────────────┼─────────────┤
//     │ 28-47         │ Gale        │
//     ├───────────────┼─────────────┤
//     │ 48-63         │ Storm       │
//     ├───────────────┼─────────────┤
//     │ Above 63      │ Hurricane   │
//     └───────────────┴─────────────┘
//}}}
// Reference: page 96 (paper) / 121 (ebook)

#include <stdio.h>

    int
main(void)
{
    int speed;

    printf("Enter a wind speed (in knots): ");
    scanf("%d", &speed);

    if (speed < 1)
        printf("Calm\n");
    else if (speed <= 3)
        printf("Light air\n");
    else if (speed <= 27)
        printf("Breeze\n");
    else if (speed <= 47)
        printf("Gale\n");
    else if (speed <= 63)
        printf("Storm\n");
    else
        printf("Hurricane\n");

    return 0;
}
