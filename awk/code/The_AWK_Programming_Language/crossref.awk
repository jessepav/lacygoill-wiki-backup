#!/usr/bin/awk -f

# A cross-referencing tool provides information which can be used to jump
# (cross) between definition (source code) and usage (reference).
#
# ctags and cscope are cross-referencing tools.
#
# But, the `nm(1)` command can probably also be used as a cross-referencing tool.
# Usage: `$ nm /boot/grub/i386-pc/*`
#
# This should scan all the files inside `/boot/grub/i386-pc/`.
# The output should like:
#
#     file.o:
#     00000c80 T _addroot
#     00000b30 T _checkdev
#     00000a3c T _checkdupl
#     U _chown
#     U _client
#     U _close
#     funmount.o:
#     00000000 T _funmount
#     U cerror
#
# There are 3 kind of lines in the output.
# The ones which have:
#
#    - 1 field  contain filenames
#    - 2 fields contain a flag and a function name
#    - 3 fields contain the same thing + an address in memory
#
# This output describes the functions which are undefined (U flag) and defined
# (T flag) in each file scanned. To use it and create a full cross-referencing
# tool, we would need to pipe its output to another program.
# But the output is intended to be read by a human, not a program.
# Indeed, the filename is not written before each function, so another a program
# wouldn't know to which file belongs a function.
# Besides, a cross-referencing tool doesn't need an address in memory.
# All in all, we would like this kind of output:
#
#     file.o: T _addroot
#     file.o: T _checkdev
#     file.o: T _checkdupl
#     file.o: U _chown
#     file.o: U _client
#     file.o: U _close
#     funmount.o: T _funmount
#     funmount.o: U cerror


# store the name of a file in the global variable `file`
NF == 1 { file = $1 }

# prepend the name of the file to which a function belongs
NF == 2 { print file, $1, $2 }

# replace the address in memory with the filename
NF == 3 { print file, $2, $3 }

# NOTE:
# In reality, the `nm` commands has flags which allow us to control its output.
# This program is just an example of where awk could be useful.
