// Purpose: compute the volume of a sphere **with a radius inputted by the user**
// Reference: page 34 (paper) / 59 (ebook)

#include <stdio.h>

#define PI 3.14159f

    int
main(void)
{
    float volume, radius;

    // use `scanf()` to let the user input the radius interactively
    scanf("%f", &radius);

    volume = (4.0f / 3.0f) * (PI * radius * radius * radius);
    printf("the volume of the sphere is %.1f cubic meters\n", volume);
}
