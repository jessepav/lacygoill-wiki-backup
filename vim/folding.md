# Options
## What does `'foldlevel'` control?

When set to a number, any fold with  a higher level is closed, and any fold with
a lower level is opened.

### Which normal commands can alter its value?

   - `zM`: reset to 0
   - `zm`: decrease by 1

   - `zR`: reset to max
   - `zr`: increase by 1

---

The commands which can open/close a particular fold, do *not* alter `'foldlevel'`:

   - `zA`
   - `zC`
   - `zO`

   - `za`
   - `zc`
   - `zo`

   - `zv`

### When is it applied?  (3)

When you:

   - load a buffer
   - press `zx` or `zX`
   - add new lines which are detected as a new fold

###
## Which normal commands automatically set `'foldenable'`?  (9)

`zN` and `zi` are meant specifically to set the option (`zi` once out of two).
In addition, any command which creates a fold (`zf`), or closes one or several fold(s):

   - `zc`
   - `zC`

   - `za`
   - `zA`

   - `zm`
   - `zM`

##
## What are the four fold-related options which are not window-local?

   - `'debug'`
   - `'foldclose'`
   - `'foldopen'`
   - `'foldlevelstart'`

### What do they control?

If `'foldclose'` is set  to `all`, a fold is automatically  closed when you move
the cursor outside of it and its level is higher than `'foldlevel'`.

---

`'foldopen'` specifies which types of commands will make Vim open a closed fold,
when they make the cursor move into one.

Its default value is:

    block,hor,mark,percent,quickfix,search,tag,undo
    │     │   │    │       │        │      │   │
    │     │   │    │       │        │      │   └ undo or redo: "u" and CTRL-R
    │     │   │    │       │        │      └ jumping to a tag: ":ta", CTRL-T, etc.
    │     │   │    │       │        └ search for a pattern: "/", "n", "*", "gd", etc.
    │     │   │    │       └ ":cn", ":crew", ":make", etc.
    │     │   │    └ "%"
    │     │   └ jumping to a mark: "'m", CTRL-O, etc.
    │     └ horizontal movements: "l", "w", "fx", etc.
    └ "(", "{", "[[", "[{", etc.

---

`'foldlevelstart'` sets `'foldlevel'` when starting to edit a buffer in a window.

Some useful values are:

    ┌────┬──────────────────────────────────────────────┐
    │ -1 │ the option is ignored                        │
    ├────┼──────────────────────────────────────────────┤
    │ 0  │ all folds are closed                         │
    ├────┼──────────────────────────────────────────────┤
    │ 1  │ most folds are closed (except level-1 folds) │
    ├────┼──────────────────────────────────────────────┤
    │ 99 │ no fold is closed                            │
    └────┴──────────────────────────────────────────────┘

It can be overridden by a modeline or by an autocmd listening to `BufReadPre`.

---

If `'debug'`  is set  to `msg`,  when Vim encounters  an error  while evaluating
`'fde'`, it gives an error message.
If it has the value `throw`, it will also throws an exception and set `v:errmsg`.

###
## `'foldopen'` doesn't work for a command I use in my mapping!

It doesn't apply to commands which are used in a mapping.
Rationale: it gives the user more control over the folds.

Use `zv` or `:norm! zv` in your mapping to get the same effect.

##
# Opening/Closing
## How to close/open
### the current fold?

Use the `zc`/`zo` command.

#### and its parent?

Use `zc`/`zo` twice.

#### and *all* its parents?

Use the `zC`/`zO` command.

###
## How to toggle the current fold?

Use the `za` command.

### What happens if I do this on
#### a nested closed fold?

The oldest parent is opened.
Then, the child of this parent is opened.
Then, its child, and so on; until the current line is visible.

#### a nested opened fold?

It's just toggled (closed, opened, closed, opened...).

###
### How to do it recursively?

Use the `zA` command.

It's equivalent to `zC`  if the current fold is open, or to  `zO` if the current
fold is closed.

##
## When Vim computes the foldlevel of new folded lines, does the new fold get closed or opened?

It depends on `'foldlevel'`.

If  the  new  fold has  a  greater  level  than  `'foldlevel'`, it  gets  closed
automatically; otherwise, it stays open.

    $ vim -Nu NONE -S <(tee <<'EOF'
        setl fdl=1 fml=0 fdm=manual fde=getline(v:lnum)=~#'^#'?'>' .. getline(v:lnum)->matchstr('^#*')->len():'='
        au BufWritePost * setl fdm=expr | eval foldlevel(1) | setl fdm=manual
        %d|sil pu=repeat(['x'], 5)|1
    EOF
    ) /tmp/md.md

    " press:  O # Esc :w  (the fold stays open)
    " press:  O ## Esc :w  (the fold is closed automatically)

---

We set `'fdl'` to 0, so a new fold is always automatically closed for us.

But we also use  some custom code which automatically presses `zv`  for us, so –
in the  end – a new  fold is always automatically  closed iff our cursor  is not
inside.

##
# Motions
## Where do the default `]z` and `[z` commands make the cursor jump?

Resp. to the start and end of the current fold.
If the cursor is already at the  start/end of the current fold, the cursor jumps
to the start/end of the containing fold.

### What about `zj` and `zk`?

Resp. to the start of the next fold, and to the end of the previous fold.

### What about our custom `]z` and `[z`?

`]z` jumps to:

   - the end of the current fold
   - the end of the next fold
   - right above the start of the next nested fold

Whichever is the nearest.

Exception: when the  folding method is 'marker',  the cursor does not  move on a
line containing a folding marker; it moves right above.

---

`[z` jumps to:

   - right below the start of the current fold
   - right below the start of the previous fold
   - right below the end of the previous nested fold

Whichever is the nearest.

###
### When I use the default `zk` command to move to the end of the previous fold, Vim skips some ends of folds!

No, it does not.

You're probably confused by the nesting foldexpr, which we don't use often.

Suppose you have this markdown file while you're using the nesting foldexpr:

    line address  foldcolumn  text
    1             -           # a
    2             |
    3             |           a
    4             |
    5             |-          ## aa
    6             ||
    7             ||          aa
    8             ||
    9             |-          ##
    10            -           # b
    11            |
    12            |           b
    13            |
    14            |-          ## bb
    15            ||
    16            ||          cursor is on this line

You execute `:norm! zk` to move to the previous end of fold.
You probably expect your cursor to jump on line 13, but in reality it jumps on line 9.
line 13 is *not* the end of a fold; it belongs to the level-1 fold starting on line 10.

##
# Enabling/Disabling Creating/Deleting
## How to enable/disable/toggle folding?

   - `zN`

   - `zn`

   - `zi`

Technically, these commands set/reset/toggle `'foldenable'`.

### What's one pitfall of temporarily disabling folding?

The view may be altered.

    $ vim -Nu NONE -S <(tee <<'EOF'
        setl fml=0 fdm=expr fde=getline(v:lnum)=~#'^#'?'>1':'='
        %d|sil pu=repeat(['#'], &lines)+['#']+repeat([''], &lines)+['#', '']
        norm! zo
    EOF
    ) /tmp/md.md

    " press:  zizi
    " the last line of the file is no longer the last line of the screen

If that's an issue, save and restore the view:

    let view = winsaveview()
    let fen_save = &l:fen
    ...
    let &l:fen = fen_save
    call winrestview(view)

---

In a script, it seems the issue is not always triggered:

    $ vim -Nu NONE -S <(tee <<'EOF'
        setl fml=0 fdm=expr fde=getline(v:lnum)=~#'^#'?'>1':'='
        %d|sil pu=repeat(['#'], &lines)+['#']+repeat([''], &lines)+['#', '']
        norm! zo
    EOF
    ) /tmp/md.md

    " the view is preserved
    :setl nofen | setl fen

    " the view is altered
    :setl nofen | exe 'norm! "' | setl fen
                       ^--^
                       a `:norm` command is necessary to trigger the issue in a script;
                       maybe other commands trigger the issue too...

I suspect that when Vim executes scripted commands, it doesn't update the view.
But it probably does when the script contains an interactive command (e.g. `:h :s_c`),
or a pseudo-interactive one (e.g. `:norm`, `feedkeys()`, ...).

##
## From a script, how to fold the lines 12 to 34?

    :12,34fold

`:fold` is the Ex equivalent of the normal command `zf`.

###
## For which folding methods can I delete folds?

`manual` and `marker`.

## How to delete folds
### recursively at the cursor?

    zD

### everywhere?

    zE

##
# Folding method
## When writing a folding expression, which value should it produce so that the parsed line:
### is not in a fold?

    0

### is in a fold of level 3?

    3

###
### starts a fold of level 3?

    '>3'

#### When can I use just `3`?

When the previous line has a lower level.

###
### ends a fold of level 3?

    '<3'

#### When can I use just `3`?

When the next line has a lower level.

###
### has the same level as
#### the previous line minus 3?

    's3'
     │
     └ subtract

#### the previous line plus 3?

    'a3'
     │
     └ add

#### the next or previous line, whichever is the smallest one?

    -1

##
## I'm using the `indent` foldmethod.
### For a given line, how to make Vim use the level of indentation of the line above or below?

If this line starts with a particular character, assign it to `'foldignore'`.

Any line starting with the character saved  inside this option will get its fold
level from the next or previous line (the smallest of the two).
Their own indentation level is ignored, hence the option name.
White space is skipped before checking for the character.

##
# Miscellaneous
## How to yank all the lines in closed folds?

    qaq
    :folddoclosed y A

`:folddoclosed` is similar to `:g`.
It lets you execute a command on a set of lines; the lines in closed folds.

### And for lines in open folds?

    :folddoopen if foldlevel('.') > 0 | y A | endif

---

`:folddoopen` does not operate only on lines which are in open folds.
It operates on any line which is not inside a closed fold.
IOW it also operates on lines outside of folds.
That's why you need the `foldlevel()` test.

---

Don't conflate `:folddoopen` with `:foldopen`.

##
## In a script, how to make Vim recompute folds without altering the state of the folds (open vs closed)?

Execute `:call foldlevel(1)`.

    $ vim -Nu NONE -S <(tee <<'EOF'
        setl fml=0 fdm=expr fde=getline(v:lnum)=~#'^#'?'>1':'='
        %d|for i in range(2) | sil pu=['#', '']+repeat(['x'], 5)+[''] | endfor
        setl fdm=manual
        1d_
        norm! zoGyyp
    EOF
    ) /tmp/file

    " the first fold stays open
    :setl fdm=expr | call foldlevel(1) | setl fdm=manual

    " the first fold gets closed
    :setl fdm=expr | exe 'norm! zx' | setl fdm=manual

Note that in both commands, the folds get recomputed, which is why you can close
the new  third fold by  pressing `zc`.  But  `zx` makes Vim  apply `'foldlevel'`
which does not preserve the state of the folds.

Also,  this  works  because  evaluating  any  fold-related  function  makes  Vim
recompute all folds; it has to, so that the function can give a correct value.

---

Alternatively, you could execute:

    exe winnr() .. 'windo "'
    setl fdm=manual

Or:

    let [curwin, curbuf] = [win_getid(), bufnr('%')]
    call timer_start(0, {-> winbufnr(curwin) == curbuf && setwinvar(curwin, '&fdm', 'manual')})

Or:

    let view = winsaveview()
    norm! zizi
    setl fdm=manual
    call winrestview(view)

But note that `:call foldlevel(1)` is the fastest method:

    " open vimrc
    :10000Time call foldlevel(1)
    0.055 seconds to run ...˜

    :10000Time exe winnr() .. 'windo "'
    0.080 seconds to run ...˜

    :10000Time let [g:curwin, g:curbuf] = [win_getid(), bufnr('%')] | call timer_start(0, {-> winbufnr(g:curwin) == g:curbuf && setwinvar(g:curwin, '&fdm', 'manual')})
    0.150 seconds to run ...˜

    :10000Time let view = winsaveview() | exe 'norm! zizi' | call winrestview(view)
    0.270 seconds to run ...˜

Besides, the fact that `:123windo "` makes Vim recompute folds is not documented.
It would be brittle to rely on such an undocumented feature, because there is no
guarantee that it continues working in the future.

