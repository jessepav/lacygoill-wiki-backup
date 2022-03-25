#!/bin/bash
# Purpose: execute simple substitution commands
# Reference: page 16 (paper) / 40 (ebook)

# `MA` → `Massachusetts`
# Test: `$ vimdiff ./input/addresses <(sed 's/MA/Massachusetts/' ./input/addresses)`
sed 's/MA/Massachusetts/' ./input/addresses

# ` MA` → `, Massachusetts`
# Test: `$ vimdiff ./input/addresses <(sed 's/ MA/, Massachusetts/' ./input/addresses)`
sed 's/ MA/, Massachusetts/' ./input/addresses
# Notice that the instruction needs to be quoted because it contains spaces.{{{
#
#         v                      v
#     sed 's/ MA/, Massachusetts/' ./input/addresses
#            ^    ^
#}}}

# ` MA` → `, Massachusetts`
# ` PA` → `, Pennsylvania`
# Test: `$ vimdiff ./input/addresses <(sed 's/ MA/, Massachusetts/; s/ PA/, Pennsylvania/' ./input/addresses)`
sed 's/ MA/, Massachusetts/; s/ PA/, Pennsylvania/' ./input/addresses
# Notice that – inside a single instruction – we can separate two consecutive commands with a semicolon.{{{
#
#     sed 's/ MA/, Massachusetts/; s/ PA/, Pennsylvania/' ./input/addresses
#                                ^
#}}}
