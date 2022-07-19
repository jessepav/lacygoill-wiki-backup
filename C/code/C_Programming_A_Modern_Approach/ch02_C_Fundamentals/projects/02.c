// Purpose: compute the volume of a sphere with a 10-meter radius{{{
//
// Use this formula:
//
//     V = 4 / 3 * (π * r³)
//
// ---
//
// Proof for the formula.
//
// By definition, the circumference of a circle is:
//
//     2 * π * r
//
// We can use this to get the area `A` of a disk:
//
//     A = ∫[0, r](2 * π * x)dx
//         ^-----^
//         integrate from 0 to r
//
//       = 2 * π * (P(r) - P(0))
//
// Where `P(x)` is a primitive of `x`, which is any function of the form:
//
//       x² / 2 + k
//                ^
//                arbitrary constant
//
//     = x² + k
//
// So:
//
//     A = 2 * π * (r² + k - (0² + k))
//       = 2 * π * r²
//
// Now, we can use this to get the  volume `V₂` of one half of the sphere.  By
// integrating  disk  areas from  0  to  `r`, along  the  `[Oy)`  axis which  is
// orthogonal to the disks, includes their centers, and start from the center of
// the sphere:
//
//     V₂ = ∫[0, r](π * x²)dy
//        = π * ∫[0, r](x²)dy
//
// Notice the issue now.  We integrate along `[Oy)`, but the integrated function
// refers  to `x`  (which is  the radius  of an  integrated disk).   We need  to
// express `x` in function of `y`.  Using the Pythagorean theorem, we know that:
//
//     x² + y² = r²
//     ⇒
//     x = √(r² - y²)
//
// Let's plug this into the last `V₂` formula to get a volume:
//
//     V₂ = π * ∫[0, r](x²)dy
//        =
//          π * ∫[0, r](√(r² - y²)²)dy
//        =
//          π * ∫[0, r](r² - y²)dy
//        =
//          π * (∫[0, r](r²)dy - ∫[0, r](y²)dy)
//        =
//          π * (r² * ∫[0, r](1)dy - ∫[0, r](y²)dy)
//        =
//          π * (r² * r - r³/3)
//        =
//          π * (r³ - r³/3)
//        =
//          2 / 3 * π * r³
//
// That's only  for one half of  the sphere.  For  the whole sphere, we  need to
// multiply by 2; hence the final result:
//
//     V = 4 / 3 * (π * r³)
//}}}
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

#define PI 3.14159f

    int
main(void)
{
    float volume;
    // We don't declare `radius` as an integer to suppress a warning.{{{
    //
    // Which is given by `-Wconversion` when computing `volume`:
    //
    //     error: conversion from ‘int’ to ‘float’ may change value [-Werror=conversion]
    //}}}
    float radius = 10.0f;

    volume = (4.0f / 3.0f) * (PI * radius * radius * radius);
    printf("the volume of the sphere is %.1f cubic meters\n", volume);
}
