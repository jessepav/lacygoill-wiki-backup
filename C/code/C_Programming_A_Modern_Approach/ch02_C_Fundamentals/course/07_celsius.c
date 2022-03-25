// Purpose: converts a Fahrenheit temperature into Celsius
// Reference: page 24 (paper) / 49 (ebook)

#include <stdio.h>

// Formula to convert from Fahrenheit to Celsius:{{{
//
//     C = (F - 32) * (5 / 9)
//
// https://en.wikipedia.org/wiki/Fahrenheit#Conversion_(specific_temperature_point)
//}}}
#define FREEZING_PT 32.0f
// We don't want to use integers here.{{{
//
// Because C would truncate the result down to the nearest integer, which here is 0:
//
//     0 < 5/9 < 1
//     ⇒
//     5/9 ≈ 0
//}}}
#define SCALE_FACTOR (5.0f / 9.0f)

int main(void)
{
    float fahrenheit, celsius;

    printf("Enter Fahrenheit temperature: ");
    scanf("%f", &fahrenheit);

    celsius = (fahrenheit - FREEZING_PT) * SCALE_FACTOR;

    printf("Celsius equivalent: %.1f\n", celsius);
    //                           ^^
    //                           we only want 1 digit after the decimal point

    return 0;
}
