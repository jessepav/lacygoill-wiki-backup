// Purpose: Using the `switch` statement, convert a numerical grade into a letter grade:{{{
//
//     Enter numerical grade: <84>
//     Letter grade: <B>
//
// Use the following grading scale:
//
//     A = 90-100
//     B = 80-89
//     C = 70-79
//     D = 60-69
//     E = 50-59
//     F = 0-59
//
// Print an error message if the grade is larger than 100 or less than 0.
// Hint: Break the grade into two digits,  then use a `switch` statement to test
// the ten's digit.
//}}}
// Reference: page 97 (paper) / 122 (ebook)

#include <stdio.h>

    int
main(void)
{
    int grade, ten_s_digit;
    printf("Enter numerical grade: ");
    scanf("%d", &grade);

    if (grade < 0 || grade > 100)
    {
        printf("Invalid grade\n");
        return 0;
    }

    ten_s_digit = grade / 10;
    switch (ten_s_digit)
    {
        case 10: case 9:
            printf("Letter grade: A\n");
            break;
        case 8:
            printf("Letter grade: B\n");
            break;
        case 7:
            printf("Letter grade: C\n");
            break;
        case 6:
            printf("Letter grade: D\n");
            break;
        case 5:
            printf("Letter grade: E\n");
            break;
        default:
            printf("Letter grade: F\n");
            break;
    }

    return 0;
}
