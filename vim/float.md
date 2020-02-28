# Which function must I invoke to create a new empty unnamed buffer?

    nvim_create_buf()

## Which arguments does it expect?

    {listed}, {scratch}

When `{listed}` is true, Nvim will set `'buflisted'`.
When `{scratch}` is true, Nvim will create a scratch buffer:

    :setlocal buftype=nofile
    :setlocal bufhidden=hide
    :setlocal noswapfile

See `:h special-buffers /scratch`.

## Which value does it return?

The buffer handle, or 0 for an error.

##
# What is a float?

A window that is  drawn above the split layout, at some  anchor position in some
other window.

It's displayed on top of normal windows.

## How is it useful?

It can be used to implement a simple widget, such as a tooltip displayed next to
the cursor.

##
## Which function must be invoked to create one?

    nvim_open_win()

### What are the 3 arguments it expects?

    {buffer}, {enter}, {config}
     │         │
     │         └ enter the window (make it the current window)
     └ buffer to display, or 0 for current buffer

#### What are the 5 mandatory keys in the `{config}` argument?

   - `width`
   - `height`
   - `relative`
   - `row`
   - `col`

##### When are `row` and `col` not mandatory?

When `relative` is `win` and you include the `bufpos` key in `{config}`.

###### If omitted, which value do they default to?

Respectively 1 and 0.

###
### Which value does it return?

The window handle, or 0 for an error.

####
### What are the 3 information necessary and sufficient to entirely describe the position of a float?

   - its width
   - its height
   - the coordinates of one of its corner

#### Which corner's coordinates are described by default?

The upper-left one.

##### How to choose a different corner?

Use the `anchor` key.  It accepts these 4 values:

   - 'NW' (default)
   - 'NE'
   - 'SE'
   - 'SW'

##### How to specify its coordinates?

Use the `row` and `col` key.

#####
##### Coordinates only make sense in a given frame.  How to set its origin to
###### the cursor?

In `{config}`, include this key-value pair:

    'relative': 'cursor'

###### the upper-left cell of the main screen grid?

    'relative': 'editor'

###### the upper-left cell of the current window?

    'relative': 'win'

###### the upper-left cell of an arbitrary window?

In `{config}`, include these 2 key-value pairs:

    'relative': 'win'
    'win': 1234
           ^^^^
           window ID

Don't conflate the `win` *key*, with the `win` *value* of the `relative` key.

###### a cell containing an arbitrary character from a buffer currently displayed?

    'relative': 'win'
    'bufpos': [12, 34]
               │   │
               │   └ 0-indexed column position
               └ 0-indexed line address

---

Note that `'row': 0,  'col': 0` and `'bufpos': [0, 0]` do not  describe the same
cell.

`row: 0`  describes the  first  line in  which  Nvim can  draw  **any type**  of
character (this includes the tabline).   Same thing for `col: 0` which describes
the first column in which Nvim can draw (including the signcolumn).

OTOH, `'bufpos': [0,0]`  describes the cell on  the first line and  in the first
column in which Nvim can draw a character in a **buffer**.
IOW, the line  0 is the first line  in a buffer (which will always  be below the
tabline), and the column 0 is the first column in a buffer (which will always be
after the signcolumn).

---

Also, if you specify  a column position which does not  match a buffer character
because the line is  shorter, Nvim will use the column of  the last character on
the line.

##
### How to change the default color of the background
#### in all floats?

    :hi link NormalFloat Search
                         ^^^^^^
                         arbitrary HG

#### in a given float?

    call setwinvar(winid, '&winhighlight', 'NormalFloat:Search')
                   ^^^^^
                   ID of the float

##
### How to hide/disable various visual features (`EndOfBuffer`, signcolumn, ...)?

In `{config}`, include this key-value pair:

    'style': 'minimal'

It also disables `'number'`, `'cursorline'`, `'spell'`, `'list'`, ...

#### When should I do it?

When displaying a temporary float where the text should not be edited.

##
### How to prevent a float from being focusable with interactive commands?

In `{config}`, include this key-value pair:

    'focusable': v:false

#### How to focus such a float in a script?

    call nvim_set_current_win(1234)
                              ^^^^
                              window ID of the float

###
## How to reconfigure the settings of a float?

    call nvim_win_set_config(0, {config})
                             │   │
                             │   └ dictionary with same keys as in `nvim_open_win()`
                             └ current window; can be replaced with arbitrary window ID

`nvim_win_set_config()` can also be invoked to convert a normal window into a float.

### What happens if I set a float with some option key, but I omit to reset it when reconfiguring the float?

It keeps its original value.

##
## How to close a float?  (2)

Use `nvim_win_close()` or `:close`.

