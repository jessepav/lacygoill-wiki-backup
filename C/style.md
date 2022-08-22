# Where to put
## the return type of a function?

On a line alone.

Also, indent it, like this:
```c
    int
main(void)
```
Rationale: moving it on a separate line makes it easier to grep a function:

    $ grep '^functionname' *.c

Because then, there is no need to match the return type.
Also, this  makes it easier  to align the return  type and the  arguments types,
without getting too long lines (which are hard to read).

---

Don't put it on the same line as the function name:
```c
int main(void)
```
## the brace which starts
### a function body?

On a line alone.

Compare:
```c
    int
main(
    int parameterOne,
    int parameterTwo) {
    int localOne,
    int localTwo
}
```
Versus:
```c
    int
main(
    int parameterOne,
    int parameterTwo)
{
    int localOne,
    int localTwo
}
```
The second is much more readable.
See: <https://softwareengineering.stackexchange.com/a/2786>

This style is also followed by the Linux kernel:
<https://www.kernel.org/doc/html/latest/process/coding-style.html?highlight=style#placing-braces-and-spaces>

### a compound statement?

On a line alone, to be consistent with a function body.
