#!/usr/bin/sed -nf

# Note how the arguments are written in the shebang.{{{
#
# None of these would work:
#
#     #!/usr/bin/sed -n -f
#     /usr/bin/sed: invalid option -- ' '~
#
#     #!/usr/bin/sed -f -n
#     /usr/bin/sed: couldn't open file  -n: No such file or directory~
#
#     #!/usr/bin/sed -fn
#     /usr/bin/sed: couldn't open file n: No such file or directory~
#
# Bottom line: The short  form of options must be concatenated  and `-f` must be
# at the end:
#}}}

s/"//g
s/^\.Se /CHAPTER /p
s/^\.Ah /	A. /p
s/^\.Bh /		B.  /p
