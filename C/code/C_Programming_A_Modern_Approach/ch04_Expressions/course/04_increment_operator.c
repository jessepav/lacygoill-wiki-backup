// Purpose: study assignment operators
// GCC Options: -Wno-conversion
// Reference: page 61 (paper) / 86 (ebook)

#include <stdio.h>

    int
main(void)
{
    int i = 1, j = 1;

    // `++` and `--` resp. increment and decrement a variable.
    i++;
    printf("i is %d\n", i);
    //     i is 2
    i--;
    printf("i is %d\n", i);
    //     i is 1


    // Using `++`/`--` as prefix and postfix operators does not always give the same results. {{{
    //
    // Just like `=`, `++` and `--` can be part of a larger expression, and have
    // the same side effect: they change  an lvalue.  But contrary to `=` (which
    // is a binary operator), `++` and `--`:
    //
    //    - are unary operators
    //    - can be used as prefix or postfix operators
    //
    // When part  of a larger expression,  the lvalue is used  (i.e. fetched and
    // *not*  discarded).  The  retrieved lvalue  depends  on how  you used  the
    // operators (prefix vs postfix):
    //
    //    - prefix: the lvalue is changed *before* being fetched
    //    - postfix: the lvalue is changed *after* being fetched
    //}}}
    // prefix test
    printf("i is %d\n", ++i);
    printf("i is %d\n", i);
    //     is is 2
    //     is is 2
    //
    // postfix test
    i = 1;
    printf("i is %d\n", i++);
    printf("i is %d\n", i);
    //     is is 1
    //     is is 2


    // the postfix `++`/`-` have a higher precedence than unary `-`/`+`
    i = 1;
    j = -i++;
    printf("j is %d\n", j);
    //     j is -1
    // If the opposite was true, an error would have been given: {{{
    //
    //     i = 1;
    //     j = (-i)++;
    //     error: lvalue required as increment operand˜
    //
    // That's because  `++`/`--` can only  operate on  an lvalue (just  like all
    // assignment operators require their LHS to  be an lvalue); and `-i` is not
    // an lvalue.
    //}}}

    // TODO: Find examples where the rules about the associativity of `++`/`--` apply.{{{
    //
    // The book says that:
    //
    //    - the postfix `++`/`--` are left-associative
    //    - the prefix `++`/`--` are right-associative
    //    - the prefix `++`/`--` have the same precedence as the unary `+`/`-`
    //
    // ---
    //
    // I *think* the last rule is applied with a statement such as:
    //
    //     ++a[i]
    //
    // We know that:
    //
    //    - A: the prefix `++` has the same precedence as the unary `+`/`-`
    //
    //    - B: `[]` (array subscripting operator) has higher precedence than
    //      the unary `+`/`-` (see Annex A in the book)
    //
    // `A ∧ B ⇒ C`, where C means:
    //
    //    - C:  `[]` has higher precedence than the prefix `++`
    //
    // Conclusion:
    //
    //       ++a[i]
    //     ⇔
    //       ++(a[i])
    //}}}

    return 0;
}
