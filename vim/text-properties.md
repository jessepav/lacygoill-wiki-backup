# Introduction

A text property can be attached to some text in a buffer.
It will move with the text:

   - when inserting/deleting whole lines above the text property
   - when inserting/deleting text inside the line right before the text property
   - when inserting/deleting text inside the text property itself
     (it will increase/decrease in size)

The main use for text properties is to highlight text.
This can be seen as a replacement for syntax highlighting.
Instead of  defining patterns to  match the text, the  highlighting is set  by a
script, possibly using the output of an external parser.
This only needs to be done once,  not every time when redrawing the screen, thus
can be much faster, after the initial cost of attaching the text properties.

Text properties can also be used for other purposes to identify text.
For example,  add a text property  on a function name,  so that a search  can be
defined to jump to the next/previous function.

A text  property is  attached at  a specific  line and  column, has  a specified
length, and can span multiple lines; it has these entries:

    ┌──────┬─────────────────────────┐
    │ id   │ arbitrary number        │
    ├──────┼─────────────────────────┤
    │ type │ name of a property type │
    └──────┴─────────────────────────┘

## Property Types

A text property normally  has the name of a property type,  which defines how to
highlight the text.  The property type can have these entries:

    ┌────────────┬──────────────────────────────────────────────────────────┐
    │ highlight  │ name of the highlight group to use                       │
    ├────────────┼──────────────────────────────────────────────────────────┤
    │ combine    │ when omitted or TRUE, the text property highlighting is  │
    │            │ combined with any syntax highlighting; when FALSE the    │
    │            │ text property highlighting replaces the syntax           │
    │            │ highlighting                                             │
    ├────────────┼──────────────────────────────────────────────────────────┤
    │ priority   │ when properties overlap, the one with the highest        │
    │            │ priority will be used.                                   │
    ├────────────┼──────────────────────────────────────────────────────────┤
    │ start_incl │ when TRUE, an insert at resp. the start and end position │
    │ end_incl   │ will be included in the text property                    │
    └────────────┴──────────────────────────────────────────────────────────┘

## Example

Suppose line 11 in a buffer has this text (excluding the indent):

    The number 123 is smaller than 4567.

To highlight the numbers in this text:

    call prop_type_add('number', {'highlight': 'Constant'})
    call prop_add(11, 12, {'length': 3, 'type': 'number'})
    call prop_add(11, 32, {'length': 4, 'type': 'number'})

Try inserting  or deleting  lines above  the text,  you will  see that  the text
properties stick to the text, thus the line number is adjusted as needed.

Setting `start_incl`  and `end_incl`  is useful when  white space  surrounds the
text, e.g. for a function name.
Using  false  is  useful when  the  text  starts  and/or  ends with  a  specific
character, such as the quote surrounding a string.

    func FuncName(arg) ~
         ^------^
    property with "start_incl" and "end_incl" set

    var = "text"; ~
          ^----^
    property with "start_incl" and "end_incl" NOT set

Nevertheless, when text  is inserted or deleted  the text may need  to be parsed
and the text properties updated.  But this can be done asynchronously.

##
# Functions
## `prop_type_add({name}, {props})`

Define a new property type `{name}`.

If a property type with this name already exists an error is given.
`{props}` is a dictionary with these optional entries:

    ┌────────────┬─────────────────────────────────────────────────┐
    │ bufnr      │ define the property only for this buffer; this  │
    │            │ avoids name collisions and automatically        │
    │            │ clears the property types when the buffer is    │
    │            │ deleted.                                        │
    ├────────────┼─────────────────────────────────────────────────┤
    │ highlight  │ name of highlight group to use                  │
    ├────────────┼─────────────────────────────────────────────────┤
    │ priority   │ when a character has multiple text              │
    │            │ properties the one with the highest priority    │
    │            │ will be used; negative values can be used, the  │
    │            │ default priority is zero                        │
    ├────────────┼─────────────────────────────────────────────────┤
    │ combine    │ when TRUE, combine the highlight with any       │
    │            │ syntax highlight; when omitted or FALSE syntax  │
    │            │ highlight will not be used                      │
    ├────────────┼─────────────────────────────────────────────────┤
    │ start_incl │ when TRUE, inserts at the start position will   │
    │            │ be included in the text property                │
    ├────────────┼─────────────────────────────────────────────────┤
    │ end_incl   │ when TRUE, inserts at the end position will be  │
    │            │ included in the text property                   │
    └────────────┴─────────────────────────────────────────────────┘

## `prop_type_delete({name} [, {props}])`

Remove the text property type `{name}`.
When text properties using  the type `{name}` are still in  place, they will not
have an effect and can no longer be removed by name.

`{props}` can contain a `bufnr` item.
When it is  given, delete a property  type from this buffer instead  of from the
global property types.

When text property type `{name}` is not found, there is no error.

## `prop_type_change({name}, {props})`

Change properties of an existing text property type.
If a property with this name does not exist, an error is given.
The `{props}` argument is just like `prop_type_add()`.

## `prop_type_get([{name} [, {props}])`

Returns the properties of property type `{name}`.
This is a dictionary with the same entries as was given to `prop_type_add()`.
When the property type `{name}` does not exist, an empty dictionary is returned.

`{props}` can contain a `bufnr` item.
When it is given, use this buffer instead of the global property types.

## `prop_type_list([{props}])`

Returns a list with all property type names.

`{props}` can contain a `bufnr` item.
When it is given, use this buffer instead of the global property types.

##
## `prop_add({lnum}, {col}, {props})`

Attach a text property at position `{lnum}, {col}`.
`{col}` is counted in bytes, use one for the first column.
If `{lnum}` is invalid an error is given.
If `{col}` is invalid an error is given.

`{props}` is a dictionary with these entries:

    ┌──────────┬────────────────────────────────────────────────┐
    │ type     │ name of the text property type                 │
    ├──────────┼────────────────────────────────────────────────┤
    │ bufnr    │ buffer to add the property to; when omitted    │
    │          │ the current buffer is used                     │
    ├──────────┼────────────────────────────────────────────────┤
    │ length   │ length of text in bytes, can only be used      │
    │          │ for a property that does not continue in       │
    │          │ another line; can be zero                      │
    ├──────────┼────────────────────────────────────────────────┤
    │ end_lnum │ line number for the end of text                │
    ├──────────┼────────────────────────────────────────────────┤
    │ end_col  │ column just after the text; not used when      │
    │          │ "length" is present; when {col} and "end_col"  │
    │          │ are equal, and "end_lnum" is omitted or equal  │
    │          │ to {lnum}, this is a zero-width text property  │
    ├──────────┼────────────────────────────────────────────────┤
    │ id       │ user defined ID for the property; when omitted │
    │          │ zero is used                                   │
    └──────────┴────────────────────────────────────────────────┘

All entries except `type` are optional.

It is an error when both `length` and `end_lnum` or `end_col` are given.
Either  use  `length` or  `end_col`  for  a property  within  one  line, or  use
`end_lnum` and `end_col` for a property that spans more than one line.
When neither `length` nor `end_col` are given, the property will be zero-width.
That means it will not be highlighted but  will move with the text, as a kind of
mark.
The property can  end exactly at the  last character of the text,  or just after
it.
In the last case,  if text is appended to the line, the  text property size will
increase, also when the property type does not have `end_incl` set.

`type` will first be looked up in the buffer the property is added to.
When not found, the global property types are used.
If not found an error is given.

## `prop_remove({props} [, {lnum} [, {lnum-end}]])`

Remove a matching text property from line `{lnum}`.
When `{lnum-end}` is  given, remove matching text properties  from line `{lnum}`
to `{lnum-end}` (inclusive).
When `{lnum}` is omitted remove matching text properties from all lines.

`{props}` is a dictionary with these entries:

    ┌───────┬─────────────────────────────────────────────────┐
    │ id    │ remove text properties with this ID             │
    ├───────┼─────────────────────────────────────────────────┤
    │ type  │ remove text properties with this type name      │
    ├───────┼─────────────────────────────────────────────────┤
    │ both  │ "id" and "type" must both match                 │
    ├───────┼─────────────────────────────────────────────────┤
    │ bufnr │ use this buffer instead of the current one      │
    ├───────┼─────────────────────────────────────────────────┤
    │ all   │ when TRUE, remove all matching text properties, │
    │       │ not just the first one                          │
    └───────┴─────────────────────────────────────────────────┘

A property matches when either `id` or `type` matches.
If buffer `bufnr` does not exist you get an error message.
If buffer `bufnr` is not loaded then nothing happens.

Returns the number of properties that were removed.

## `prop_clear({lnum} [, {lnum-end} [, {props}]])`

Remove all text properties from line `{lnum}`.

When  `{lnum-end}` is  given,  remove  all text  properties  from  line `{lnum}`  to
`{lnum-end}` (inclusive).

When `{props}` contains a `bufnr` item  use this buffer, otherwise use the current
buffer.

## `prop_list({lnum} [, {props}])`

Return a List with all text properties in line `{lnum}`.

When `{props}` contains  a `bufnr` item, use this buffer  instead of the current
buffer.

The properties are ordered by starting column and priority.
Each property is a Dict with these entries:

    ┌────────┬────────────────────────────────────────────┐
    │ col    │ starting column                            │
    ├────────┼────────────────────────────────────────────┤
    │ length │ length in bytes, one more if line break is │
    │        │ included                                   │
    ├────────┼────────────────────────────────────────────┤
    │ id     │ property ID                                │
    ├────────┼────────────────────────────────────────────┤
    │ type   │ name of the property type, omitted if      │
    │        │ the type was deleted                       │
    ├────────┼────────────────────────────────────────────┤
    │ start  │ when TRUE, property starts in this line    │
    │ end    │ when TRUE, property ends in this line      │
    └────────┴────────────────────────────────────────────┘

When `start` is zero,  the property started in a previous  line, the current one
is a continuation.
When `end` is zero, the property continues in the next line.
The line break after this line is included.

## `prop_find({props} [, {direction}])`

Search for a text property as specified with `{props}`:

    ┌───────────┬────────────────────────────────────────┐
    │ id        │ property with this ID                  │
    ├───────────┼────────────────────────────────────────┤
    │ type      │ property with this type name           │
    ├───────────┼────────────────────────────────────────┤
    │ bufnr     │ buffer to search in; when present a    │
    │           │ start position with `lnum` and `col`   │
    │           │ must be given; when omitted the        │
    │           │ current buffer is used                 │
    ├───────────┼────────────────────────────────────────┤
    │ lnum      │ start in this line (when omitted start │
    │           │ at the cursor)                         │
    ├───────────┼────────────────────────────────────────┤
    │ col       │ start at this column (when omitted     │
    │           │ and `lnum` is given: use column 1,     │
    │           │ otherwise start at the cursor)         │
    ├───────────┼────────────────────────────────────────┤
    │ skipstart │ do not look for a match at the start   │
    │           │ position                               │
    └───────────┴────────────────────────────────────────┘

`{direction}` can be `f` for forward and `b` for backward.
When omitted forward search is performed.

If  a  match  is found  then  a  Dict  is  returned  with the  entries  as  with
`prop_list()`, and additionally an `lnum` entry.
If no match is found then an empty Dict is returned.

##
# When text changes

Vim will do its best to keep the text properties on the text where it was
attached.  When inserting or deleting text the properties after the change
will move accordingly.

When text is deleted and a text property no longer includes any text, it is
deleted.  However, a text property that was defined as zero-width will remain,
unless the whole line is deleted.

When a buffer is unloaded, all the text properties are gone.  There is no way
to store the properties in a file.  You can only re-create them.  When a
buffer is hidden the text is preserved and so are the text properties.  It is
not possible to add text properties to an unloaded buffer.

When using replace mode, the text properties stay on the same character
positions, even though the characters themselves change.

To update text properties after the text was changed, install a callback with
`listener_add()`.  E.g, if your plugin does spell checking, you can have the
callback update spelling mistakes in the changed text.  Vim will move the
properties below the changed text, so that they still highlight the same text,
thus you don't need to update these.

## Text property columns are not updated:

- When setting the line with |setline()| or through an interface, such as Lua,
  Tcl or Python.  Vim does not know what text got inserted or deleted.

- With a command like `:move`, which takes a line of text out of context.

##
# Todo
## The concept of 'id' is confusing.

Document that:

   - a property type does *not* have an id

   - a property *has* an id

   - an id is only useful for the functions `prop_add()`, `prop_remove()`, `prop_list()`, `prop_find()`

   - an id is not unique to a property; you can have multiple properties with the same id;
     think of it as a namespace, rather than an identifier

## Study what happens when we try to remove a property type while some properties are still using it.

Update: It seems the highlighting of a property whose type has been removed persists.
But only for a  short time; e.g. if you add an empty  line above, then undo, the
highlighting disappears.

##
## Document
### the meaning of `'all': v:true` for `prop_remove()`.

Hint: it's similar to `:h :s_g`.
Without, if there are several matching text properties on a line, only the first
one is removed; with it, *all* matching text properties are removed.

### that text properties are lost after a `:move` command.

That's  because  internally, Vim  first  copies  the  line(s), then  remove  the
original one(s).  And the copy do(es) not inherit the text properties.
As a workaround, you can move the neighbor line(s).

To move the range of lines, from the  current one down to the next `p` ones, `q`
lines downward, execute this Ex command:

    +p+1,+p+qm-|+

To move the range of lines, from the  current one down to the next `p` ones, `q`
lines upward, execute this Ex command:

    -q,-m.+p|-q

As an example, consider this text file in `/tmp/file`:

    The number 12 is smaller than 345.
    The number 6789 is bigger than 1234.
    The number 56789 is smaller than 123456.
    aaa
    bbb
    ccc
    ddd
    eee

And this script in `/tmp/vim.vim`:

    call prop_type_add('number', {'highlight': 'Search'})
    call prop_add(1, 12, {'length': 2, 'type': 'number'})
    call prop_add(1, 31, {'length': 3, 'type': 'number'})
    call prop_add(2, 12, {'length': 4, 'type': 'number'})
    call prop_add(2, 32, {'length': 4, 'type': 'number'})
    call prop_add(3, 12, {'length': 5, 'type': 'number'})
    call prop_add(3, 34, {'length': 6, 'type': 'number'})

Now, start Vim like this:

    vim -Nu NONE -S /tmp/vim.vim /tmp/file

To move the 3 lines containing numbers 4 lines downward, execute this Ex command
while on the first line of the range of number lines:

    +2+1,+2+4m-|+

And to move it again 3 lines upward,  execute this Ex command while on the first
line of the range of number lines:

    -3,-m.+2|-3

See: <https://github.com/vim/vim/issues/5648#issuecomment-587041255>

### that when 2 text properties conflict with each other and have the same priority, the first one wins.

First in the chronological meaning of the term.

### when we should use text-properties.

As an example,  we use them in `vim-quickhl`,  as well as for the  `]e` and `[e`
mappings, and in `~/.vim/pack/mine/opt/lg-lib/tools/ansi.vim`.

More generally,  I think text  properties are useful when  the text you  want to
highlight (or  mark) can't be directly  described with a regex.   Or rather, the
regex you might use would not describe the text itself (because it does not have
a particular  structure), but its  location; that is,  the regex refers  to some
temporary notion  (like the current  cursor position), which might  become stale
whenever the buffer changes.

---

You might be tempted to replace ad-hoc  syntax plugins which are used for static
buffers (i.e. buffers which we read but don't edit) with text properties.

But how would you parse the text?  With a while loop?  It will be slow.
Also, if  you don't edit  the buffer, then  the main benefit  of text-properties
disappears.

Update: Parsing might be the wrong way to look at the issue.
If you know in advance the lines you're  going to write in the buffer, you might
compute the positions of the texts you need to highlight.  No parsing needed...

