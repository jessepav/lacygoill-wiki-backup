# Purpose: Write  a program  that asks  the user  how many  people are  in their
# dinner  group.  If  the answer  is  more than  eight, print  a message  saying
# they'll  have to  wait for  a table.   Otherwise, report  that their  table is
# ready.

# Reference: page 117 (paper) / 155 (ebook)

n = int(input('How many people are in your dinner group? '))

if n > 8:
    print("You'll have to wait for a table.")
else:
    print('Your table is ready.')
#     How many people are in your dinner group? 4
#     Your table is ready.
