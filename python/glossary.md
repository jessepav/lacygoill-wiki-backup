# a
## argument
### keyword arguments

In a function  call, name-value pairs which  can be used to pass  arguments to a
function.

Pro: Contrary to  positional arguments, this  syntax is  immune to the  order in
which the arguments are specified, because  the semantics of a given argument is
no longer derived from its position but from its associated name.

Con: You need  to know  the names of  the parameters as  they're written  in the
function header.

---

    def my_function(a, b):
        ...

    my_function(b=12, a=34)
                ^--^  ^--^

This example will  work as expected even  though the order in which  we pass the
arguments in  the function call  (`b` then `a`) is  different than the  order in
which we declare the parameters in the function header (`a` then `b`).

That's because the keyword arguments `b=12` and `a=34` associate the values `12`
and `34` to  the names `b` and  `a`.  Python doesn't use the  arguments order to
determine  which  parameter should  be  assigned  `12`  and  `34`; it  uses  the
associated names.

### optional arguments

Arguments which  can be omitted  because their  parameters have been  assigned a
default  value.  A  default  value is  only  used if  its  argument is  omitted;
otherwise, it's ignored.

---

                        default value
                        vvv
    def my_function(a, b=34):
        ...

    my_function(12)
                  ^
                  no second argument for `b`

Here, in the function call, we've omitted the argument for the `b` parameter.
This will not cause an error, because the function will fall back on the default
value `34`.

    my_function(12, 56)
                    ^^

And here, the  default value `34` will  be ignored, because we did  not omit the
argument for `b`; we specified the explicit value `56`.

---

Optional parameters must be declared *after* mandatory parameters:

                                 ✔
                    v-------------------------v
    def my_function(mandatory, optional='value'):
        ...

                                 ✘
                    v-------------------------v
    def my_function(optional='value', mandatory):
        ...

    SyntaxError: non-default argument follows default argument˜

There  is  no  fundamental  reason  for this;  it's  just  an  arbitrary  choice
presumably made with the intent of following a simple rule.

It would also have been possible to allow for optional parameters to be declared
anywhere.   First,  the  mandatory  parameters would  be  assigned  reading  the
arguments from left to  right.  Then, whatever is left would  be assigned to the
optional parameters reading the arguments from right to left:
<https://stackoverflow.com/a/2900474>

We would  need to read  the arguments  from different well-known  positions (far
left and far right), to get simple rules for how 2 different types of parameters
should be assigned.

In contrast,  it's easier to  just state that  the optional arguments  should be
specified after  the mandatory ones; that's  just 1 rule, and  the arguments are
all  read in  the same  natural direction  (from left  to right;  that's natural
because we read/write code from left to right).

### positional arguments

Arguments in a  function call which need to  be passed in the same  order as the
parameters in the function header.

    def my_function(n: number, s: str):
        ...

    my_function(123, 'abc')
                ^^^  ^---^

Here, `123` and `"abc"` are positional  arguments.  They need to be specified in
the correct order for the function to work as expected.
That is,  we need to first  pass a value for  `n` then another for  `s`, because
that's the order in which these parameters are specified in the function header.

##
# c
## CapWords

Synonym for CamelCase.  Used by PEP8 when recommending to name a class using the
CapWords notation.

##
# i
## immutable

Said of something which cannot change.

##
# l
## logical error

Error in the logic of the code.

This is different than a syntax error or a type error.
A syntax or type error causes Python to raise an exception; not a logical error.
A logical error can only be handled by writing a proper test.

## logical expression

Expression which  is tested by  an `if` or  `while` statement, or  a conditional
operator.  It  can be  built from relational,  equality, and  logical operators.
It's always considered true or false.

##
# m
## module

A module is a script from which you can import some or all items in another script.

It lets you:

   - hide the details of your program's code and focus on its higher-level logic
     (by moving the low-level details into a separate file)

   - re-use functions in many different programs

   - share specific code with other programmers

   - use libraries of functions that other programmers have written

##
# n
## None

Keyword used to define a null value, or no value at all.

The `get()` method returns `None` when you ask for the value associated to a key
in a dictionary from which the key is absent.

##
# p
## PEP

Python Enhancement Proposal

## PEP 8

This PEP  specifies some coding conventions  with regards to how  Python code in
the standard library should be formatted/styled.

When working on a particular project, you should respect its style.
When  working on  your own  project, you  can do  whatever you  want, but  being
consistent helps, hence why you should follow *some* conventions.

In the absence of a particular style guide, PEP 8 is a good starting point.
You can follow it, or use it to build your own.

See: <https://peps.python.org/pep-0008/>

##
## parameter

In a  function header,  name of a  variable which will  be assigned  an argument
passed to a function at runtime inside a function call.

                    parameter
                    v---v
    def my_function(param):
        ...

    my_function(123)
                ^^^
                argument

In this example, `123` is an  argument passed to `my_function()` in the function
call `my_function(123)`.   Inside the function  body, `123` will be  assigned to
the parameter `param`.

### properties which determine whether it requires an argument
#### mandatory parameter

Parameter which must be assigned an argument.

#### optional parameter

Parameter for which the argument can be omitted.

###
### properties which determine how it should be assigned an argument

            special parameters used as delimiters
                       v                   v
    def func(pos, ..., /, pos_or_kwd, ..., *, kwd, ...):
             ├─┘          ├────────┘          ├─┘
             │            │                   └ keyword-only
             │            │
             │            └ positional-or-keyword
             │
             └ positional-only

#### keyword-only parameter

Parameter which  can only be assigned  with an argument passed  by keyword (e.g.
`arg='value'`).  It must be declared *after* the special parameter `*`.

#### positional-only parameter

Parameter which can only be assigned with an argument passed by position.
It must be declared *before* the special parameter `/`.

#### positional-or-keyword parameter

Parameter  which can  be assigned  with  an argument  passed by  position or  by
keyword.   That's the  default for  all parameters,  unless one  of the  special
parameters `*` or `/` appears in the function header.

##
# s
## set

Collection in which each item must be unique.

Contrary to a list or a tuple  which are surrounded by resp. square brackets and
parentheses, a set is surrounded by curly brackets.

              v                v
    >>> set = {1, 2, 3, 1, 2, 3}
    >>> print(set)
    {1, 2, 3}

Don't conflate a set with a dictionary:

In a set, there is no colon separating a key from its value:

                   v
    >>> dict = {'a': 1}
    >>> set = {'a'}

Also, contrary to a dictionary (and a list), a set is not ordered.

    >>> s = {'a', 'b', 'c'}
    >>> print(s)
    {'c', 'a', 'b'}

##
# t
## truthy/falsy

An expression is "truthy" or "falsy" if it's considered resp. true or false when
used as a logical expression in a test.  All expressions are truthy, except:

   - `None`
   - `False`
   - the number 0 (no matter how it's represented: `0`, `0.0`, ...)
   - an empty sequence or collection (e.g. `''`, `[]`, ...)

   - objects for which the `__bool__()` method returns `False`, or the
     `__len__()` method returns 0 (assuming  `__bool__` is undefined)

Those adjectives are colloquial; they're not used in the official documentation.
The latter rather talks about "truth value":
<https://docs.python.org/3/library/stdtypes.html#truth-value-testing>

To get the truth value of an expression, use the `bool()` function:

    >>> bool('')
    False

    >>> bool(123)
    True

## tuple

Immutable list.

It's useful when  you want to store a  set of values that should  not be changed
throughout the life of a program.

