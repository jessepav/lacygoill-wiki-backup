// Purpose: declare variables and assign them values
// Reference: page 17 (paper) / 42 (ebook)

#include <assert.h>
#include <stdio.h>

    int
main(void)
{
    // about declarations
    // Variables must be declared by specifying their type, then their name:{{{
    //
    //     vvv v----v
    //     int height;
    //
    //     float profit;
    //     ^---^ ^----^
    //     type   name
    //}}}
    // If several variables have the same type, their declarations can be combined:{{{
    //
    // By writing the type only once, then the variables separated with commas:
    //
    //     vvv
    //     int height, length, width, volume;
    //               ^       ^      ^
    //
    //     v---v
    //     float profit, loss;
    //                 ^
    //}}}
    //   And include initializations:{{{
    //
    //     int height = 8, length = 12, width = 10;
    //                ^^^         ^--^        ^--^
    //
    // You can even choose which one to initialize:
    //
    //     int height, length, width = 10;
    //                               ^--^
    //
    // Here, `height` and `length` remain uninitialized
    //}}}

    // about assignments
    // A variable can be given a value by means of assignment:{{{
    //
    //     height = 8;
    //            ^^^
    //     length = 12;
    //            ^--^
    //     width = 10;
    //           ^--^
    //
    // 8, 12, and 10 are said to be constants.
    //}}}
    // Once a variable has been assigned a value, it can be used to help compute the value of another variable:{{{
    //
    //     height = 8;
    //     length = 12;
    //     width = 10;
    //     volume = height * length * width;  // volume is now 960
    //              ^---------------------^
    //}}}

    // about printing
    // `printf()` can be used to display the current value of a variable:{{{
    //
    //     int height = 8;
    //     printf("Height: %d\n", height);
    //     ^----^
    //     Height: 8˜
    //
    // `%d` is  a placeholder indicating  where the value  of `height` is  to be
    // filled inside the  message. `\n` tells `printf()` to advance  to the next
    // line after printing `height`.
    //}}}
    // To print a floating-point number, we use `%f` instead of `%d`:{{{
    //
    //     float profit = 2150.48f;
    //     printf("Profit: $%f\n", profit);
    //                      ^^
    //     Profit: $2150.479980˜
    //}}}
    //   To force `%f` to print `p` digits after the decimal point, use `%.pf`:{{{
    //
    //     float profit = 2150.48f;
    //     printf("Profit: $%.2f\n", profit);
    //                       ^^
    //     Profit: $2150.48˜
    //}}}
    // `printf()` can print several variables in a single call:{{{
    //
    //     int height = 8;
    //     int length = 12;
    //     printf("Height: %d  Length: %d\n", height, length);
    //                                        ^----^  ^----^
    //     Height: 8  Length: 12˜
    //}}}
    // `printf()` can print any expression (not just variables):{{{
    //
    //     printf("%d\n", height * length * width);
    //                    ^---------------------^
    //}}}
}
