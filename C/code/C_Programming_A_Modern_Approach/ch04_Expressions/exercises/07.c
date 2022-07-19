// Purpose: The algorithm for computing the UPC check digit ends with the following steps:
//
// Subtract 1 from the total.
// Compute the remainder when the adjusted total is divided by 10.
// Subtract the remainder from 9.
//
// It's tempting to try to simplify the algorithm by using these steps instead:
//
// Compute the remainder when the total is divided by 10.
// Subtract the remainder from 10.
//
// Q: Why doesn't this work?
//
// Reference: page 69 (paper) / 94 (ebook)


// A1: The  second algorithm  could  produce a  check digit  whose  value is  10
// (`10 - 0`).  But that's  not a valid value.  The check  digit, by definition,
// is a single digit number.


// A2: Let's formalize the first algorithm in 1 single expression:
//
//     9 - (T - 1) % 10
//
// Let's do the same for the second algorithm:
//
//     10 - T % 10
//
// Now, let's make the hypothesis that the two are equivalent.
// If that's true, then we can write:
//
//       9 - (T - 1) % 10 = 10 - T % 10
//     ⇔
//       T % 10 = 1 + (T - 1) % 10
//
// We also know that there exist values  of `T` for which `(T -1) % 10` is 0, 1,
// 2, ..., 9.  In  particular, there are values of `T`  for which the expression
// is 9.  Let's call `T₉` such a value:
//
//       (T₉ - 1) % 10 = 9
//     ∧
//       T₉ % 10 = 1 + (T₉ - 1) % 10
//     ⇒
//       T₉ % 10 = 1 + 9 = 10
//                         ^^
//                         ✘
//
// The last result is  impossible.  The remainder in a division  by 10 cannot be
// ten.  This proves  that our original hypothesis was wrong:  the two algorithm
// are *not* equivalent.
