# a
## associativity (operator)

Property of  an operator which determines  how operators of the  same precedence
are grouped (with their operands) in the absence of parentheses.

If an operand is both preceded and followed by operators (for example, `^ 3 ^`),
and those operators have equal precedence, then the operand may be used as input
to two different operations.
The choice  of which operations  to apply the operand  to, is determined  by the
*associativity* of the operators.

### What type of associativity can an operator have?

Operators may be:

   - associative       (the operations can be grouped arbitrarily)
   - left-associative  (the operations are grouped from the left)
   - right-associative (the operations are grouped from the right)

   - non-associative
     (operations cannot be chained,
     often because the output type is incompatible with the input types)

The associativity and precedence of an operator is a part of the definition of a
programming language;  different languages may have  different associativity and
precedence for the same type of operator.

### Why must operators with the same precedence have the same associativity?

To prevent  cases where operands would  be associated with two  operators, or no
operator at all.

---

Suppose that `/` was right-associative, while `*` was still left-associative.
In which order should the operators in this expression be grouped?

    1 * 2 / 3

There would be an ambiguity.
That's why `*` and `/` which have  the same precedence, can *not* have different
associativities.

##
# c
## constant

There are 3 kinds of constants:

   - string
   - numeric
   - regex (`/pat/`)

## control flow

Order  in which  individual statements,  instructions  or function  calls of  an
imperative program are executed or evaluated.

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

Operator performing a regex comparison:

   - `~`
   - `!~`

## relational operator

Operator performing a numeric or lexicographic comparison:

   - `==`
   - `!=`
   - `<`
   - `>`
   - `<=`
   - `>=`

## comparison operator

Relational or matching operator.

##
## output record

Output from an entire print statement.

> The output from an entire print statement is called an output record.
> Each print statement outputs one output record, and then outputs a string called
> the output record separator (or ORS).
> The initial value of ORS is the string "\n" (i.e., a newline character).
> Thus, each print statement normally makes a separate line.

Source: A User’s Guide for GNU Awk Edition 4.2

---

Does that mean  that the notion of  an output record is  fundamentally linked to
the `print` statement?

Yes, and there's nothing weird about that.
Awk doesn't print anything on its output  by default; you have to use `print` or
`printf` for awk to have an output.

##
# r
## record

Awk splits automatically the input into records.
By default, it considers a newline as a separator between 2 consecutive records.

## regular expression

A combination of operators and metacharacters, which can be surrounded by either
slashes or double quotes.

## rule

A pattern followed by an action.

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

