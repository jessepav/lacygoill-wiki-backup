// Purpose: study how complex expressions are evaluated
// Reference: page 63 (paper) / 88 (ebook)

#include <stdio.h>

    int
main(void)
{
    // Suppose we run across this complex expression:
    //
    //     a = b += c++ - d + --e / -f
    //
    // How will the operations be grouped?
    // Let's start with the operator(s) of highest precedence.{{{
    //
    // Here, there is only 1:
    //
    //     a = b += c++ - d + --e / -f
    //               ^^
    //
    // We group it with its operand:
    //
    //     a = b += (c++) - d + --e / -f
    //              ^   ^
    //}}}
    // Let's continue with the operator(s) of next precedence.{{{
    //
    // This time, there are 2 of them:
    //
    //     a = b += (c++) - d + --e / -f
    //                          ^^    ^
    //
    // We group them with their operands:
    //
    //     a = b += (c++) - d + (--e) / (-f)
    //                          ^   ^   ^  ^
    //}}}
    // The operator of next precedence is:{{{
    //
    //     a = b += (c++) - d + (--e) / (-f)
    //                                ^
    //
    // We group it with its operands:
    //
    //     a = b += (c++) - d + ((--e) / (-f))
    //                          ^            ^
    //}}}
    // The operators of next precedence are:{{{
    //
    //                    can't be a unary minus because it has an operand on its immediate left
    //                    v
    //     a = b += (c++) - d + ((--e) / (-f))
    //                    ^   ^
    //
    // It's not  obvious how  they should be  grouped, because  they're adjacent
    // to  the  same  operand  (`d`).   But   we  know  that  `+`  and  `-`  are
    // left-associative, so we should group the leftmost first (i.e. `-`):
    //
    //     a = b += ((c++) - d) + ((--e) / (-f))
    //              ^         ^
    //
    // Then, we group the leftmost remaining operator (i.e. `+`):
    //
    //     a = b += (((c++) - d) + ((--e) / (-f)))
    //              ^                            ^
    //}}}
    // The operators of next precedence are:{{{
    //
    //     a = b += (((c++) - d) + ((--e) / (-f)))
    //       ^   ^^
    //
    // Again,  it's not  obvious how  they  should be  grouped, because  they're
    // adjacent to the  same operand (`b`).  But  we know that `=`  and `+=` are
    // right-associative, so we should group the rightmost first (i.e. `+=`):
    //
    //     a = (b += (((c++) - d) + ((--e) / (-f))))
    //         ^                                   ^
    //
    // Then, we group the rightmost remaining operator (i.e. `=`):
    //
    //     (a = (b += (((c++) - d) + ((--e) / (-f)))))
    //     ^                                         ^
    //
    // The expression  is now fully parenthesized,  and we know exactly  how all
    // operations are grouped.
    //}}}

    return 0;
}
