/* Some
 * Multiline
 * Comment */

// Some single line comment

// What's this `#include`?{{{
//
// A  directive  which includes  the  source  file  –  identified by  the  the
// following filename – into the current  source file, at the line immediately
// afterward.
//}}}
// We'll need  `printf()` to print  to the screen,  and `scanf()` to  take input
// from the user, which `/usr/include/stdio.h` can provide.
#include <stdio.h>
// We'll also need `strcpy()`.
#include <string.h>

// What's this `#define`?{{{
//
// A directive which which defines the following identifier (here `MYNAME`) as a
// macro.  Its syntax is:
//
//     #define identifier replacement-list
//
// It  instructs  the  preprocessor/compiler   to  replace  all  occurrences  of
// `identifier` with `replacement-list`.  Technically,  this process is a "token
// expansion".
//}}}
//   What's a macro?{{{
//
// A way to write something short and simple and have it automatically turn into
// something longer and more complicated.
//}}}
// Define the macro `MYNAME`.{{{
//
// At compile  time, the preprocessor  will replace all occurrences  of `MYNAME`
// with the string "Derek Banas".
//}}}
#define MYNAME "Derek Banas"

// Let's create  a global variable; it  will be accessible from  any function in
// the program.
int globalVar = 100;

// Any C program needs a `main()` function.
// That's always where the computer starts executing your code.
int main() {
    // Let's create  a function-local variable  of type `char`  (for character),
    // which can hold any of 256 characters.  The value must be surrounded
    // by single quotes.
    char firstLetter = 'D';

    // Let's create a  local variable of type `int`, which  can hold any integer
    // from `-32,768` up to `+32,768`.
    int age = 38;

    // Let's create an even bigger number.
    long int superBigNum = -327670000;

    // Let's create a float which can be as big as 38 decimal points in length.
    float piValue = 3.14159;

    // Let's create a float with even more precision.
    double reallyBigPi = 3.14159265358979323846;

    printf("\n");
    printf("This will print to screen\n\n");

    // `%d` are called "conversion characters"; they can be used as a placeholder
    // in a format string to be replaced with a value of (data) type `int`.
    printf("I am %d years old\n\n", age);
    //           ^^

    // For a value of type `long int`, use the conversion characters `%ld`.
    printf("Big Number %ld\n\n", superBigNum);
    //                 ^^^

    // For a value of type `float`, use the conversion characters `%f`.
    // However, by default, 6 decimal places would be printed (with a padding of
    // 0s if necessary);  we only want 5  places to show up, so  we must include
    // the desired precision.
    printf("Pi = %.5f\n\n", piValue);
    //           ^--^

    // For a value of type `float`, we can still use `%f`.
    printf("Big Pi = %.15f\n\n", reallyBigPi);
    //               ^---^

    // For a value of type `char`, we must use `%c`.
    printf("The first letter in my name is %c\n\n", firstLetter);
    //                                     ^^

    // For a string, we must use `%s`.
    printf("My Name is %s\n\n", "Derek");
    //                 ^^

    // To create a string, we must actually create an array of chars.
    // We must specify the  size of the array; it must be  big enough to contain
    // all the  characters in the  initializer string; here 11  + 1 (+1  for the
    // string terminator).
    char myName[12] = "Derek Banas";
    //         ^--^

    // *Or* we can let the compiler compute the size from the initializer string.
    char myName2[] = "Derek Banas";
    //          ^^

    // TODO: add explanation about purpose
    strcpy(myName, "Bob Smith");

    printf("My Name is %s\n\n", myName);
    printf("My Name2 is %s\n\n", myName2);
}
