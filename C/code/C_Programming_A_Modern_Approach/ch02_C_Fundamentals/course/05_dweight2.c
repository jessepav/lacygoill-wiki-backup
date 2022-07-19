// Purpose: computes the dimensional weight of a box from input provided by the user
// Input: any set of 3 integers; e.g. 8, 12, 10
// Output: 2 messages; one giving the actual volume, the other the dimensional weight:{{{
//
//     Volume (cubic inches): 960
//     Dimensional weight (pounds): 6
//}}}
// Reference: page 23 (paper) / 48 (ebook)

#include <stdio.h>

    int
main(void)
{
    int height, length, width, volume, weight;

    printf("Enter height of box: ");
    scanf("%d", &height);

    printf("Enter length of box: ");
    scanf("%d", &length);

    printf("Enter width of box: ");
    scanf("%d", &width);

    volume = height * length * width;
    weight = (volume + (166 - 1)) / 166;

    printf("\nVolume (cubic inches): %d\n", volume);
    printf("Dimensional weight (pounds): %d\n", weight);
}
