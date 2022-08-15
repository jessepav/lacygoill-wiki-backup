# Purpose: use strings
# Reference: page 19 (paper) / 57 (ebook)

message = 'a single-quoted string can embed "double quotes"'
print(message)

message = "a double-quoted string can embed 'single quotes'"
print(message)

# The escape sequences `\t` and `\n` represent resp. a newline and a tab:
print('a\tb\nc')
#      tab character
#      v-----v
#     a       b
#     c
#
# Notice that Python doesn't need the  string to be double quoted; single quotes
# work too (that's different from Vim script).
