# ?

typeset [ {+|-}AHUaghlmrtux ] [ {+|-}EFLRZip [ n ] ]
        [ + ] [ name[=value] ... ]
typeset -T [ {+|-}Uglrux ] [ {+|-}LRZp [ n ] ]
        [ + | SCALAR[=value] array[=(value ...)] [ sep ] ]
typeset -f [ {+|-}TUkmtuz ] [ + ] [ name ... ]
       Set or display attributes and values for shell parameters.

       Except as noted below for control flags that change the behavior, a parameter is created for each name
       that does not already refer to one.  When inside a function, a new parameter is created for every name
       (even those that already exist), and is unset again when the function completes.  See  `Local  Parame‐
       ters'  in  zshparam(1).   The same rules apply to special shell parameters, which retain their special
       attributes when made local.

       For each name=value assignment, the parameter name is set to value.

       If the shell option TYPESET_SILENT is not set, for each remaining name that refers to a parameter that
       is already set, the name and value of the parameter are printed in the form of an assignment.  Nothing
       is printed for newly-created parameters, or when any attribute flags listed below are given along with
       the name.  Using `+' instead of minus to introduce an attribute turns it off.

       If no name is present, the names and values of all parameters are printed.  In this case the attribute
       flags restrict the display to only those parameters that have the specified attributes, and using  `+'
       rather than `-' to introduce the flag suppresses printing of the values of parameters when there is no
       parameter name.

       All forms of the command handle scalar assignment.   Array  assignment  is  possible  if  any  of  the
       reserved words declare, export, float, integer, local, readonly or typeset is matched when the line is
       parsed (N.B. not when it is executed).  In this case the arguments are parsed as  assignments,  except
       that  the  `+=' syntax and the GLOB_ASSIGN option are not supported, and scalar values after = are not
       split further into words, even if expanded (regardless of the setting of the KSH_TYPESET option;  this
       option is obsolete).

       Examples of the differences between command and reserved word parsing:

              # Reserved word parsing
              typeset svar=$(echo one word) avar=(several words)

       The above creates a scalar parameter svar and an array parameter avar as if the assignments had been

              svar="one word"
              avar=(several words)

       On the other hand:

              # Normal builtin interface
              builtin typeset svar=$(echo two words)

       The  builtin  keyword causes the above to use the standard builtin interface to typeset in which argu‐
       ment parsing is performed in the same way as for other commands.  This example creates a  scalar  svar
       containing  the  value  two  and another scalar parameter words with no value.  An array value in this
       case would either cause an error or be treated as an obscure set of glob qualifiers.

       Arbitrary  arguments are  allowed if  they take  the form  of assignments
       after  command-line   expansion;  however,  these  only   perform  scalar
       assignment:

              var='svar=val'
              typeset $var

       The  above  sets  the scalar parameter svar to the value val.  Parentheses around the value within var
       would not cause array assignment as they will be treated as ordinary characters when $var  is  substi‐
       tuted.  Any non-trivial expansion in the name part of the assignment causes the argument to be treated
       in this fashion:

              typeset {var1,var2,var3}=name

       The above syntax is valid, and has the expected effect of setting the three  parameters  to  the  same
       value, but the command-line is parsed as a set of three normal command-line arguments to typeset after
       expansion.  Hence it is not possible to assign to multiple arrays by this means.

       Note that each interface to any of the commands my be disabled separately.  For example,  `disable  -r
       typeset'  disables the reserved word interface to typeset, exposing the builtin interface, while `dis‐
       able typeset' disables the builtin.  Note that disabling the reserved word interface for  typeset  may
       cause problems with the output of `typeset -p', which assumes the reserved word interface is available
       in order to restore array and associative array values.

       Unlike parameter assignment statements, typeset's exit status on an assignment that involves a command
       substitution  does not reflect the exit status of the command substitution.  Therefore, to test for an
       error in a command substitution, separate the declaration of the parameter from its initialization:

              # WRONG
              typeset var1=$(exit 1) || echo "Trouble with var1"

              # RIGHT
              typeset var1 && var1=$(exit 1) || echo "Trouble with var1"

       To initialize a parameter param to a command output and mark it readonly,  use  typeset  -r  param  or
       readonly param after the parameter assignment statement.

       If no attribute flags are given, and either no name arguments are present or the flag +m is used, then
       each parameter name printed is preceded by a list of the attributes of that parameter (array, associa‐
       tion,  exported, float, integer, readonly, or undefined for autoloaded parameters not yet loaded).  If
       +m is used with attribute flags, and all those flags are introduced with  +,  the  matching  parameter
       names are printed but their values are not.

       The following control flags change the behavior of typeset:

       +      If  `+'  appears by itself in a separate word as the last option, then the names of all parame‐
              ters (functions with -f) are printed, but the values (function bodies) are not.  No name  argu‐
              ments may appear, and it is an error for any other options to follow `+'.  The effect of `+' is
              as if all attribute flags which precede it were given with a `+' prefix.  For example, `typeset
              -U  +' is equivalent to `typeset +U' and displays the names of all arrays having the uniqueness
              attribute, whereas `typeset -f -U +' displays the names of all autoloadable functions.  If + is
              the only option, then type information (array, readonly, etc.) is also printed for each parame‐
              ter, in the same manner as `typeset +m "*"'.

       -g     The -g (global) means that any resulting parameter will not be restricted to local scope.  Note
              that  this  does not necessarily mean that the parameter will be global, as the flag will apply
              to any existing parameter (even if unset) from an  enclosing  function.   This  flag  does  not
              affect  the  parameter after creation, hence it has no effect when listing existing parameters,
              nor does the flag +g have any effect except in combination with -m (see below).

       -m     If the -m flag is given the name arguments are taken as patterns (use quoting to prevent  these
              from  being  interpreted  as file patterns).  With no attribute flags, all parameters (or func‐
              tions with the -f flag) with matching names are printed (the shell option TYPESET_SILENT is not
              used in this case).

              If the +g flag is combined with -m, a new local parameter is created for every matching parame‐
              ter that is not already local.  Otherwise -m applies all other  flags  or  assignments  to  the
              existing parameters.

              Except  when  assignments are made with name=value, using +m forces the matching parameters and
              their attributes to be printed, even inside a function.  Note that -m is ignored if no patterns
              are given, so `typeset -m' displays attributes but `typeset -a +m' does not.

       -p [ n ]
              If  the  -p option is given, parameters and values are printed in the form of a typeset command
              with an assignment, regardless of other flags and options.  Note that the -H flag on parameters
              is respected; no value will be shown for these parameters.

              -p  may  be followed by an optional integer argument.  Currently only the value 1 is supported.
              In this case arrays and associative arrays are printed with newlines between indented  elements
              for readability.

       -T [ scalar[=value] array[=(value ...)] [ sep ] ]
              This  flag  has  a  different  meaning  when  used with -f; see below.  Otherwise the -T option
              requires zero, two, or three arguments to be present.  With no arguments, the list  of  parame‐
              ters created in this fashion is shown.  With two or three arguments, the first two are the name
              of a scalar and of an array parameter (in that order) that will be tied together in the  manner
              of  $PATH and $path.  The optional third argument is a single-character separator which will be
              used to join the elements of the array to form the scalar; if absent, a colon is used, as  with
              $PATH.   Only the first character of the separator is significant; any remaining characters are
              ignored.  Multibyte characters are not yet supported.

              Only one of the scalar and array parameters may be assigned an initial value (the  restrictions
              on assignment forms described above also apply).

              Both  the  scalar  and the array may be manipulated as normal.  If one is unset, the other will
              automatically be unset too.  There is no way of untying the variables without  unsetting  them,
              nor  of  converting  the  type  of  one of them with another typeset command; +T does not work,
              assigning an array to scalar is an error, and assigning a scalar to array sets it to be a  sin‐
              gle-element array.

              Note  that both `typeset -xT ...'  and `export -T ...' work, but only the scalar will be marked
              for export.  Setting the value using the scalar version causes a split on all separators (which
              cannot be quoted).  It is possible to apply -T to two previously tied variables but with a dif‐
              ferent separator character, in which case the variables remain joined as before but the separa‐
              tor is changed.

       Attribute  flags  that transform the final value (-L, -R, -Z, -l, -u) are only applied to the expanded
       value at the point of a parameter expansion expression using `$'.  They are not applied when a parame‐
       ter is retrieved internally by the shell for any purpose.

       The following attribute flags may be specified:

       -A     The names refer to associative array parameters; see `Array Parameters' in zshparam(1).

       -L [ n ]
              Left  justify and remove leading blanks from the value when the parameter is expanded.  If n is
              nonzero, it defines the width of the field.  If n is zero, the width is determined by the width
              of  the  value  of  the first assignment.  In the case of numeric parameters, the length of the
              complete value assigned to the parameter is used to determine the width,  not  the  value  that
              would be output.

              The width is the count of characters, which may be multibyte characters if the MULTIBYTE option
              is in effect.  Note that the screen width of the character is not taken into account;  if  this
              is  required, use padding with parameter expansion flags ${(ml...)...} as described in `Parame‐
              ter Expansion Flags' in zshexpn(1).

              When the parameter is expanded, it is filled on the right with blanks or truncated if necessary
              to  fit  the  field.   Note  truncation can lead to unexpected results with numeric parameters.
              Leading zeros are removed if the -Z flag is also set.

       -R [ n ]
              Similar to -L, except that right justification is used; when the  parameter  is  expanded,  the
              field  is  left  filled with blanks or truncated from the end.  May not be combined with the -Z
              flag.

       -U     For arrays (but not for associative arrays), keep only the first occurrence of each  duplicated
              value.   This may also be set for colon-separated special parameters like PATH or FIGNORE, etc.
              Note the flag takes effect on assignment, and the type of the variable  being  assigned  to  is
              determinative; for variables with shared values it is therefore recommended to set the flag for
              all interfaces, e.g. `typeset -U PATH path'.

              This flag has a different meaning when used with -f; see below.

       -Z [ n ]
              Specially handled if set along with the -L flag.  Otherwise, similar to -R, except that leading
              zeros  are  used  for  padding  instead  of blanks if the first non-blank character is a digit.
              Numeric parameters are specially handled: they are always eligible for padding with zeroes, and
              the zeroes are inserted at an appropriate place in the output.

       -a     The names refer to array parameters.  An array parameter may be created this way, but it may be
              assigned to in the typeset statement only if the reserved word form of typeset is  enabled  (as
              it is by default).  When displaying, both normal and associative arrays are shown.

       -f     The  names refer to functions rather than parameters.  No assignments can be made, and the only
              other valid flags are -t, -T, -k, -u, -U and -z.  The flag -t turns on  execution  tracing  for
              this  function;  the flag -T does the same, but turns off tracing for any named (not anonymous)
              function called from the present one, unless that function also has the -t or -T flag.  The  -u
              and -U flags cause the function to be marked for autoloading; -U also causes alias expansion to
              be suppressed when the function is loaded.  See the description of the `autoload'  builtin  for
              details.

              Note  that  the  builtin functions provides the same basic capabilities as typeset -f but gives
              access to a few extra options; autoload gives further additional options for the  case  typeset
              -fu and typeset -fU.

       -h     Hide:  only useful for special parameters (those marked `<S>' in the table in zshparam(1)), and
              for local parameters with the same name as a special parameter, though harmless for others.   A
              special parameter with this attribute will not retain its special effect when made local.  Thus
              after `typeset -h PATH', a function containing `typeset PATH' will  create  an  ordinary  local
              parameter  without  the usual behaviour of PATH.  Alternatively, the local parameter may itself
              be given this attribute; hence inside a function `typeset -h PATH' creates  an  ordinary  local
              parameter  and  the  special  PATH parameter is not altered in any way.  It is also possible to
              create a local parameter using `typeset +h special', where  the  local  copy  of  special  will
              retain its special properties regardless of having the -h attribute.  Global special parameters
              loaded from shell modules (currently those in zsh/mapfile and zsh/parameter) are  automatically
              given the -h attribute to avoid name clashes.

       -H     Hide  value:  specifies  that  typeset will not display the value of the parameter when listing
              parameters; the display for such parameters is always as if the `+' flag had been  given.   Use
              of the parameter is in other respects normal, and the option does not apply if the parameter is
              specified by name, or by pattern with the -m option.  This is on by default for the  parameters
              in  the  zsh/parameter and zsh/mapfile modules.  Note, however, that unlike the -h flag this is
              also useful for non-special parameters.

       -i [ n ]
              Use an internal integer representation.  If n is nonzero it defines the output arithmetic base,
              otherwise it is determined by the first assignment.  Bases from 2 to 36 inclusive are allowed.

       -E [ n ]
              Use an internal double-precision floating point representation.  On output the variable will be
              converted to scientific notation.  If n is nonzero it defines the number of significant figures
              to display; the default is ten.

       -F [ n ]
              Use an internal double-precision floating point representation.  On output the variable will be
              converted to fixed-point decimal notation.  If n is nonzero it defines the number of digits  to
              display after the decimal point; the default is ten.

       -l     Convert  the  result  to  lower case whenever the parameter is expanded.  The value is not con‐
              verted when assigned.

       -r     The given names are marked readonly.  Note that if name is a special  parameter,  the  readonly
              attribute can be turned on, but cannot then be turned off.

              If  the  POSIX_BUILTINS  option is set, the readonly attribute is more restrictive: unset vari‐
              ables can be marked readonly and cannot then be set; furthermore, the readonly attribute cannot
              be  removed  from any variable.  Note that in zsh (unlike other shells) it is still possible to
              create a local variable of the same name as this is considered  a  different  variable  (though
              this variable, too, can be marked readonly).

       -t     Tags the named parameters.  Tags have no special meaning to the shell.  This flag has a differ‐
              ent meaning when used with -f; see above.

       -u     Convert the result to upper case whenever the parameter is expanded.  The  value  is  not  con‐
              verted when assigned.  This flag has a different meaning when used with -f; see above.

       -x     Mark  for automatic export to the environment of subsequently executed commands.  If the option
              GLOBAL_EXPORT is set, this implies the option -g, unless +g is also explicitly given; in  other
              words  the  parameter  is  not made local to the enclosing function.  This is for compatibility
              with previous versions of zsh.

# ?

        -T [ scalar[=value] array[=(value ...)] [ sep ] ]

This flag has a different meaning when used with -f:

        % typeset -T -f some_func

This should turn on execution tracing for `some_func`, and turns off tracing for
any named (not anonymous) function called  from the latter, unless that function
has the `-t` or `-T` flag.

   > The flag -T does  the same, but turns off tracing for  any named (not anonymous)
   > function called from the present one, unless that function also has the -t or -T
   > flag.

Otherwise the -T option requires zero, two, or three arguments to be present.

With no arguments, the list of parameters created in this fashion is shown.

With two or  three arguments, the first two  are the name of a scalar  and of an
array parameter  (in that  order) that will  be tied together  in the  manner of
$PATH and $path.

The optional third  argument is a single-character separator which  will be used
to join  the elements of  the array to  form the scalar;  if absent, a  colon is
used, as with $PATH.

Only  the  first  character  of  the separator  is  significant;  any  remaining
characters are ignored.

Only one  of the scalar  and array parameters may  be assigned an  initial value
(the restrictions on assignment forms described above also apply).

Both the scalar and the array may be manipulated as normal.

If one is unset, the other will automatically be unset too.

There  is  no way  of  untying  the variables  without  unsetting  them, nor  of
converting the  type of one  of them with another  typeset command; +T  does not
work, assigning an array to scalar is  an error, and assigning a scalar to array
sets it to be a single-element array.

Note that both `typeset  -xT ...' and `export -T ...' work,  but only the scalar
will be marked for export.

Setting the  value using  the scalar  version causes a  split on  all separators
(which cannot be quoted).

It is possible to apply -T to two previously tied variables but with a different
separator character, in which case the variables remain joined as before but the
separator is changed.

##
##
##
# Concepts
## What are the 3 main characteristics of a parameter?

Its name, its value and its attributes (e.g. readonly).

## What are the 3 types of value you can assign to a parameter?

   - scalar (e.g. string, integer, float)
   - array (list indexed by integers)
   - associative array (unordered set of (key, value) pairs indexed by strings)

##
# Getting info
## What's a special parameter?

I think  it's a parameter which  is set automatically  by the shell, and  has an
influence on its behavior.

For example, `PATH` is set automatically, and changing its value may
help/prevent the shell from finding an executable (script or binary).

## How can I know whether a parameter is special?

In `man zshparam`, a special parameter is marked with the characters `<S>`.

##
## How to get the type of a parameter and its attributes?

    % echo ${(t)param}
              │
              └ man zshexpn
                > PARAMETER EXPANSION
                > Parameter Expansion Flags

Use  a string  describing the  type  of the  parameter  where the  value of  the
parameter would usually appear.

This string consists of keywords separated by hyphens (`-`).

The  first keyword  in the  string describes  the main  type:

   - `array`
   - `association`
   - `float`
   - `integer`
   - `scalar`

The other keywords describe the type in more detail:

    ┌──────────────┬────────────────────────────────────────────────┐
    │ export       │ exported parameters                            │
    ├──────────────┼────────────────────────────────────────────────┤
    │ hide         │ parameters with the `hide` flag                │
    ├──────────────┼────────────────────────────────────────────────┤
    │ hideval      │ parameters with the `hideval` flag             │
    ├──────────────┼────────────────────────────────────────────────┤
    │ left         │ left justified parameters                      │
    ├──────────────┼────────────────────────────────────────────────┤
    │ local        │ local parameters                               │
    ├──────────────┼────────────────────────────────────────────────┤
    │ lower        │ parameters whose value is converted            │
    │              │ to all lower case when it is expanded          │
    ├──────────────┼────────────────────────────────────────────────┤
    │ readonly     │ readonly parameters                            │
    ├──────────────┼────────────────────────────────────────────────┤
    │ right_blanks │ right justified parameters with leading blanks │
    ├──────────────┼────────────────────────────────────────────────┤
    │ right_zeros  │ right justified parameters with leading zeros  │
    ├──────────────┼────────────────────────────────────────────────┤
    │ special      │ special parameters defined by the shell        │
    ├──────────────┼────────────────────────────────────────────────┤
    │ tag          │ tagged parameters                              │
    ├──────────────┼────────────────────────────────────────────────┤
    │ unique       │ arrays which keep only the first occurrence    │
    │              │ of duplicated values                           │
    ├──────────────┼────────────────────────────────────────────────┤
    │ upper        │ parameters whose value is converted            │
    │              │ to all upper case when it is expanded          │
    └──────────────┴────────────────────────────────────────────────┘

## How to get the command which can re-assign the current value of a parameter?

    % typeset -p param
              ├┘
              └ warning:
                you can't combine it with other flags,
                they are ignored

## How to make the output more readable for a big array?

    % typeset -p1 param
                │
                └ arrays and associative arrays are printed
                  with newlines between indented elements for readability

##
## How to print all parameters in the shell?

        % typeset

## Without their values?

        % typeset +

## With the assignments which can re-create them?

        % typeset -p1
                    │
                    └ make a big array more readable

##
# String
## What happens if I change the type of a parameter from string to array?

In bash, it works as expected:
the variable contains an array with a single element whose value is the string.

    $ var='hello'
    $ typeset -a var
    $ typeset -p var
    declare -a var='([0]="hello")'˜

    $ echo $var
    hello˜

---

In zsh, the variable contains an empty array.

    % var='hello'
    % typeset -a var
    % typeset -p var
    typeset -a var=(  )˜
                    ^^
    % echo $var
    ∅˜

It seems that changing the type of a variable empties its value.

##
## How to get the number of characters in a string?

        ${#str}

##
# Array
## What's a subscript?  A subscript operator?  An index?

Here's how to refer to the element of an array whose index is `3`:

             ┌ subscript
             ├─┐
        ${arr[3]}
             │││
             ││└ subscript operator (2nd part)
             ││
             │└ index
             │
             └ subscript operator (1st part)

## What's the output of `echo $arr`?

The first element of the array in bash.
All its elements in zsh.

## What's the index of its first element?

`0` in bash.
`1` in zsh.

## What's the effect of setting the 'KSH_ARRAYS' option?

This is a zsh option.
If you set it:

    - array elements are numbered from zero

    - an array parameter without subscript refers to the first element instead
      of the whole array

    - braces are required to delimit a subscript:

            # ✘
            $path[2]

            # ✔
            ${path[2]}

    - braces are required to apply modifiers to any parameter:

            # ✘
            $PWD:h

            # ✔
            ${PWD:h}

By default  it's unset,  which means  that, in  zsh, you  don't need  the braces
around the parameter name most of the time.

## What's the difference between the subscripts `[@]` and `[*]`?

The shell considers the expansion of:

        - `$arr[@]` as SEVERAL words; as many as there are elements in the array
        - `$arr[*]` as a SINGLE word containing all the elements

## What's the meaning of the `-U` attribute?  (2)

It prevents a non-associative array from storing duplicate values.
It does the same thing for colon-separated special parameters (like `PATH`).

In  combination with  the  `-f` flag,  it suppresses  alias  expansion when  the
function is loaded.

## What's a “tied array”?

It's an array and a scalar whose values are linked:
changing one changes the other.

The tied scalar contains the elements of the array separated by colons.

For example: the `path` array is the companion of the `PATH` variable.
If you modify `path`, the change is reflected in `PATH`.

##
## How to get the number of elements in an array?

        ┌ can be shortened to `$#arr` in zsh
        ├────────┐
        ${#arr[@]}
          ^
          flag

        man zshexpn
      > PARAMETER EXPANSION
      > Parameter Expansion Flags

## How to get the number of characters in the element 3?

        ${#arr[3]}

If the  element is a number,  and not a  string, the evaluation will  return how
many digits it contains.

## How to get its last element?

        arr[-1]

## How to get all the elements, in any shell?

        "${arr[@]}"   →   "one" "two" ...

        "${arr[*]}"   →   "one two ..."

## How to get the element whose index is:  `1` plus the value stored in `$offset`?

        ${arr[1+$offset]}
                ^
                don't seem necessary, but better be safe

This  shows that  you  can  use another  parameter  expansion, and  mathematical
expression inside a subscript.

## How to get the list of tied arrays?

        % typeset -T

Warning:
This command doesn't print the special tied arrays:

        cdpath
        fignore
        fpath
        mailpath
        manpath
        module_path
        path
        psvar
        watch
        zsh_eval_context

Maybe because they're special (and not regular).

##
## How to assign a value to an array?  (4)

        % arr=( a b c )
        % arr=( [1]='a' [2]='b' [3]='c' )

        % typeset -a arr=( a b c )
        % typeset -a arr=( [1]='a' [2]='b' [3]='c' )
          │
          └ same as `typeset`, but more readable

## How to re-assign the value of the element whose index is 3?

        arr[3]=new_value

## How to remove the element whose index is `3`?

        arr[3]=()
              ├─┘
              └ zsh only

## How to prevent a non-associative array from containing duplicate values?

Give it the “uniqueness” attribute (zsh only):

        % typeset -U arr

Example:

        % typeset -U path
        % path=( ~/bin $path )

## How to remove an attribute from a parameter?

Re-invoke `typeset` with the same flag attribute, but prefixed with `+` instead of `-`.
For example, to remove the `-U` attribute from the `path` array:

        % typeset +U path

##
## How to create a tied array?

        % typeset -T FOO foo

Note that the order of the arguments is important.
The name of the scalar should come first, then the name of the array.

Also, you don't have to, but it's probably a good idea to respect the convention
which uses the same name with different cases.

## How to untie a scalar and its tied array?

Change the type of the scalar to an array, then assign it a string:

    % typeset -T FOO foo
    % typeset -a FOO
    % FOO='hi'

Result:

    % typeset -p FOO
    typeset FOO=hi˜

    % typeset -p foo
    typeset: no such variable: foo˜

## How to change the separator used by an existing tied scalar?

        % typeset -T FOO foo X
        % foo=( a b c )
        % echo $FOO
              aXbXc

        % typeset -T FOO foo Y
        % echo $FOO
              aYbYc

## How to create a tied scalar using `;` as a separator instead of `:`?

        % typeset -T A a \;
                         │
                         └ `;` is interpreted by the shell
                           as a separator between 2 consecutive commands

                           we need to escape it to make it lose its special meaning

##
## Can the subscript contain a range?

In zsh, yes.

In bash, yes, but:

   - only the last index in the range will be used

         $ arr=( a b c )
         $ arr[1,2]=d
         $ echo ${arr[@]}
         a b d˜

   - you can't assign a list to (an) array member(s):

         $ arr=( a b c )
         $ arr[1]=( B )
             bash: arr[1]: cannot assign list to array member

## How to get all the elements, except the first one and the last one?

        arr[2,-2]
            ├──┘
            └ zsh only

## How to re-assign the values of the elements whose index is between 2 and 4?

        arr=( a b c d e )
        arr[2,4]=( B C D )
            ├─┘
            └ zsh only

## What's the output of the last command in this zsh snippet?

        % arr=( a b c )
        % arr[2]=( D E F )
        % echo $arr
↣
            a D E F c

Here's what happened:

 1. the element `b` is removed
 2. the array `( D E F )` is inserted between the 2 sub-arrays before/after the
    previously removed element
↢

##
## Assigning to it all the filenames whose extension is `.c` or `.h`, anywhere below the cwd
### How to do it with only globs?

        % arr=( **/*.[ch] )

### How to do it without `**`?

        % arr=( "$(find . -name '*.[ch]' -print)" )

##
## `arr=( a b c ); print -l $arr[*]` prints 3 lines!  Shouldn't there be a single line?

The shell performed a field splitting when it processed the `% print` command.

If you quote the expansion, to prevent this splitting, you'll see that `$arr[*]`
is indeed considered as a single value:

    % arr=( a b c )
    % print -l "$arr[*]"
    a b c˜

Remember:
quote an expansion, if you don't want it to be altered by a field splitting.
