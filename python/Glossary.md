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
all read  in the same  direction, from left to  right (that matches  the natural
direction in which we read/write code).

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
## assignment

Statement which binds a name to an object by placing it inside a namespace.

---

An assignment to a name always goes into the innermost scope (unless `global` or
`nonlocal` has been used earlier).

The same is true  for a deletion: the statement `del  x`  removes the binding of
`x` from the namespace referenced by the local scope.

More generally, all operations that introduce  new names use the local scope: in
particular,  import  statements and  function  definitions  bind the  module  or
function name in the local scope.

### augmented assignment

Statement which combines a binary operation and an assignment.

Example:

    x += 1

In C, that's called a *compound* assignment.

##
# b
## byte array

Mutable version of a bytes objects.

A byte array supports most methods which  work on strings and most methods which
work on  lists.  The former  produce a copy  because strings are  immutable; the
latter operate in-place because lists *are* mutable.

## bytes object

Immutable sequence  of bytes.   Each item  in a  bytes object  is an  integer in
`[0, 256)`.

In case you wonder  where 256 comes from, remember that a  byte contains 8 bits,
and that each bit can have 2 values; that's 2⁸ = 256 values for a byte.

##
# c
## CapWords

Synonym for CamelCase.  Used by PEP8 when recommending to name a class using the
CapWords notation.

## constructor

Function which can build some iterable by exhausting an iterator.

Examples of built-in constructors:

   - `list()`
   - `dict()`
   - `set()`
   - `frozenset()`
   - `bytearray()`

---

TODO: I think that's only one possible meaning.
It seems that `int()` is also a constructor.
From "Python Object-Oriented Programming" page 273:

   > In this example, the frequencies object uses the function int() to create default
   > values. This is the **constructor** for an integer object.

That doesn't fit our current definition.

## container

Object that holds other objects, like a list, tuple, dictionary or set.
More container types are available in the `collections` module.

Technically,  a container  is an  object which  implements the  `__contains__()`
method, while an iterable is an object which implements the `__iter__()` method.
So, in  theory, both  concepts are  orthogonal, and you  could create  an object
which is  a container but not  an iterable.  However, in  practice, all built-in
containers are  also iterables  (same thing for  most containers  implemented by
libraries).

---

A string is an  iterable, because you can iterate over  its characters, but it's
not a container.  To be a container,  it would need to hold objects, which means
that its characters would need to be  objects; but they are not.  In particular,
there is no `char` type, and a character doesn't have attributes nor methods.

##
# d
## dictionary view

Iterable returned from `dict.keys()`, `dict.values()`, or `dict.items()`.

It's not a simple  list.  A list could not be updated  dynamically when an entry
in the dictionary is added, removed, or changed.  A view is updated.
To force the dictionary view to become a full list use `list(dictview)`.

A  dictionary  view  can be  iterated  over  to  yield  its data,  and  supports
membership tests.

##
# h
## hashability

Characteristic of an object which allows it to  be used as a dictionary key or a
set member.  Dictionaries and sets use the hash value internally.

## hashable

Said of an object  whose hash value (as given by  its `__hash__()` method) never
changes during its lifetime, and which can be compared to other objects (it also
needs an `__eq__()` method).

The hash  value of a given  object remains the same  only for the duration  of a
Python process.   If you start another  Python process, an object  with the same
type and value can have a different hash (and ID):

    $ python -c 'print(hash("hello"))'
    -5997811172218844908

    $ python -c 'print(hash("hello"))'
    7399159032506071523

---

Hashable objects which compare equal must have the same hash value.

---

Mutable containers are not hashable.

Most immutable objects are hashable; but an immutable container (such as a tuple
and a frozenset) is only hashable if its items are hashable.

Objects which  are instances  of user-defined classes  are hashable  by default.
They  all compare  unequal (except  with themselves),  and their  hash value  is
derived from their `id()`.

##
# i
## idiom

A syntax which is particular to a language.

Usually, using an idiom makes the code less verbose.
Often, it makes it also easier to read and understand.
But in  general, that's not  necessarily true;  e.g. bash provides  some obscure
idioms which are hard to read.

A list  comprehension is an  example of  idiom in Python;  you won't find  it in
other languages.  In  contrast, a `for` loop  is not an idiom; you  can find the
same syntax in many other languages.

## immutable

Said of an object whose value cannot change.
The opposite is "mutable", which is said of an object whose value *can* change.

It's important to understand that "mutable" and "immutable" are properties of an
*object*; they are not properties of a name/variable.  For example:
```python
age = 42
age = 43
```
`age` has  changed, but  that doesn't mean  that the object  whose value  is the
number 42 is mutable.  An integer is  *im*mutable, so 42 is immutable too.  What
happens in  the second statement, is  that a new  object, whose value is  43, is
created, and the name `age` is re-bound to that new object in the namespace tied
to the current scope.  This is confirmed by the output of `id()`:
```python
age = 42
print(id(age))
age = 43
print(id(age))
```
    9802560
    9802592

The ID  of the object to  which `age` is  bound has changed; that's  because the
object itself  has changed.  Therefore, there  is no mutation; a  mutation deals
with a single object, not several.

In contract, a list *is* a mutable object:
```python
l = [1, 2]
print(l)
print(id(l))
l.pop()
print(l)
print(id(l))
```
    [1, 2]
    139635115412416
    [1]
    139635115412416

Notice that the  *value* of the list  object to which `l` is  bound has changed.
But the ID has  not changed, which means that the object  itself has not changed
(only its value).  That's a mutation: a single object whose value changes.

Dictionaries and instances of classes are other examples of mutable objects.

## in-place

Said of  an operation on a  name which modifies  the object bound to  that name,
instead of rebinding the name to a newly created object.

Example:
```python
l = [1]
ll = l
ll += [2]
print(l)
print(ll)
```
    [1, 2]
    [1, 2]

Here, the  `ll += [2]` augmented assignment  did not rebind  the name `ll`  to a
newly created object `[1, 2]`; all the bindings have remained the same.  It just
modified the old object `[1]` which both `l` and `ll` were bound to.

Here is  another similar  example which relies  on a method  call instead  of an
augmented assignment:
```python
l = [1, 2]
ll = l
ll.pop()
print(l)
print(ll)
```
    [1]
    [1]

## iterable

An object capable of returning its members one at a time.
Technically, this means that the object implements the `__iter__()` method.

Examples of  iterables include all  sequence types  (such as `list`,  `str`, and
`tuple`), and some non-sequence types like `set` and `dict`.

Iterables can be  used in a `for` loop  and in other places where  a sequence is
needed (`zip()`, `map()`, ...).

##
# l
## library

Collection of functions  and objects that provide  functionalities which augment
the capabilities of a language.

For  example, from  the  Python's math  library, you  can  import the  factorial
function, which calculates the factorial of a number:

    >>> from math import factorial
    >>> factorial(5)
    120

A library can be implemented as a module or as a package of modules.

##
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
## mapping

A  container object  that  supports  arbitrary key  lookups  and implements  the
methods specified in the `Mapping` or `MutableMapping` abstract base classes.

Examples include:

   - `dict`
   - `collections.Counter`
   - `collections.OrderedDict`
   - `collections.defaultdict`

##
## method
### magic

Informal synonym for the adjective special in "special method".

### special

Said  of a  method that  is called  implicitly by  Python to  execute a  certain
operation on a  type, such as addition.   Such a method has a  name starting and
ending with dunderscores.

In a class definition, `__init__()` is an example of special method.

See: <https://docs.python.org/3/reference/datamodel.html#specialnames>

##
## modular exponentiation

Remainder when an integer `b` (base) is  raised to the power `e` (exponent), and
divided by a positive integer `m` (modulus).

In arithmetic, it's written as $b^e \mod m$.
In Python, it can be computed with `pow(b, e, m)`.

## modular multiplicative inverse

A modular multiplicative inverse  of an integer `a` is an  integer `x` such that
the product `a*x` is congruent to 1  with respect to the modulus `m`.  Formally,
it's noted $ax \equiv 1 \mod m$

This lets  us extend the definition  of a modular exponentiation  to cases where
the exponent is  negative.  Indeed, you can  change the sign of  the exponent to
positive, provided you replace the base with its modular multiplicative inverse:

$$b^e\mod m\equiv i^\left(-e\right)\mod m$$

Here, `i` is the modular multiplicative inverse of `b`.
If  `e` is  negative,  we can't  compute the  modular  exponentiation using  the
expression on the LHS, but we can if we use the one on the RHS.

In   Python,  the   modular  multiplicative   inverse  can   be  computed   with
`pow(b, -1, m)`.  But `b`  must be relatively prime to `m`.   That is, they must
have no common divisor  (except for 1).  In arithmetic, we  would say that their
GCD (Greatest Common divisor) must be 1.

##
## module

A file from which you can usually import some or all items in another file.

It lets you:

   - hide the details of your program's code and focus on its higher-level logic
     (by moving the low-level details into a separate file)

   - re-use functions in many different programs

   - share specific code with other programmers

   - use libraries of functions that other programmers have written

### `builtins`

Module where the built-in names live (e.g. `abs()`).

### `__main__`

Module containing  the statements  executed by the  top-level invocation  of the
interpreter.  Those could be:

   - in a script, if Python was started to run a script
   - typed interactively, if Python was started as a REPL

##
# n
## name

In Python,  a name  is the closest  abstraction to what  other languages  call a
variable.  A name is bound to an object.

## namespace

Mapping from names to  objects.  A mapping can be viewed  as a dictionary, whose
keys are names, and values are objects:

    namespace = {
        name1: 'value1',
        name2: 'value2',
        ...
    }

---

Examples of namespaces are:

   - the set of built-in names (e.g. functions such as `abs()`, and exceptions)
   - the global names in a module
   - the local names in a function
   - the set of attributes of an object

WRT the last bullet  point, imagine you have 2 bikes objects,  each with its own
`color` attribute.  You could access those attributes with sth like:

    red_bike.color
    blue_bike.color

Even though  the attributes  are named  the same, there  would be  no confusion,
because each of them is in a separate namespace (`red_bike` vs `blue_bike`).
And we use the dot operator to walk into each namespace.

---

A namespace is useful to organize names and avoid conflicts.
A namespace  can contain other namespaces  (just like the value  in a dictionary
can itself be a nested dictionary).

For example:

    from mall.floor2.restaurant import meal

In this `import` statement, `mall` is used as a namespace.
Inside, we walk into the `floor2` namespace (again using the dot operator).
Then, we walk into the `restaurant` namespace, and finally we import `meal` from
the latter.

This hierarchy  of namespaces is  useful, because it  gives more meaning  to the
code,  and  it makes  it  easier  to avoid  conflicts;  you  could have  a  name
`employee`  in the  `mall`  namespace  *and* in  the  `restaurant` one,  without
raising any error, and without one shadowing the other.

## None

Keyword used to define a null value, or no value at all.

The `get()` method returns `None` when you ask for the value associated to a key
in a dictionary from which the key is absent.

A user-defined function returns `None`,  unless it contains a `return` statement
which returns another value.

---

In a boolean context, you probably want to avoid `None`.

If you don't, it will evaluate to `False`, but it doesn't mean the same thing:

   - `None` means that we don't have any information ("I don't know")
   - `False` means that we *do* have an information: it's false (whatever "it" is)

If you need to  test an expression which can evaluate to  `None`, you might want
to handle the latter as a special case before.

##
# o
## object

Any data with state (attributesor or value) and defined behavior (methods).

It is instantiated from a class, and has an ID, a type, as well as a value.

##
## overloading
### operator overloading

Some operators can represent different operations depending on the type of their
operands.  We say that those operators are overloaded.

For example, if `+` is surrounded by numbers, it performs an arithmetic addition:

    >>> 1 + 2
    3

But if it's surrounded by sequences, it performs a concatenation:

    >>> [1] + [2]
    [1, 2]

##
# p
## package

Directory which contains the special file `__init__.py`.
What matters for a package is the existence of the latter file, not its contents.

It provides a higher level organizational structure above a module (which itself
is above items such as functions and classes): it lets you group modules.

For example, consider this layout where 3 modules are grouped inside a `util` package:

    $ tree -v example/
    example/
    ├── core.py
    ├── run.py
    └── util
        ├── __init__.py
        ├── db.py
        ├── math.py
        └── network.py

Without this package, the layout would be:

    $ tree -v example/
    example/
    ├── core.py
    ├── db.py
    ├── math.py
    ├── network.py
    └── run.py

The first layout makes it easier to understand the purpose of the modules.
In particular, it makes it explicit that the `db.py`, `math.py` and `network.py`
modules provide *utilities* for various tasks  (interact with a db, do some math
computations, send/receive data on a network).

Together, they form a utility library.

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
## PEP

Python Enhancement Proposal.

A document that describes a newly propose feature.

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
## PyPI

Where  the  Python  international  community maintains  a  body  of  third-party
libraries, tailored to specific needs.

## Pythonic

Your code is Pythonic if it uses the Python language how it's meant to.

In practice, it often means using common idioms.

For example, in Python we can iterate over items in a list directly:
```python
for piece in food:
    print(piece)
```
If  you come  from another  language  where that's  not possible,  you might  be
tempted to write this instead:
```python
for i in range(len(food)):
    print(food[i])
```
It works, but it's not Pythonic because it does not use the previous idiom.

##
# q
## qualified name

A dotted name  showing the “path” from  a module's global scope  to a class,
function or method defined in that module.

For example:
```python
class C:
     class D:
         def meth(self):
             pass
```
    ┌────────┬────────────────┐
    │ object │ qualified name │
    ├────────┼────────────────┤
    │ meth() │ C.D.meth       │
    ├────────┼────────────────┤
    │ D      │ C.D            │
    ├────────┼────────────────┤
    │ C      │ C              │
    └────────┴────────────────┘

See: <https://peps.python.org/pep-3155/>

##
# s
## scope

Textual region  of a  Python program  where a  namespace is  directly accessible
(i.e. for  which you don't  need to use qualified  names).  Such a  namespace is
said to be "tied" to the scope.

A namespace contains names (aka symbols) that you can use in your code.
A scope determines from which namespace you can use unqualified names.

On any  given line, there  are between  3 and 4  nested scopes searched  in this
order whenever Python needs to find a name:

   - the local scope which contains local names (those can be the names in the
     innermost function, if we are in a function, or the same names as in the
     global scope)

   - the enclosing scopes of enclosing functions, if any, which are searched
     from the nearest one to the furthest  one (they contain names which  are
     simultaneously non-local and non-global)

   - the global scope which contains the current module's names
   - the built-in scope wich contains the builtin names (e.g. `abs()`)

Mnemonic: LEGB for "local", "enclosing", "global", "built-in".

## sequence

An iterable which supports efficient  element access using *integer* indices via
the  `__getitem__()`  special method,  and  defines  a `__len__()`  method  that
returns its length.

Some built-in sequence types are `list`, `str`, `tuple`, and `bytes`.
A set is not a sequence.

Note  that  `dict`  also  supports   `__getitem__()`  and  `__len__()`,  but  is
considered a  mapping rather than a  sequence because the lookups  use arbitrary
immutable keys rather than integers.

##
## set

Unordered collection of immutable and unique objects.

Contrary to a list or a tuple  which are surrounded by resp. square brackets and
parentheses, a set is surrounded by curly brackets.

              v                v
    >>> set = {1, 2, 3, 1, 2, 3}
    >>> print(set)
    {1, 2, 3}

Don't conflate a set with a dictionary.
In a set, there is no colon separating a key from its value:

                   v
    >>> dict = {'a': 1}
    >>> set = {'a'}

Also, contrary to a dictionary (and a list), a set is not ordered.

    >>> s = {'a', 'b', 'c'}
    >>> print(s)
    {'c', 'a', 'b'}

### difference

The difference between 2 sets A and B is the set of all items which are included
in A *but not* in B.

$$A - B = \{x: x \in A \land x \notin B\}$$

### intersection

The intersection  between 2  sets A  and B  is the  set of  all items  which are
included in A *and* in B.

$$A \cap B = \{x: x \in A \land x \in B\}$$

### union

The union between 2 sets A and B is the set of all items which are included in A
*or* in B.

$$A \cup B = \{x: x \in A \lor x \in B\}$$

##
## string

Immutable sequence of Unicode code points.

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

A tuple usually contains a heterogeneous  sequence of items, and is accessed via
unpacking  or indexing.   In contrast,  a  list usually  contains a  homogeneous
sequence of items and is iterated over.

A tuple  can be used  in various contexts,  but is well-suited  for mathematical
vectors.

##
# u
## UTF-8

Variable-length  character encoding,  capable of  encoding all  possible Unicode
code points.

##
# v
## virtual environment

Isolated  Python environment,  which  is created  by a  directory  with all  the
necessary executables to use the packages that  a Python project needs, and by a
modified  shell  environment  in  which  the  PATH  is  updated  so  that  those
executables are invoked instead of the ones from the system.

This solves the  issue of working on  multiple projects at the  same time, which
require incompatible dependencies/libraries.
