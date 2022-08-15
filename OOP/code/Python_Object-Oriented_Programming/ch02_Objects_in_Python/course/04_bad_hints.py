# Purpose: more errors from mypy
# Reference: page 42 (paper) / 63 (ebook)


def odd(n: int) -> bool:
    return n % 2 != 0

def main():
#     Function is missing a return type annotation
#     Use "-> None" if function does not return a value
    print(odd('Hello, world!'))
    #     Argument 1 to "odd" has incompatible type "str"; expected "int"

if __name__ == '__main__':
    main()
    #     Call to untyped function "main" in typed context
    # This error would be fixed if you specified `-> None` in `def main():`.
