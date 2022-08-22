# Purpose: Write  an `if-elif-else`  chain that determines  a person's  stage of
# life.  Set a value for the variable `age`, and then:
#
#    - If the person is  less than 2 years old, print a message  that the
#      person is a baby.
#
#    - If the person is at least 2 years old but less than 4, print a message
#      that the person is a toddler.
#
#    - If the person is at least 4 years old but less than 13, print a message
#      that the person is a kid.
#
#    - If the person is at least 13 years old but less than 20, print a message
#      that the person is a teenager.
#
#    - If the person is at least 20 years old but less than 65, print a message
#      that the person is an adult.
#
#    - If the person is 65 years or older, print a message that the person is
#      an elder adult.
#
# Reference: page 85 (paper) / 123 (ebook)

age = 33

if age < 2:
    print("you're a baby")
elif age < 4:
    print("you're a toddler")
elif age < 13:
    print("you're a kid")
elif age < 20:
    print("you're a teenager")
elif age < 65:
    print("you're an adult")
else:
    print("you're an elder")
#     you're an adult
