// Purpose: compute the dimensional weight of a 12" x 10" x 8" box
// Reference: page 20 (paper) / 45 (ebook)

// Definition: dimensional weight.{{{
//
// A  shipping company  cannot base  the  fee of  a  box solely  on its  weight.
// Indeed, a box could  have a small weight, and still occupy  a lot of valuable
// space.  To  avoid losing money, they  need to take  the volume of a  box into
// account.  That's  where the  concept of "dimensional  weight" comes  in (also
// called volumetric weight).
//
// To compute the latter, the company divides the volume by some number.
// For  example, in  the US,  for  international shipments  (!= domestic),  this
// number is 166.   It's expressed in cubic  inches per pound.  The  result is a
// weight: the  number of pounds that  the box would  weigh if it had  a uniform
// density of 1 pound per 166 cubic inches.
//
// The  shipping fee  is based  on the  biggest number  between the  dimensional
// weight, and the actual one.
//
// This lets the company  enforce a minimal density under which  a big and light
// box could easily fall.
//}}}

#include <stdio.h>

    int
main(void)
{
    int length, width, height, volume, weight;

    length = 12;
    width = 10;
    height = 8;
    volume = length * width * height;
    // The result of a division is rounded down.
    // To avoid making the company lose money, we want to round up.
    // That's why we add 165.
    weight = (volume + (166 - 1)) / 166;

    printf("Dimensions: %dx%dx%d\n", length, width, height);
    printf("Volume (cubic inches): %d\n", volume);
    printf("Dimensional weight (pounds): %d\n", weight);

    return 0;
}
