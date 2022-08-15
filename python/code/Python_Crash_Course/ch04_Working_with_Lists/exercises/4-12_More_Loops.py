# Purpose: All versions of  `foods.py` in this section have  avoided using `for`
# loops when printing to save space.   Choose a version of `foods.py`, and write
# two `for` loops to print each list of foods.

# Reference: page 65 (paper) / 103 (ebook)

my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]
my_foods.append('cannoli')
friend_foods.append('ice cream')

print('My favorite foods are:')
for food in my_foods:
    print(food)
#     My favorite foods are:
#     pizza
#     falafel
#     carrot cake
#     cannoli

print("\nMy friend's favorite foods are:")
for food in friend_foods:
    print(food)
#     My friend's favorite foods are:
#     pizza
#     falafel
#     carrot cake
#     ice cream
