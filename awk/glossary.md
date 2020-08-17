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
# b
## bracket expression

A regex operator matching  any one of the characters that  are enclosed inside a
pair of square brackets:

    [aeiou]

In other literature,  you may see a  bracket expression referred to  as either a
character set, a character class, or a character list.
In Vim, it's referred to as a collection.

## BRE vs ERE

Basic and Extended Regular Expression.

They are two variations on the syntax of a pattern.

By default:

   - sed (and grep) uses the BRE syntax
   - Vim uses a syntax very similar to BRE
   - Gawk uses a superset of ERE

The only  difference between BRE  and ERE  is in the  behavior of a  few special
characters: `?`, `+`, `()`, `{}`, and `|`.
With  BRE syntax,  these  characters  do not  have  any  special meaning  unless
prefixed with a backslash.
While with ERE  syntax, it's reversed: these characters are  special unless they
are prefixed with a backslash.

##
# c
## character class

Named classes of characters which are predefined within bracket expressions.

---

This terminology was defined in a POSIX standard.
Prior  to  that,  “character  class”  referred to  what  we  call  now  “bracket
expression”; this old terminology is still used in various documentations.

### `[:alnum:]`

Alphanumeric  characters: `[:alpha:]`  and `[:digit:]`;  in the  ‘C’ locale  and
ASCII character encoding, this is the same as `[0-9A-Za-z]`.

### `[:alpha:]`

Alphabetic characters: `[:lower:]` and `[:upper:]`; in the ‘C’ locale and
ASCII character encoding, this is the same as `[A-Za-z]`.

### `[:blank:]`

Blank characters: space and tab.

### `[:cntrl:]`

Control characters.
In ASCII, these characters have octal codes 000 through 037, and 177 (DEL).
In other character sets, these are the equivalent characters, if any.

### `[:digit:]`

0 1 2 3 4 5 6 7 8 9

### `[:graph:]`

Graphical characters: `[:alnum:]` and `[:punct:]`.

### `[:lower:]`

Lower-case letters; in the ‘C’ locale  and ASCII character encoding, this is all
letter a b c d e f g h i j k l m n o p q r s t u v w x y z.

### `[:print:]`

Printable characters: `[:alnum:]`, `[:punct:]`, and space.

### `[:punct:]`

Punctuation characters; in the ‘C’ locale and ASCII character encoding, this is
! " # $ % & ’ ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ‘ { | } ~.

### `[:space:]`

Space characters:  in the ‘C’ locale,  this is tab, newline,  vertical tab, form
feed, carriage return, and space.

### `[:upper:]`

Upper-case letters: in the ‘C’ locale and  ASCII character encoding, this is A B
C D E F G H I J K L M N O P Q R S T U V W X Y Z.

### `[:xdigit:]`

Hexadecimal digits: 0 1 2 3 4 5 6 7 8 9 A B C D E F a b c d e f.

###
## collating symbol

Sequence of characters that should be treated as a unit.
It consists of the characters bracketed by `[.` and `].`.
It must appear inside the square brackets of a bracket expression.

---

Example:

When  matching or  sorting string  data  in the  czech locale,  the sequence  of
characters ‘ch’ must be treated as a single character:

    $ sudo locale-gen cs_CZ.UTF-8
    $ LC_ALL=cs_CZ.UTF-8 grep '^[[.ch.]]o$' <<<'cho'
    cho~

It comes after ‘h’ but before ‘i’:

    $ LC_ALL=cs_CZ.UTF-8 grep '^[h-i]o$' <<<'cho'
    cho~

See here for more info:
<https://unix.stackexchange.com/questions/254811/what-does-ch-mean-in-a-regex>

---

Here's how the book ‘Sed & Awk’ introduces the concept of collation:

   > Additionally, the standard provides for sequences of characters that should be
   > treated as a single unit when matching and collating (sorting) string data.
   > POSIX also changed what had been common terminology.
   > What we've been calling a "character  class" is called a "bracket expression" in
   > the POSIX standard.

Page 56 of the pdf.

## constant

There are 3 kinds of constants:

   - string
   - numeric
   - regex (`/pat/`)

##
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
## cycle

Application of all commands in a sed script to an input line in the pattern space.
There are as many cycles as there are input lines passed to the sed process.

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

## equivalence class

Set of characters that should be considered equivalent, such as e and è.
It consists of a named element from the locale, bracketed by `[=` and `=]`.
It must appear inside the square brackets of a bracket expression.

## evaluation

Process through which a programming language (such as awk):

   1. interprets an expression (according to its particular rules of precedence
      and of association)

   2. computes it

   3. from the result, produces a new value of a given type (numerical, string,
      logical - true / false, function, ...)

## expression

A combination of one or more:

   - arrays
   - constants
   - functions
   - operators
   - variables

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
# p
## pattern space

Temporary buffer  where a  single line of  input is held  while the  sed editing
commands are applied.

Its contents are dynamic; they change after every statement in the sed script.
So, a previous command may have an impact on the next one.
See our pitfall about replacing `three` with `two`, and `two` with `one`.

As soon as all  the commands have been applied to the  pattern space, the latter
is written on sed's standard output.
Then,  the next  input line  is copied  in the  pattern space,  and the  process
repeats itself.

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

