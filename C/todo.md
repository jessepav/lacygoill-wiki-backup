# Document
## `fmod()`

You can't apply the `%` operator on a floating-point number.
Use `fmod()` instead:
```c
    // GCC Options: -Wno-implicit-function-declaration -Wno-error -lm
    #include <stdio.h>

        int
    main(void)
    {
        int i = 3;
        printf("i %% 2 = %f\n", fmod(i, 2));
    }
```
    i % 2 = 1.000000

Notice that you  need to pass `-lm`  to `gcc(1)` (which itself will  pass it the
linker `ld(1)`); and it needs to be written *after* the compiled file:

    $ gcc -o /tmp/object /tmp/c.c -lm [...]
                                  ^^^

Without `-lm`, `ld(1)` would complain:

    undefined reference to `fmod'

That's because `ld(1)` doesn't know any implementation of `fmod()`.
But you  can help it find  one with `-lm`, which  asks it to search  the library
named `m` in the following way:

   - prepend `m` with `lib`
   - append `libm` with `.a`
   - look for the resulting file name in a standard list of directories

Whatever file `ld(1)` finds in the last step,  it will be used as if it had been
specified precisely by name.  For more info:

   - `man gcc /OPTIONS/;/Options for Linking/;/^\s*-l`
   - `man ld /OPTIONS/;/^\s*-l`
   - <https://stackoverflow.com/a/44176189>
   - <https://stackoverflow.com/a/11336610>

## `pow()`

There is no exponentiation operator.   Use `pow()` instead:
```c
    #include <stdio.h>
    #include <math.h>

        int
    main(void)
    {
        int i = 3;
        printf("i^3 = %f\n", pow(i, 3));
    }
```
    i^3 = 27.000000

Notice that:

   - `pow()` outputs a `double` by default, not an `int`
   - you need to include `math.h`

##
# Build Your Own Text Editor

<http://viewsourcecode.org/snaptoken/kilo/>
