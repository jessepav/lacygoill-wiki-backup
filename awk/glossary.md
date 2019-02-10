# c
## constant

There are 2 kinds of constants:

   - string
   - numerical

## control flow

Order  in which  individual statements,  instructions  or function  calls of  an
imperative program are executed or evaluated.

The emphasis  on explicit control  flow distinguishes an  imperative programming
language from a declarative programming language.

<https://en.wikipedia.org/wiki/Control_flow>

## control flow graph

Representation,  using graph  notation, of  all  paths that  might be  traversed
through a program during its execution.

<https://en.wikipedia.org/wiki/Control_flow_graph>

## control flow statement

Within  an  imperative programming  language,  a  control  flow statement  is  a
statement, the execution of which results in  a choice being made as to which of
two or more paths to follow.

Here are a few categories of control flow statements:

   - alternatives (if, if–else,  switch, ...)
   - loops (while, do–while, for, ...)
   - exception handling constructions (try–catch,  ...)

##
# d
## dynamic regex

A regex can be computed by:

   1. evaluating an expression, converted to a string if necessary
   2. using the contents of the evaluated string

A regex computed in this way is called a dynamic regex.

In contrast, a string of characters between  slashes, used as a regex, is called
a *regex constant*.

##
# e
## escape sequence

A string can contain the following escape sequences:

    ┌───────┬──────────────────────────────────┐
    │  \b   │ backspace                        │
    ├───────┼──────────────────────────────────┤
    │  \f   │ form feed                        │
    │       │                                  │
    │       │ ask the printer to eject         │
    │       │ the current page, and continue   │
    │       │ printing on a new page           │
    ├───────┼──────────────────────────────────┤
    │  \n   │ line feed                        │
    ├───────┼──────────────────────────────────┤
    │  \r   │ carriage return                  │
    │       │                                  │
    │       │ position the cursor at the       │
    │       │ beginning of the current line    │
    ├───────┼──────────────────────────────────┤
    │  \t   │ tab                              │
    ├───────┼──────────────────────────────────┤
    │ \123  │ character whose octal code       │
    │       │ is `123`                         │
    ├───────┼──────────────────────────────────┤
    │ \x123 │ character whose hexadecimal code │
    │       │ is `123`                         │
    ├───────┼──────────────────────────────────┤
    │  \\   │ literal backslash                │
    ├───────┼──────────────────────────────────┤
    │  \"   │ literal double quote             │
    └───────┴──────────────────────────────────┘

## expression

A combination of one or more:

   - arrays
   - constants
   - functions
   - operators
   - variables

... which a programming language (such as awk):

   1. interprets (according to its particular rules of precedence and of association)
   2. computes
   3. from the result, produces a new value of a given type
      (numerical, string, logical - true / false, function, ...)

In mathematics, this process is called “evaluation”.

##
# i
## input

Set of all data processed by awk.

##
# o
## unary operator

Operator associating a value to 1 operand.

As an  example, `?` is a  unary regex operator,  and the regex `r?`  matches the
text `r` or an empty text.

## binary operator

Operator associating a value to 2 operands.

As an example, `+`  is a binary arithmetic operator, and the  expression `1 + 2`
produces the number `3`.

##
## matching operator

   - `~`
   - `!~`

## relational operator

   - `==`
   - `!=`
   - `<`
   - `>`
   - `<=`
   - `>=`

## comparison operator

Relational or matching operator.

##
# r
## record

Awk splits automatically the input into records.
By default, it considers a newline as a separator between 2 consecutive records.

## regular expression

It can be either:

   - a combination of operators and metacharacters surrounded by a pair of
     delimiters (typically `/`)

   - a string

##
# s
## statement

This can be a `pattern { action }`, or a command inside an action.

## syntactic sugar

A construction can be considered “syntactic sugar” iff:

   - it simplifies the reading/writing of another syntactic construction

   - its removal wouldn't make the language less expressive, nor would it remove
     any feature of the language


Example1:

    printf  "fmt",  expr-list

is probably syntactic sugar for:

    printf("fmt", expr-list)


Example2:

    my_array[1,2]

is probably syntactic sugar for sth like:

    get_array(my_array, vector(1,2))

And similarly:

    my_array[1,2] = 345

is probably syntactic sugar for sth like:

    set_array(my_array, vector(1,2), 345)

---

The processors of the language (interpreter, preprocessor, compiler, ...) expand
syntactic sugar into more fundamental constructions, before processing the code.
This process is called “desugaring”.

##
# v
## value

A value is an expression whose evaluation can not be reduced to a simpler form.

