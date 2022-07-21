// Purpose: study scanf()
// Reference: page 42 (paper) / 67 (ebook)

#include <stdio.h>

    int
main(void)
{
    int a, b;
    int i, j;
    float x, y;

    // In a `scanf()` *format*, when finding:
    // whitespace, whitespace is skipped in the input.{{{
    //
    // In a `scanf()` format, you only need a whitespace in front of an ordinary
    // non-whitespace character;  and only  if you  want to  let the  user input
    // whitespace before inputting that character.
    //}}}
    // a conversion specification, whitespace is skipped in the input.{{{
    //
    // If you input this:
    //
    //     1/   2
    //       ^^^
    //
    // The next `printf()` prints this:
    //
    //     i = 1, j = 2
    //
    // ---
    //
    // But an  input whitespace still  terminates an  input item (i.e.  it's not
    // entirely ignored).
    //
    // For example, if you have this code:
    //
    //     int i;
    //     scanf("%d", &i);
    //     printf("i = %d\n", i);
    //
    // And you input `1 2`, this is printed:
    //
    //     i = 1
    //
    // Not this:
    //
    //     i = 12
    //}}}
    // ordinary non-whitespace, a character is either discarded or put back in the input.{{{
    //
    // Either:
    //
    //    - it matches the next input character, it's discarded, and `scanf()`
    //      goes on processing the rest of the format
    //
    //    - it does *not* match the next input character, and is put back into
    //      the input buffer, right before `scanf()` returns; which stops the
    //      processing of the format, and the reading of the input (until
    //      another possible call to `scanf()`)
    //
    // For example, if you input this (`▫` denotes a space):
    //
    //     ▫5/▫96
    //     ^  ^
    //
    // The next `printf()` prints this:
    //
    //     i = 5, j = 96
    //
    // Because any input space is ignored,  and the input slash is discarded (it
    // matches the slash in the format).
    //
    // OTOH, if you input this:
    //
    //     ▫5▫/▫96
    //       ^
    //
    // The next `printf()` prints this:
    //
    //     i = 5, j = <random integer>
    //
    // Because  the  slash  in  the  format does  not  match  the  second  input
    // space.  And `scanf()` does  not skip an input space to  find a match with
    // an ordinary non-whitespace in the format.  It only does that when looking
    // for a match with a conversion specification.
    //
    // If you want to be able to input a space before an ordinary character such
    // as this slash, you must write a space in the format:
    //
    //     scanf("%d /%d", &i, &j);
    //              ^
    //}}}


    // `scanf()` peeks at a character, and "puts it back" if it doesn't match the conversion specification.{{{
    //
    // That's possible because  `scanf()` does not read the  input directly; the
    // latter is first written into a buffer.
    //}}}
    //   A "put back" character can be read:{{{
    //
    //    - during the scanning of the next input item (since the next scanning
    //      will read from the same input buffer)
    //
    //    - by a subsequent call to `scanf()`
    //}}}
    //   Even the trailing/validating newline is peeked at.{{{
    //
    // It will be left for the next call of `scanf()`.
    //}}}
    // `scanf()` returns as soon as it fails to read an item; ignoring subsequent ones.{{{
    //
    // That's why, if you input `1!2`:
    //
    //    - `b` is not initialized with `2`
    //
    //    - the second call to `scanf()` does not prompt you for anything;
    //      because "!" is still at the start of the input buffer (it was put
    //      back by the previous `scanf()`),  but it doesn't match  the start
    //      of  the `%d%d%f%f` format,  which is `%d`
    //}}}
    scanf("%d/%d", &a, &b);
    printf("a = %d, b = %d\n", a, b);


    // `scanf()` can include several conversion specifications.
    // `%f`, `%e`, `%g` are interchangeable.{{{
    //
    // Whatever  you write,  `scanf()`  always uses  the same  rules  to read  a
    // floating-point number.  It looks for (in that order):
    //
    //    - a plus or minus sign (optional)
    //    - a series of digits (possibly containing a decimal point)
    //    - an exponent (optional):
    //      it must start with `e` or `E`, then an optional sign, then one or more digits
    //}}}
    scanf("%d%d%f%f", &i, &j, &x, &y);
    printf("i = %d, j = %d, x = %f, y = %f\n", i, j, x, y);
    // Q: What will `printf()` print if you input `1-20.3-4.0e3`?{{{
    //
    //     i = 1, j = -20, x = 0.300000, y = -4000.000000
    //
    // When `scanf()` reads an integer for `i`, it stops before the first minus:
    //
    //     1-20.3-4.0e3
    //      ^
    //
    // The minus is only  peeked at.  And since it can't be in  the middle of an
    // integer, it's put back for the next input item.
    //
    // Similarly, when reading an integer for `j`, the dot is only peeked at:
    //
    //     1-20.3-4.0e3
    //         ^
    //
    // Same thing when reading a floating-point number for `x`; the second minus
    // is also only peeked at:
    //
    //     1-20.3-4.0e3
    //           ^
    //}}}
}
