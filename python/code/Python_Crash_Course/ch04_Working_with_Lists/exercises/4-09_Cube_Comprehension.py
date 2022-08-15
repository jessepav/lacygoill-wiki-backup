# Purpose: Use a list comprehension to generate a list of the first 10 cubes.
# Reference: page 60 (paper) / 98 (ebook)

cubes = [n ** 3 for n in range(1, 11)]
for cube in cubes:
    print(cube)
    #     1
    #     8
    #     27
    #     64
    #     125
    #     216
    #     343
    #     512
    #     729
    #     1000
