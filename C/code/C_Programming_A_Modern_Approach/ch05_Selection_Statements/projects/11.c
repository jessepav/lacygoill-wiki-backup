// Purpose: Ask the user for a two-digit number, then print the English word for the number:{{{
//
//     Enter a two-digit number: <45>
//     You entered the number forty-five.
//
// Hint: Break the number into two digits.   Use one `switch` statement to print
// the word for the first digit ("twenty", "thirty", and so forth).
// Use a second `switch` statement to print the word for the second digit.
// Don't forget that the numbers between 11 and 19 require special treatment.
//}}}
// Reference: page 97 (paper) / 122 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n, digit1, digit2;

    printf("Enter a two-digit number: ");
    scanf("%2d", &n);

    printf("You entered the number ");
    digit1 = n / 10;
    digit2 = n % 10;
    switch (digit1)
    {
        case 0:
              break;
        case 1:
              switch (digit2)
              {
                  case 0:
                      printf("ten\n");
                      return 0;
                  case 1:
                      printf("eleven\n");
                      return 0;
                  case 2:
                      printf("twelve\n");
                      return 0;
                  case 3:
                      printf("thirteen\n");
                      return 0;
                  case 4:
                      printf("fourteen\n");
                      return 0;
                  case 5:
                      printf("fifteen\n");
                      return 0;
                  case 6:
                      printf("sixteen\n");
                      return 0;
                  case 7:
                      printf("seventeen\n");
                      return 0;
                  case 8:
                      printf("eighteen\n");
                      return 0;
                  case 9:
                      printf("nineteen\n");
                      return 0;
                  default:
                      return 0;
              }
              break;
        case 2:
              printf("twenty");
              break;
        case 3:
              printf("thirty");
              break;
        case 4:
              printf("fourty");
              break;
        case 5:
              printf("fifty");
              break;
        case 6:
              printf("sixty");
              break;
        case 7:
              printf("seventy");
              break;
        case 8:
              printf("eighty");
              break;
        case 9:
              printf("ninety");
              break;
        default:
              break;
    }

    switch (digit2)
    {
        case 0:
            break;
        case 1:
            printf("-one\n");
            break;
        case 2:
            printf("-two\n");
            break;
        case 3:
            printf("-three\n");
            break;
        case 4:
            printf("-four\n");
            break;
        case 5:
            printf("-five\n");
            break;
        case 6:
            printf("-six\n");
            break;
        case 7:
            printf("-seven\n");
            break;
        case 8:
            printf("-eight\n");
            break;
        case 9:
            printf("-nine\n");
            break;
        default:
            break;
    }
}
