# Purpose: create a simple program printing a "Hello World!" message to the screen
# Reference: page 9 (paper) / 47 (ebook)

# Notice that this script doesn't start with a shebang, and is not executable:{{{
#
#     $ cd ./code/Python_Crash_Course/ch01_Getting_Started/course/
#
#     $ [[ -x ./01_hello_world.py ]] || echo 'the script is NOT executable'
#     the script is NOT executable
#
#     $ ./01_hello_world.py
#     ./01_hello_world.py: Permission denied
#}}}
#   And yet, it can still be executed by passing it as an argument to a Python interpreter:{{{
#
#     $ python ./01_hello_world.py
#
# In both cases, the script is executed  by a Python interpreter; but not at the
# same moment.  In  the first case, the kernel first  tests whether the *script*
# is executable  (later, it will  find the shebang, and  pass the script  to the
# appropriate interpreter).  In the second  case, the kernel first tests whether
# the *interpreter* is executable.
#
# The python interpreter is always executable:
#
#     $ [[ -x $(which python) ]] && echo 'the interpreter is executable'
#     the interpreter is executable
#
# So, the second case always works.
# But there is no such guarantee in the first case.
#}}}

print('Hello Python world!')
#     Hello Python world!
