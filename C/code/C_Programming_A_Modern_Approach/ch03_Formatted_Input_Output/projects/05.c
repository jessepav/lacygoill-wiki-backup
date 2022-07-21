// Purpose: Query the user for the numbers from  1 to 16 (in any order) and then
// displays the  numbers in a 4  by 4 arrangement,  followed by the sums  of the
// rows, columns, and diagonals.
// Input:{{{
//
//     Enter the numbers from 1 to 16 in any order:
//     <16 3 2 13 5 10 11 8 9 6 7 12 4 15 14 1>
//}}}
// Output:{{{
//
//     <
//     16  3  2 13
//      5 10 11  8
//      9  6  7 12
//      4 15 14  1
//
//     Row sums: 34 34 34 34
//     Column sums: 34 34 34 34
//     Diagonal sums: 34 34
//     >
//}}}
// Reference: page 75 (paper) / 50 (ebook)

#include <stdio.h>

    int
main(void)
{
    int n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16;
    int row1_sum, row2_sum, row3_sum, row4_sum;
    int col1_sum, col2_sum, col3_sum, col4_sum;
    int diag_l2r_sum, diag_r2l_sum;

    printf("Enter the numbers from 1 to 16 in any order:\n");
    scanf("%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d",
            &n1, &n2, &n3, &n4, &n5, &n6, &n7, &n8,
            &n9, &n10, &n11, &n12, &n13, &n14, &n15, &n16);

    printf("%2d %2d %2d %2d\n", n1, n2, n3, n4);
    printf("%2d %2d %2d %2d\n", n5, n6, n7, n8);
    printf("%2d %2d %2d %2d\n", n9, n10, n11, n12);
    printf("%2d %2d %2d %2d\n", n13, n14, n15, n16);

    row1_sum = n1  + n2  + n3  + n4;
    row2_sum = n5  + n6  + n7  + n8;
    row3_sum = n9  + n10 + n11 + n12;
    row4_sum = n13 + n14 + n15 + n16;

    col1_sum = n1  + n5  + n9  + n13;
    col2_sum = n2  + n6  + n10  + n14;
    col3_sum = n3  + n7 + n11 + n15;
    col4_sum = n4 + n8 + n12 + n16;

    diag_l2r_sum = n1 + n6 + n11 + n16;
    diag_r2l_sum = n4 + n7 + n10 + n13;

    printf("\nRow sums: %d %d %d %d", row1_sum, row2_sum, row3_sum, row4_sum);
    printf("\nColumn sums: %d %d %d %d", col1_sum, col2_sum, col3_sum, col4_sum);
    printf("\nDiagonal sums: %d %d\n", diag_l2r_sum, diag_r2l_sum);
    // Trivia: If the  row, column,  and diagonal  sums are  all the  same (like
    // here), the numbers are said to form a **magic square**.
    // The magic  square in the current  example appears in a  1514 engraving by
    // artist and mathematician  Albrecht Dürer.  Notice that  the date appears
    // in the middle of the last row.
}
