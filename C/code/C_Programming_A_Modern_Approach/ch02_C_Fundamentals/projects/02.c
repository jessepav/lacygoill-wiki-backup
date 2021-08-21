// Purpose: compute the volume of a sphere with a 10-meter radius{{{
//
// Use this formula:
//
//     v = 4 / 3 * (π * r³)
//
// ---
//
// Proof for the formula.
//
// By definition, the circumference of a circle is:
//
//     2 * π * r
//
// We can use this to get the area of a disk:
//
//     ∫[0, r](2 * π * x)
//     ^-----^
//     integrate from 0 ro r
//
// Which evaluates to:
//
//     2 * π * I(x)(0, r)
//     =
//     2 * π * r²/2
//     =
//     π * r²
//
// Now, we can use this to get the volume of one half of the sphere.
// By  integrating disk  areas from  0  to r,  along  the `[Ox)`  axis which  is
// orthogonal to the disks, includes their centers, and start from the center of
// the sphere:
//
//     ∫[0, r](π * y²)
//
// But first, we  need to express `y`  by using known symbols; i.e.  `r` and `x`
// (`x` being the position of the disk along `[Ox)`).
//
//     x² + y² = r²
//     ⇒
//     y = √(r² - x²)
//
// Let's plug this into the previous formula to get a volume:
//
//     ∫[0, r](π * y²)
//     =
//     ∫[0, r](π * √(r² - x²)²)
//     =
//     ∫[0, r](π * (r² - x²))
//     =
//     π * ∫[0, r](r² - x²)
//     =
//     π * (∫[0, r](r²) - ∫[0, r](x²))
//     =
//     π * (r² * ∫[0, r](1) - ∫[0, r](x²))
//     =
//     π * (r² * r - r³/3)
//     =
//     π * (r³ - r³/3)
//     =
//     2 / 3 * π * r³
//
// That's only  for one half of  the sphere.  For  the whole sphere, we  need to
// multiply by 2:
//
//     v
//     2 * 2 / 3 * π * r³
//     =
//     4 / 3 * π * r³
//     ^------------^
//     final result
//}}}
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

#define PI 3.14159f

int main(void)
{
    float volume;
    // We don't declare `radius` as an integer to suppress a warning.{{{
    //
    // Which would be given by `-Wconversion` when computing `volume`:
    //
    //     error: conversion from ‘int’ to ‘float’ may change value [-Werror=conversion]
    //}}}
    float radius = 10.0f;

    volume = (4.0f / 3.0f) * (PI * radius * radius * radius);
    printf("the volume of the sphere is %.1f cubic meters\n", volume);

    return 0;
}
