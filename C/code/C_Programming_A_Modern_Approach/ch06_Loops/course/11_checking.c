// Purpose: Balance a checkbook.{{{
//
// The program should offer the user a menu of choices:
//
//    - clear the account balance
//    - credit money to the account
//    - debit money from the account
//    - display the current balance
//    - exit the program
//
// The  choices should  be  represented by  the  integers  0, 1,  2,  3, and  4,
// respectively.  Here's what a session with the program might look like:
//
//     *** ACME checkbook-balancing program ***
//     Commands: 0=clear, 1=credit, 2=debit, 3=balance, 4=exit
//
//     Enter command: <1>
//     Enter amount of credit: <1042.56>
//     Enter command: <2>
//     Enter amount of debit: <133.79>
//     Enter command: <1>
//     Enter amount of credit: <1754.32>
//     Enter command: <2>
//     Enter amount of debit: <1400>
//     Enter command: <2>
//     Enter amount of debit: <68>
//     Enter command: <2>
//     Enter amount of debit: <50>
//     Enter command: <3>
//     Current balance: $<1145.09>
//     Enter command: <4>
//
// When the user  enters the command 4  to `exit`, the program  should exit from
// the `switch` statement *and* the surrounding loop, using a `return` statement
// (not a `goto`).
//}}}
// Reference: page 114 (paper) / 139 (ebook)

#include <stdio.h>

    int
main(void)
{
    int cmd;
    float amount, balance;

    balance = 0.00f;

    printf("*** ACME checkbook-balancing program ***\n");
    printf("Commands: 0=clear, 1=credit, 2=debit, 3=balance, 4=exit\n\n");

    while (1)
    {
        printf("Enter command: ");
        scanf("%d", &cmd);
         switch (cmd)
         {
             case 0:
                 balance = 0.0f;
                 break;

             case 1:
                 printf("Enter amount of credit: ");
                 scanf("%f", &amount);
                 balance += amount;
                 break;

             case 2:
                 printf("Enter amount of debit: ");
                 scanf("%f", &amount);
                 balance -= amount;
                 break;

             case 3:
                 printf("Current balance: $%.2f\n", balance);
                 break;

             case 4:
                 return 0;

             default:
                 printf("Commands: 0=clear, 1=credit, 2=debit, 3=balance, 4=exit\n\n");
                 break;
         }
    }

    return 0;
}
