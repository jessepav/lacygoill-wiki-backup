// Purpose: Break down an ISBN input by the user.{{{
//
// Books are identified by an  International Standard Book Number (ISBN).  ISBNs
// assigned after  January 1, 2007 contain  13 digits, arranged in  five groups,
// such as 978-0-393-97950-3 (older ISBNs use 10 digits).
//
//    - The first group (the **GS1 prefix**) is currently either 978 or 979.
//    - The  **group identifier**  specifies the  language  or country  of origin  (for
//      example, 0 and 1 are used in English-speaking countries).
//    - The  **publisher  code**  identifies  the   publisher  (393  is  the  code  for
//      W.W. Norton).
//    - The **item  number** is assigned by  the publisher to identify  a specific book
//      (97950 is the code for this book).
//    - An ISBN ends with  a **check digit** that's used to verify  the accuracy of the
//      preceding digits.
//}}}
// Input: {{{
//
//     Enter ISBN: <978-0-393-97950-3>
//}}}
// Output: {{{
//
//     GS1 prefix: 978
//     Group identifier: 0
//     Publisher code: 393
//     Item number: 97950
//     Check digit: 3
//}}}
// Reference: page 75 (paper) / 50 (ebook)

#include <stdio.h>

    int
main(void)
{
    int gs1_prefix;
    int group_id;
    int publisher_code;
    int item_number;
    int check_digit;

    printf("Enter ISBN: ");
    scanf("%d-%d-%d-%d-%d", &gs1_prefix, &group_id, &publisher_code, &item_number, &check_digit);

    printf("GS1 prefix: %d\n", gs1_prefix);
    printf("Group identifier: %d\n", group_id);
    printf("Publisher code: %d\n", publisher_code);
    printf("Item number: %d\n", item_number);
    printf("Check digit: %d\n", check_digit);
}
