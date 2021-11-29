# What are the three mechanisms highlighting text in Vim?

The matches defined by `matchadd()`.
The builtin HGs documented at `:help highlight-groups`.
The syntax highlighting.

## In case of conflict, which one wins?

From the biggest priority to the lowest one:

   1. `matchadd()`
   2. builtin HGs
   3. syntax highlighting

## Can you think of an example of conflict?

When `'cursorline'` is set, the current line is highlighted by the `CursorLine` HG.
And if you're in the qf window, the beginning of the current line should also be
highlighted by `qfFileName`.

So, at that position, the text is highlighted by `CursorLine` and `qfFileName`.

### Which attributes are used in this example?

The ones of the builtin HG, `CursorLine`.

### How to make Vim use the other attribute, on a per-attribute basis?

Reset the undesired attribute of the builtin HG by giving it the value `NONE`.

##
# Match
## What's the benefit of `matchadd()` over `:[2|3]match`?

`matchadd()` can define as many matches as you want.
And it gives you control over the relative priority between the matches.

##
## What's the default priority of
### a match?

`10`.

### `'hlsearch'` (HG `Search`)?

`0`.

##
## How to get information about
### the match whose id is `3`?  (without using `getmatches()`)

    :echo matcharg(3)

### all the matches defined in the current window?

    :echo getmatches()

Each item in the list is a dictionary with 4 keys:

   - `group`
   - `pattern`
   - `priority`
   - `id`

Contrary to `matcharg()`  which is limited to the id  `1` to `3`, `getmatches()`
can give information about *all* the matches.

##
## How to highlight
### `pat` with the HG `DiffAdd`?  (2)

    :match DiffAdd /pat/

    :call matchadd('DiffAdd', 'pat')

### `pat` with `DiffAdd`, an id of `12` and a priority of `34`?

    :call matchadd('DiffAdd', 'pat', 34, 12)

##
## How to make `matchadd()` choose an id automatically for the match?

Don't give any priority, or `-1` if you need the optional `dict` argument.

##
## How to remove
### the match `3`?  (2)

    :3match none
    :call matchdelete(3)

### a match defined by `matchadd()`?

Call `matchdelete()`:

    :let id = matchadd('DiffAdd', 'pat')
    :call matchdelete(id)

### all the matches?

    :call clearmatches()

##
## How to restore all the matches?

Use `setmatches()`:

    :call matchadd('DiffAdd', 'foo')
    :call matchadd('DiffChange', 'bar')

    :let list = getmatches()
    :call clearmatches()

    :call setmatches(list)
          ^--------^

##
## Is the search of the pattern case-sensitive by default?

Yes.

Add `\c` to make it insensitive.

## What's the difference between a match whose priority is `0` and another whose priority is `> 0`?

The HG `Search` wins over a match whose priority is `0`, but loses otherwise.

## How does Vim handle a too complex pattern passed to `:syn`, `:match`, or `matchadd()`?

It stops highlighting new matches/text after `'redrawtime'` ms, to avoid hanging.

##
# Highlight Groups
## What are the three main types of highlight groups?

   1. The builtin ones documented at `:help highlight-groups`, which are used to
      highlight various UI elements.

   2. The ones used for all syntax languages, documented at `:help group-name`,
      like for example `Function` or `Identifier`.

   3. The ones used for specific languages.  Their  names start  with  the name
      of  the language.   Many  don't have  any attributes, but are linked to
      a group of the second type.

---

`:help highlight-groups` mentions:

    CursorIM
    Terminal

But they're not present in the output of `:highlight` when you start Vim with no
config (`$ vim -Nu NONE`), nor when you load seoul256.

`CursorIM` is not there because it requires Vim to be in a certain mode...
Maybe `Terminal` is not there because it has no default definition, and needs to
be defined manually...

---

When you start Vim with `$ vim -Nu NONE`, `:highlight` includes these HGs:

    ToolbarButton
    ToolbarLine
    lCursor

But they're not documented at `:help highlight-groups`.
I think the help forgot them.

## What are the two types of highlight groups among the ones used for all syntax languages?

   - the preferred groups (prefixed by a `*` at `:help group-name`)

   - the minor groups

### Where and how are they set?

By default, they're set in `$VIMRUNTIME/syntax/syncolor.vim`.

The minor groups are linked to the preferred groups.

However, they both  can be reset in  a color scheme, and the minor  groups can be
set directly (without a link).

For example,  `Function` is  a minor group,  and by default  it's linked  to the
preferred group `Identifier`; so, they share the same colors.
However, seoul256 defines them separately.

##
## Is the name of a HG case-INsensitive?

Yes:

    :highlight MyGroup ctermbg=green guibg=green
    :highlight mygroup
    MyGroup        xxx ctermbg=10 guibg=green˜

##
## Why shouldn't a syntax plugin author set the attributes of a HG in their plugin?  (2)

   1. It's not their job.
   Their job is to teach Vim how to recognize the meaning of the text.

   2. If every syntax plugin author did the same, the user experience would be
   inconsistent.
   For example,  in some  language the  functions could  be colored  in blue,
   while in another they would be colored in green.

## Which issue can you face if a syntax plugin author sets the attributes of a HG in their plugin?

When you change the color scheme, you may lose the highlighting of some text.

That's because a  color scheme executes `:highlight clear` at  its beginning, to
reset all HGs to their default attributes.
Doing so, it removes all HGs including the ones set in syntax plugins.
But it  doesn't reinstall  the latter  because it  has no  way of  knowing their
existence.  It can only know about the HGs documented at:

   - `:help group-name`
   - `:help highlight-groups`

---

That's what happens to `snipLeadingSpaces` in a snippet buffer.
The latter highlights leading spaces on a line in a snippet definition.

Currently, we fix this issue by reloading  any syntax plugin used by a displayed
buffer, with an autocmd in our vimrc:

    au ColorScheme * ReinstallClearedHg()

##
## Builtin HGs
### How to get the list of all builtin HGs in Vim's pager?

    :help hl- C-d

### Which HGs control the appearance of
#### html links?

`Underlined`

#### the completion menu?

    ┌────────────┬────────────────────────┐
    │ Pmenu      │ normal item            │
    ├────────────┼────────────────────────┤
    │ PmenuSel   │ selected item          │
    ├────────────┼────────────────────────┤
    │ PmenuSbar  │ scrollbar              │
    ├────────────┼────────────────────────┤
    │ PmenuThumb │ thumb of the scrollbar │
    └────────────┴────────────────────────┘

For more info, see `:help popupmenu-keys`.

#### the line matching the current qf entry in the qf window?

`QuickFixLine`:

    highlight! link QuickFixLine Search
    "        │
    "        └ :help E414

#### the more prompt (used when Vim's pager has a full page)?

`MoreMsg`

#### unprintable characters?

`SpecialKey`

This controls the  appearance of the special  keys in the output  of `:map`, and
the ones in `'listchars'`.

#### characters giving information but which don't exist in the buffer?

`NonText`

This controls the appearance of the characters in `'showbreak'` (among others).

#### the tilde characters in front of filler lines after last line in the buffer?

`EndOfBuffer`

#### the parentheses under the cursor when the `matchparen` plugin is enabled?

`MatchParen`

##
## Setting a HG
### Are `cterm` and `ctermfg` some attributes of a HG?

No, they're arguments passed to `:highlight` to set some attributes of a HG.

The values that you pass to those arguments *are* the attributes.

### What are the 8 arguments which can be passed to `:highlight`?

    ┌──────────┬──────────────────────────────┐
    │ term     │ style in normal terminal     │
    │ cterm    │ style in color terminal      │
    │ gui      │ style in GUI                 │
    ├──────────┼──────────────────────────────┤
    │ ctermfg  │ foreground color in terminal │
    │ guifg    │ foreground color in GUI      │
    ├──────────┼──────────────────────────────┤
    │ ctermbg  │ background color in terminal │
    │ guibg    │ background color in GUI      │
    │ guibg    │ background color in GUI      │
    └──────────┴──────────────────────────────┘

### Can the attributes set by `guifg` and `guibg` be used in a terminal?

Yes, on the condition that:

   - `'tgc'` is set

   - the terminal supports true colors

   - Vim and tmux are properly configured to support true colors:
   see `:help xterm-true-color`, and `man tmux /Tc`

### What are the 6 most common attributes which can be given to a HG via `[c]term` and `gui`?

The  `term`, `cterm`,  and `gui`  arguments accept  this non-exhaustive  list of
values (attributes):

   - bold
   - underline
   - reverse
   - italic
   - standout
   - NONE

### What happens if I use `cterm=reverse`?

The values of the arguments `fg` and `bg` are exchanged, in a color terminal.

### How to hide the characters highlighted by the HG `NonText`?

    :highlight NonText ctermfg=bg

`bg` is a  special value, which is  evaluated into the value which  was given to
`ctermfg=` or `guifg` from the HG `Normal`.

###
### When do I need to add a bang after `:highlight`?

When you try to create a link between  2 HGs, and the first one has been defined
with its own attributes:

    :highlight MyGroup ctermbg=green guibg=green
    :highlight link MyGroup Search
    E414˜

    " ✔
    :highlight! link MyGroup Search
              ^

---

If you execute `:highlight MyGroup`, you'll see that the old attributes are still there.
But the highlighting applied to `xxx` is given by the link.
This shows that a link has priority over attributes.

---

You could also have cleared `MyGroup`:

    :highlight MyGroup ctermbg=green guibg=green
    :highlight clear MyGroup
    :highlight link MyGroup Search

### My HG has its own attributes and is linked to another HG.  Which attributes is it using?

The link wins:

    :highlight MyGroup ctermbg=green guibg=green
    :highlight! link MyGroup Search
    :highlight MyGroup

###
### How to clear a HG?

If it has its own attributes (and no link), pass the `clear` argument to `:highlight`:
```vim
 # definition
highlight MyGroup ctermbg=green guibg=green

 # clearing
highlight clear MyGroup

 # check
highlight MyGroup
```
    MyGroup        xxx cleared

If it's linked, then you need to reset the link to `NONE` (`*`):
```vim
 # definition
highlight default link MyGroup ErrorMsg

 # clearing
highlight link MyGroup NONE

 # check
highlight MyGroup
```
    MyGroup        xxx cleared

If it  has its own attributes  *and* is linked to  another HG at the  same time,
then you need to `clear` it, *then* reset the link to `NONE` (`*`):
```vim
 # definition
highlight MyGroup ctermbg=green guibg=green
highlight! default link MyGroup ErrorMsg

 # clearing
highlight clear MyGroup
highlight link MyGroup NONE

 # check
highlight MyGroup
```
    MyGroup        xxx cleared

---

(`*`) In reality, you don't always *need* to reset the link to `NONE`.
`:highlight clear`  might work  too; but only  if the link  was set  without the
`default` argument.  OTOH,  resetting the link to  `NONE` works unconditionally;
it's more reliable.

### How to reset (clear) some attribute of a HG?

Give it the value `NONE`.

    :highlight MyGroup ctermfg=blue ctermbg=yellow
    :highlight MyGroup ctermfg=NONE
    :highlight MyGroup

Here, the first statement set the attribute `ctermfg` with the color `blue`, but
the second one reset it.
Notice how it doesn't touch the other attribute `ctermbg`.

### What's the effect of `:highlight clear`?

It resets all highlighting to the defaults.

For the  HGs documented at  `:help group-name` and `:help  highlight-groups`, it
means that the attributes are reset to their default values (which depend on the
value of `'bg'`).

For the  user-defined HGs,  it simply  means that  their attributes  are removed
(because  they  have  no  default   value;  by  definition,  they  didn't  exist
originally):

    $ vim --cmd 'highlight WillItSurvive ctermbg=green | highlight clear | highlight WillItSurvive | cquit'
    WillItSurvive  xxx cleared˜

as well as their links:

    $ vim --cmd 'highlight link WillItSurvive ErrorMsg | highlight clear | highlight WillItSurvive | cquit'
    WillItSurvive  xxx cleared˜

---

There is one exception though.  Default links survive:

                           v----------v
    $ vim --cmd 'highlight default link WillItSurvive ErrorMsg | highlight clear | highlight WillItSurvive | cquit'
    WillItSurvive  xxx links to ErrorMsg˜

Which is why you should probably always use the `default` argument when defining
a linked HG.

##
### What's the purpose of `'hl'`?

It's a global option which can be  used to configure the highlighting of various
elements of the UI.
It contains a comma separated list of values.

Each value follows one the following syntax:

      ┌ character standing for which element of the UI you want to configure
      │         ┌ character standing for which style you want to apply
      ├────────┐├────┐
      {occasion}{mode}

      {occasion}:{HG}
                  │
                  └ highlight group to color the element of the UI

The default values all use the 2nd syntax.  They all use a HG.
But you could also use a mode:

    ┌───┬─────────────────┐
    │ r │ reverse         │
    ├───┼─────────────────┤
    │ i │ italic          │
    ├───┼─────────────────┤
    │ b │ bold            │
    ├───┼─────────────────┤
    │ s │ standout        │
    ├───┼─────────────────┤
    │ u │ underline       │
    ├───┼─────────────────┤
    │ c │ undercurl       │
    ├───┼─────────────────┤
    │ n │ no highlighting │
    └───┴─────────────────┘

#### Why should you *not* use it?

`:highlight link`  gives you the same  control, and is more  consistent with how
you configure non-builtin HGs.

###
# Color Scheme
## How to run some code before or after a color scheme has been sourced?

Install an autocmd listening to:

    ColorschemePre

    Colorscheme

## How to write a color scheme which is not altered by the user's configuration of the terminal palette?

Don't refer to the ANSI colors (i.e. color names and color 0-15).

   > So if  I write colorscheme morning  in my .vimrc, since  the morning colorscheme
   > makes reference to the ANSI colors, and these have been changed from the default
   > ones by ~/.Xresources, the morning colorscheme is not rendered as the author had
   > intended it to be.
   > [...]
   > I see  therefore two  ways to  make my terminal's  theme independent  from vim's
   > color scheme:
   > 1. Use a  vim color scheme that  does not make  reference to the ANSI  colors, only
   > using colors 16-255, which have not been modified by ~/.Xresources.
   > There should  be plenty of  colors for  the scheme to  choose from to  be pretty
   > enough.
   > [...]

Source: <https://www.reddit.com/r/vim/comments/bp67ww/how_to_make_vim_ignore_xresources/ens0rkg/>

##
# Terminal Colors
## How to get the colors used in a terminal buffer?

    :echo term_getansicolors('')
                             ├┘
                             └ current terminal buffer

### How to set them at starting time?

Assign 16 hex color codes to the variable `g:terminal_ansi_colors`:

    let g:terminal_ansi_colors = ['#123456', ...]

Note that this is useful only when you  start gVim; or when you start Vim from a
terminal whose `$TERM` is not `xterm` nor `xterm-256color`, and `'tgc'` is set.
Otherwise,  Vim should  correctly  use  the 16  ANSI  colors  of the  underlying
terminal.

Also, you can use a color name  as suggested at `:help gui-colors`, instead of a
hex color code, but  it would make Vim choose the  color in its builtin/fallback
palette, which will be ugly/flashy.

##
### How to change them at run time?

    :call term_setansicolors('', ['#123456', ...])

##
##
##
# Todo
## ?

Document how to change the cursor color.

In the GUI, Vim  is able to change the color of the  cursor, via the `Cursor` HG
whose default attributes are  fine.  In the TUI, Vim cannot  change the color of
the cursor; the latter is set by the terminal.

Source: <https://unix.stackexchange.com/a/72800>

So, in  the TUI,  you have to  do it at  the terminal  level, using an  `OSC 12`
sequence:

    # open xterm
    $ printf '\033]12;#ff0000\007'

See: `OSC Ps ; Pt BEL/;/Ps = 1 2`

To send this sequence to the terminal, you can use `echoraw()` or append it to `'t_ti'`.
In tmux, you can also set the tmux pane option `cursor-color`:
```vim
 # can also be an hexadecimal code
var color: string = 'green'
if $TMUX != ''
    # No need to quote the value of `color`.  The command is not passed to a shell.
    var cmd: string = 'tmux set-option -p cursor-color ' .. color
    job_start(cmd)
else
    # `OSC Ps ; Pt ST/;/Ps = 1 2  -> Change text cursor color to Pt.`
    var seq: string = "\033]12;" .. color .. "\007"
    echoraw(seq)
endif
```
See `man tmux /cursor-colour`.

You probably also need to set the  terminfo extensions `Cr`, `Cs`, which you can
do with the server option `terminal-features`:

    set-option -as terminal-features '*:ccolour'

Like all server options, if you don't  set it automatically in your tmux config,
but manually  later, you need  to detach then re-attach  the client for  the new
value to take effect.

---

In the GUI, the cursor color is the foreground color of `Normal`:

    :highlight Cursor
    Cursor         xxx guifg=bg guibg=fg
                                ^------^

You can get its value programmatically, like this:

    :echo hlget('Normal')->get(0)->get('guifg', '')

---

To reset the cursor color, you need OSC 112; see `OSC Ps ; Pt ST/;/Ps = 1 1 2`.
To send this sequence to the terminal, you can use `echoraw()` or append it to `'t_te'`.
In tmux, you can also set the tmux pane option `cursor-color`:
```vim
if $TMUX != ''
    job_start('tmux set-option -p cursor-color default')
else
    echoraw("\033]12;112\007")
endif
```
## ?

Document that the optional `default` argument of the `:highlight` command has 2 effects.

First, it prevents a link from overwriting an existing one:

    $ vim /tmp/c.c +'highlight link cComment Question | highlight cComment'
    cComment       xxx links to Question˜

                               v-----v
    $ vim /tmp/c.c +'highlight default link cComment Question | highlight cComment'
    cComment       xxx links to Comment˜

Second,  it causes  Vim to  restore a  link after  `:highlight clear`  (which is
executed whenever you change/reload the color scheme):

                           v-----v
    $ vim --cmd 'highlight default link WillItSurvive ErrorMsg | highlight clear | highlight WillItSurvive | cquit'
    WillItSurvive  xxx links to ErrorMsg˜

See `:help :highlight-default`.

## ?

Document that  for `CursorLine`  not to  completely override  `Diff*`, `Search`,
`IncSearch`, you should define the latter with the `reverse` attribute.

    highlight clear CursorLine | highlight CursorLine ctermbg=white
    highlight DiffChange ctermfg=235 ctermbg=108
    nos e /tmp/file1 | pu='some text'
    nos vs /tmp/file2 | pu='some other text'
    windo set cul | diffthis

When you select the changed line, `CursorLine` overrides `DiffChange`.
Now, try this:

    highlight clear CursorLine | highlight CursorLine ctermbg=white
    highlight DiffChange cterm=reverse ctermfg=108 ctermbg=235
    nos e /tmp/file1 | pu='some text'
    nos vs /tmp/file2 | pu='some other text'
    windo set cul | diffthis

This time, it looks like `DiffChange` overrides `CursorLine`.

---

Before `7.4.390`, the `Diff*` HGs had priority over `CursorLine`.  Starting from
[`7.4.391`][1],  the attributes  of  `Diff*` are  combined  with the  attributes
of  `CursorLine`,  which is  why  the  `reverse`  attribute of  `Diff*`  affects
`CursorLine` causing the undefined `ctermfg` attribute to be used instead of the
defined `ctermbg`:

    " on a line without diff highlighting
    highlight CursorLine ctermbg=white
    ⇔
    highlight CursorLine ctermbg=white ctermfg=NONE

    " on a line *with* diff highlighting, 'reverse' is applied
    highlight CursorLine cterm=reverse ctermbg=white ctermfg=NONE
    ⇔
    highlight CursorLine ctermbg=NONE ctermfg=white
    ⇔
    highlight CursorLine ctermfg=white

Same thing for the search and match highlighting (`Search` and `IncSearch`?).
Starting from [`7.4.682`][2], their attributes are combined with `CursorLine`.

## ?

Some  people say  that  `:syntax  on` and  `:syntax  enable`  are *in  practice*
equivalent.  They say that, because most color scheme authors write this:

    if exists("syntax_on")
      syntax reset
    endif

To document. (also document the `reset` subcommand)

<https://www.reddit.com/r/vim/comments/choowl/vimpolyglot_syntax_on_or_syntax_enable/euvzia0/>

Update: This whole snippet seems useless:
<https://github.com/vim/colorschemes/issues/34>

Also, `:syntax reset` is confusing because it has nothing to do with the syntax:

   > It is a bit of a wrong name, since it does not reset any syntax items, it only
   > affects the highlighting.

## ?

Why did Vim choose to apply the `cterm` attribute when `'termguicolors'` is set?

Answer: <https://github.com/vim/vim/issues/1740#issuecomment-667682280>

## ?

Document the fact  that `execute('highlight ...')` can contain  newlines, if the
width of the current window is too small.

You need to make sure they're removed.

It seems the issue is specific to `:highlight`:

<https://www.reddit.com/r/vim/comments/aikx7g/utility_function_to_extendoverride_highlight/eep49gk/>

Still, maybe there are other commands which behave like that.

Make sure we haven't made this kind of mistake elsewhere:

    :vim /\C\s\<execute(/gj ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/** ~/.vim/vimrc

Also, should we remove the newline, or replace it  with a space?
If we remove it, is it enough, or does Vim still add an extra space?

When you know what to do, review what we did in:

    ~/.vim/autoload/colorscheme.vim
    /colorscheme#customize(
    /highlight Underlined

Update:  Now that we have `hlget()`, all this section needs to be reviewed.

## ?

Document the fact that for a HG, the only relevant attributes are:

- `gui`, `guifg` and `guibg` (in GUI)
- `cterm`, `guifg` and `guibg` (in a truecolor terminal)
- `term`, `cterm`, `ctermfg` and `ctermbg` (in a terminal)

BTW, the style `term` is only used in a terminal with less than 2 colors (i.e. `&t_Co == 0`):

   > Typographic attributes are defined with **term= for &t_Co == 0** and cterm= for &t_Co >= 2.

Source: <https://github.com/vim/colorschemes/wiki/On-terminal-emulators-and-colors#typography>

In which case, `cterm`, `ctermfg` and `ctermbg` are ignored:

   > cterm, ctermbg, and ctermfg are ignored.

Source: <https://github.com/vim/colorschemes/wiki/On-terminal-emulators-and-colors#t_co--0>

Note that a virtual console in linux supports 8 colors, so `term` doesn't apply there.

## ?

Document that it  seems that the special  color value `bg` is  only available if
the Normal HG has its `ctermbg` attribute set.
It's probably  the same thing  for `fg`: the Normal  HG must have  its `ctermfg`
attribute set.

Make sure it's true.

MWE:

    :colorscheme elflord
    :highlight EndOfBuffer ctermfg=bg
    E420: BG color unknown˜

It doesn't matter whether you start Vim or gVim.
It seems only `ctermbg` matters, not `guibg` (weird...).

## ?

Experiment the new termcap codes `t_AU` and `t_8u`:
<https://github.com/vim/vim/commit/e023e88bed3f2e0a7ea4cf10cac2de80bc9c271c>

They should  allow you to  specify a color for  underline/undercurl, independent
from the foreground color.

See also `:help undercurl`:

   > "undercurl" is a curly underline.  When "undercurl" is not possible
   > then "underline" is used.  In general "undercurl" and "strikethrough"
   > are only available in the GUI and some terminals.  The color is set
   > with |highlight-guisp| or |highlight-ctermul|.  You can try these
   > termcap entries to make undercurl work in a terminal: >
   >     let &t_Cs = "\e[4:3m"
   >     let &t_Ce = "\e[4:0m"

## ?

Document that  running a  `:highlight` command  to (re)set  an attribute  has no
effect on the other ones.

    :highlight SpecialKey
    SpecialKey     xxx term=bold ctermfg=145 guifg=#afafaf˜
    :highlight SpecialKey guifg=#121212
    :highlight SpecialKey
    SpecialKey     xxx term=bold ctermfg=145 guifg=#121212˜
                       ^-------------------^
                       did not change

That's because Vim doesn't clear existing attributes.
It merges them.
From `:help :highlight-verbose` (right above):

   > Note that all settings that are not included remain the same, only the
   > specified field is used, and **settings are merged with previous ones**.

## 'bg'

What's the effect of setting `'background'`?

Vim will adjust the builtin HGs for the new value.
`'bg'` is also  used in `$VIMRUNTIME/syntax/syncolor.vim` to  set the attributes
of preferred HGs (used in syntax highlighting).
After changing `'bg'`, you must load `syntax.vim` again to see the result.
This can be done with `:syntax on`.

Update:

That's not what seems to happen.

    :highlight ErrorMsg ctermbg=blue
    :unlet! g:colors_name
    :set bg=light
    :highlight ErrorMsg

`ErrorMsg` wasn't reset.
Also, it seems that `syncolor.vim` is automatically resourced...

---

When  a color scheme  is already  loaded (i.e.  `g:colors_name` is  set), setting
`'bg'` will cause it to be reloaded.
The color scheme may adjust to the new value of `'bg'`.
Or it may reset `'bg'`.
First delete `g:colors_name` when needed (for what?  to make Vim behave as if no
color scheme was loaded, i.e. only resets the builtin HGs?).
<https://vi.stackexchange.com/a/13089/17449>

When `'bg'` is set, the default attributes for the HGs will change.
To use other attributes, place `:highlight` commands *after* setting `'bg'`.

## how to write my own color scheme

Document this:

    https://speakerdeck.com/cocopon/creating-your-lovely-color-scheme
    http://vimcasts.org/episodes/creating-colorschemes-for-vim/
    https://gist.github.com/romainl/5cd2f4ec222805f49eca
    https://vimways.org/2019/vims-default-colors/

---

template to create own color scheme:

    https://github.com/cocopon/iceberg.vim/blob/master/src/template.vim

    if !has('gui_running') && &t_Co < 256
      finish
    endif

    set background=dark
    highlight clear

    let g:colors_name = 'iceberg'


    {{ rules }}
    highlight HG ctermfg=...
    ...

    {{ links }}
    highlight! link HG1 HG2
    ...


To customize an existing one:

    $ mkdir ~/.vim/colors/
    $ cat <<'EOF' >~/.vim/colors/test.vim
    runtime colors/evening.vim
    let g:colors_name = 'mine'
    highlight ...
    ...
    EOF

    $ echo 'colorscheme mine' >>~/.vim/vimrc

---

For more info about how creating a color scheme:

    $VIMRUNTIME/colors/README.txt:70

In particular, if you can't find a meaningful name for your color scheme, write:

    let g:colors_name = expand('<sfile>:t:r')

## how to write a reliable / correct color scheme

<https://github.com/lifepillar/vim-colortemplate>

## how to test whether my color scheme contains some common mistakes

Load the file implementing your color scheme:

    :e my_colorscheme.vim

and run:

    :so $VIMRUNTIME/colors/tools/check_colors.vim

`check_colors.vim` should output possible errors.

## document that a highlight group is automatically defined whenever you define a syntax group

    :highlight foobar
    E411: highlight group not found: foobar˜

    :syn match foobar /foobar/
    :highlight foobar
    foobar         xxx cleared˜

But notice that it doesn't have any attribute defined yet.
That's for you to define later:

    :highlight foobar ...
                      ^^^

##
## hlID() and synID()

    :echo hlID('NonText')

    :echo synID('.', col('.'), 1)

Returns the id of:

   - the HG `NonText`

   - the HG highlighting the character after the cursor or the syntax item after
     the cursor

L'ID d'un élément syntaxique est identique à celui du HG qui le colorise.
On peut le vérifier en positionnant le curseur sur du texte dans un bloc de code
markdown et en tapant:

    :echo synID('.', col('.'), 1)
    120 ˜

    :echo synID('.', col('.'), 1)->synIDattr('name')
    markdownCodeBlock ˜

    :echo hlID('markdownCodeBlock')
    120 ˜

---

Lorsque le 3e  argument de `synID()` est non nul,  si l'élément est transparent,
il est réduit à l'élément qu'il révèle.
Utile pour connaître les attributs du HG qui le met en couleurs.

## synIDtrans()

    :echo synIDtrans(42)

Retourne l'id du HG `42`, en suivant d'éventuels liens.
Si le HG  d'identifiant `42` est lié à  un autre HG, c'est l'id de  cet autre HG
qui est retourné.

On utilise généralement  `synIDtrans()` autour d'un `synID()`  ou `hlID()`, pour
s'assurer que les liens sont suivis.

## synIDattr()

    :echo hlID('Comment')->synIDattr('fg')
    :echo synID('.', col('.'), 1)->synIDattr('name')

Retourne:

   - la couleur du HG Comment (valeur de l'attribut `fg`)
   - le nom de l'élément syntaxique sous le curseur

`synIDattr()` permet d'obtenir la valeur de n'importe quel attribut d'un HG.

Si on  veut s'assurer que  les liens entre HGs  soient suivis, il  faut utiliser
`synIDtrans()`:

    :echo hlID('Comment')->synIDtrans()->synIDattr('fg')
    :echo synID('.', col('.'), 1)->synIDtrans()->synIDattr('name')

## synstack()

Document it.

## :syn sync

    :syntax sync fromstart

Réparer la coloration syntaxique qui peut  avoir été perdue lorsque les règles à
appliquer sont complexes.

En  fonction de  la taille  du buffer,  et de  la complexité  des règles,  cette
commande peut être plus ou moins longue et coûteuse en cpu.

##
# Reference

[1]: https://github.com/vim/vim/commit/e0f148270a03e0da2bf21706bee4d2fe99146c55
[2]: https://github.com/vim/vim/releases/tag/v7.4.682
