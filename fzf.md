# ?

How to update fzf?

In your vimrc, write:

    :Plug 'junegunn/fzf', {'dir': '~/.fzf', 'do': './install ...'}
                                            ^------------------^
                                            this invokes the fzf installer
                                            whenever there's an update

# ?

How to control what interface fzf installs?

You can tweak the installer command by passing other arguments.
For example:

    $ ~/.fzf/install --all --no-bash

For more info about the options you can pass to the installer:

    $ ~/.fzf/install --help

# The preview for some files fails with this message: “highlight: Unknown source file extension...”!

Try to install a more recent version of the highlight package:

    $ sudo aptitude purge highlight highlight-common
    $ sudo aptitude install libboost1.58-dev liblua5.3-dev
    $ git clone https://gitlab.com/saalen/highlight.git highlight
    $ cd highlight
    $ make
    $ sudo make install

For more info: <http://www.andre-simon.de/doku/highlight/en/install.php>

##
# Options

Note that most options have the opposite versions with `--no-` prefix.

## Search mode
### -x, --extended

Extended-search mode.
Enabled by default.
You can disable it with `+x` or `--no-extended`.

### -e, --exact

Enable exact-match.

### -i

Case-insensitive match (default: smart-case match).

### +i

Case-sensitive match.

### --literal

Do not normalize latin script letters for matching.

### --algo=TYPE

Fuzzy matching algorithm (default: v2)

   - v2: Optimal scoring algorithm (quality)
   - v1: Faster but not guaranteed to find the optimal result (performance)

### -n, --nth=N[,..]

Comma-separated list of field index expressions for limiting search scope.
See Field Index Expression for the details.

### --with-nth=N[,..]

Transform the presentation of each line using field index expressions

### -d, --delimiter=STR

Field delimiter regex for `--nth` and `--with-nth` (default: AWKstyle).

##
## Search result
### +s, --no-sort

Do not sort the result.

### --tac  Reverse the order of the input

Example:

    $ history | fzf --tac --no-sort

### --tiebreak=CRI[,..]

Comma-separated list of sort criteria to apply when the scores are tied.

    ┌────────┬─────────────────────────────────────────────────────────────┐
    │ length │ Prefers line with shorter length                            │
    ├────────┼─────────────────────────────────────────────────────────────┤
    │ begin  │ Prefers line with matched substring closer to the beginning │
    ├────────┼─────────────────────────────────────────────────────────────┤
    │ end    │ Prefers line with matched substring closer to the end       │
    ├────────┼─────────────────────────────────────────────────────────────┤
    │ index  │ Prefers line that appeared earlier in the input stream      │
    └────────┴─────────────────────────────────────────────────────────────┘

   - Each criterion should appear only once in the list
   - index is only allowed at the end of the list
   - index is implicitly appended to the list when not specified
   - Default is length (or equivalently length,index)
   - If end is found in the list, fzf will scan each line backwards

##
## Interface
### -m, --multi

Enable multi-select with tab/shift-tab.

### +m, --no-multi

Disable multi-select.

### --no-mouse

Disable mouse.

### --bind=KEYBINDS

Comma-separated list of custom key bindings.
See Key Bindings for the details.

### --cycle

Enable cyclic scroll.

### --no-hscroll

Disable horizontal scroll.

### --hscroll-off=COL

Number  of screen  columns to  keep to  the right  of the  highlighted substring
(default: 10).
Setting it to a  large value will cause the text to be  positioned on the center
of the screen.

### --filepath-word

Make word-wise movements and actions respect path separators.
The following actions are affected:

   - backward-kill-word
   - backward-word
   - forward-word
   - kill-word

### --jump-labels=CHARS

Label characters for `jump` and `jump-accept`.

##
## Layout

### --height=HEIGHT[%]

Display fzf window below  the cursor with the given height  instead of using the
full screen.

### --min-height=HEIGHT

Minimum height when `--height` is given in percent (default: 10).
Ignored when `--height` is not specified.

### --layout=LAYOUT

Choose the layout (default: default)

    ┌──────────────┬───────────────────────────────────────────────────────────┐
    │ default      │ Display from the bottom of the screen                     │
    ├──────────────┼───────────────────────────────────────────────────────────┤
    │ reverse      │ Display from the top of the screen                        │
    ├──────────────┼───────────────────────────────────────────────────────────┤
    │ reverse-list │ Display from the top of the screen, prompt at  the bottom │
    └──────────────┴───────────────────────────────────────────────────────────┘

### --reverse

A synonym for `--layout=reverse`.

### --border

Draw border above and below the finder.

### --margin=MARGIN

Comma-separated expression for margins around the finder.

    ┌─────────┬──────────────────────────────────────────────┐
    │ TRBL    │ Same margin for top, right, bottom, and left │
    ├─────────┼──────────────────────────────────────────────┤
    │ TB,RL   │ Vertical, horizontal margin                  │
    ├─────────┼──────────────────────────────────────────────┤
    │ T,RL,B  │ Top, horizontal, bottom margin               │
    ├─────────┼──────────────────────────────────────────────┤
    │ T,R,B,L │ Top, right, bottom, left margin              │
    └─────────┴──────────────────────────────────────────────┘

Each part  can be  given in  absolute number  or in  percentage relative  to the
terminal size with % suffix.

Examples:

    $ fzf --margin 10%

    $ fzf --margin 1,5%

### --inline-info

Display finder info inline with the query.

### --prompt=STR

Input prompt (default: `> `).

### --header=STR

The given string will be printed as the sticky header.
The lines  are displayed  in the given  order from top  to bottom  regardless of
`--layout` option, and are not affected by `--with-nth`.
ANSI color codes are processed even when `--ansi` is not set.

### --header-lines=N

The first N lines of the input are treated as the sticky header.
When `--with-nth`  is set, the lines  are transformed just like  the other lines
that follow.

##
## Display

### --ansi Enable processing of ANSI color codes

### --tabstop=SPACES

Number of spaces for a tab character (default: 8)

### --color=[BASE_SCHEME][,COLOR:ANSI]

Color configuration.
The name of the base color scheme is followed by custom color mappings.
Ansi color code of -1 denotes terminal default foreground/background color.
You can also specify 24-bit color in #rrggbb format.

    $ fzf --color=bg+:24

    $ fzf --color=light,fg:232,bg:255,bg+:116,info:27

#### BASE SCHEME:

Default: dark on 256-color terminal, otherwise 16.

    ┌───────┬───────────────────────────────────────────┐
    │ dark  │ Color scheme for dark 256-color terminal  │
    ├───────┼───────────────────────────────────────────┤
    │ light │ Color scheme for light 256-color terminal │
    ├───────┼───────────────────────────────────────────┤
    │ 16    │ Color scheme for 16-color terminal        │
    ├───────┼───────────────────────────────────────────┤
    │ bw    │ No colors                                 │
    └───────┴───────────────────────────────────────────┘

#### COLOR:

    ┌─────────┬────────────────────────────────────────────────────────────────────┐
    │ fg      │ Text                                                               │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ bg      │ Background                                                         │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ hl      │ Highlighted substrings                                             │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ fg+     │ Text (current line)                                                │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ bg+     │ Background (current line)                                          │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ hl+     │ Highlighted substrings (current line)                              │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ info    │ Info                                                               │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ border  │ Border of the preview window and horizontal  separators (--border) │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ prompt  │ Prompt                                                             │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ pointer │ Pointer to the current line                                        │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ marker  │ Multi-select marker                                                │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ spinner │ Streaming input indicator                                          │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ header  │ Header                                                             │
    └─────────┴────────────────────────────────────────────────────────────────────┘

### --no-bold

Do not use bold text.

### --black

Use black background.

##
## History
### --history=HISTORY_FILE

Load search history  from the specified file and update  the file on completion.
When enabled, `C-n`  and `C-p` are automatically remapped  to `next-history` and
`previous-history`.

### --history-size=N

Maximum number of entries in the history file (default: 1000).
The file  is automatically truncated  when the number  of the lines  exceeds the
value.

##
## Preview
### --preview=COMMAND

Execute the  given command for  the current line and  display the result  on the
preview window.
`{}` in  the command is  the placeholder that  is replaced to  the single-quoted
string of the current line.
To transform the replacement string, specify field index expressions between the
braces (See Field Index Expression for the details).

    $ fzf --preview='head -$LINES {}'

    $ ls -l | fzf  --preview="echo  user={3}  when={-4..-2};  cat {-1}" --header-lines=1

fzf overrides `$LINES`  and `$COLUMNS` so that they represent  the exact size of
the preview window.

A  placeholder  expression starting  with  `+`  flag  will  be replaced  to  the
space-separated list of the selected lines  (or the current line if no selection
was made) individually quoted.

Examples:

    $ fzf --multi --preview='head -10 {+}'

    $ git log --oneline | fzf --multi --preview 'git show {+1}'

When using a field index expression, leading and trailing whitespace is stripped
from the replacement string.
To preserve the whitespace, use the `s` flag.

Also, `{q}` is replaced to the current query string.

Note that you can escape a placeholder pattern by prepending a backslash.

Preview window will be updated even when there is no match for the current query
if any of the placeholder expressions evaluates to a non-empty string.

### --preview-window=[POSITION][:SIZE[%]][:wrap][:hidden]

Determine the layout of the preview window.
If  the argument  ends with  `:hidden`,  the preview  window will  be hidden  by
default until toggle-preview action is triggered.
Long lines are truncated by default.
Line wrap can be enabled with `:wrap` flag.

If size is  given as 0, preview window  will not be visible, but  fzf will still
execute the command in the background.

#### POSITION: (default: right)

   - up
   - down
   - left
   - right

Examples:

    $ fzf --preview="head {}" --preview-window=up:30%

    $ fzf --preview="file {}" --preview-window=down:1

##
## Scripting
### -q, --query=STR

Start the finder with the given query.

### -1, --select-1

Automatically select the only match.

### -0, --exit-0

Exit immediately when there's no match.

### -f, --filter=STR

Filter mode.
Do not start interactive finder.
When used with `--no-sort`, fzf becomes a fuzzy-version of grep.

### --print-query

Print query as the first line.

### --expect=KEY[,..]

Comma-separated list of keys that can be used to complete fzf in addition to the
default enter key.
When this option is set, fzf will print the name of the key pressed as the first
line of its output (or as the second line if `--print-query` is also used).
The line will be empty if fzf is completed with the default enter key.
If `--expect` option  is specified multiple times, fzf will  expect the union of
the keys.
`--no-expect` will clear the list.

    $ fzf --expect=ctrl-v,ctrl-t,alt-s --expect=f1,f2,~,@

### --read0

Read input delimited by ASCII NUL characters instead of newline characters.

### --print0

Print output delimited by ASCII NUL characters instead of newline characters.

### --no-clear

Do not clear finder interface on exit.
If fzf was started in full screen mode,  it will not switch back to the original
screen, so you'll have to manually run tput rmcup to return.
This option can be used to avoid  flickering of the screen when your application
needs to start fzf multiple times in order.

### --sync

Synchronous search for multi-staged filtering.
If specified,  fzf will  launch ncurses  finder only after  the input  stream is
complete.

    $ fzf --multi | fzf --sync

### --version

Display version information and exit.

##
# Environment Variables
## FZF_DEFAULT_COMMAND

Default command to use when input is tty.
On *nix  systems, fzf runs the  command with `$ sh  -c`, so make sure  that it's
POSIX-compliant.

## FZF_DEFAULT_OPTS

Default options.

    $ export FZF_DEFAULT_OPTS="--extended --cycle"

##
# Exit Status

    ┌─────┬─────────────────────────────┐
    │ 0   │ Normal exit                 │
    ├─────┼─────────────────────────────┤
    │ 1   │ No match                    │
    ├─────┼─────────────────────────────┤
    │ 2   │ Error                       │
    ├─────┼─────────────────────────────┤
    │ 130 │ Interrupted with C-c or Esc │
    └─────┴─────────────────────────────┘

##
# Field Index Expression

A  field index  expression  can be  a  non-zero integer  or  a range  expression
(`[BEGIN]..[END]`).
`--nth` and `--with-nth` take a comma-separated list of field index expressions.

## Examples

    ┌──────┬─────────────────────────────────────────────────┐
    │ 1    │ The 1st field                                   │
    ├──────┼─────────────────────────────────────────────────┤
    │ 2    │ The 2nd field                                   │
    ├──────┼─────────────────────────────────────────────────┤
    │ -1   │ The last field                                  │
    ├──────┼─────────────────────────────────────────────────┤
    │ -2   │ The 2nd to last field                           │
    ├──────┼─────────────────────────────────────────────────┤
    │ 3..5 │ From the 3rd field to the 5th field             │
    ├──────┼─────────────────────────────────────────────────┤
    │ 2..  │ From the 2nd field to the last field            │
    ├──────┼─────────────────────────────────────────────────┤
    │ ..-3 │ From the 1st field to the 3rd to the last field │
    ├──────┼─────────────────────────────────────────────────┤
    │ ..   │ All the fields                                  │
    └──────┴─────────────────────────────────────────────────┘

##
# Extended Search Mode

Unless specified otherwise, fzf will start in "extended-search mode".
In this mode, you can specify multiple patterns delimited by spaces, such as:

    'wild ^music .mp3$ sbtrkt !rmx

You can prepend a backslash to a space (\ ) to match a literal space character.

## Exact-match (quoted)

A term  that is prefixed  by a single-quote character  (') is interpreted  as an
"exact-match" (or "non-fuzzy") term.
fzf will search for the exact occurrences of the string.

## Anchored-match

A term can  be prefixed by `^`,  or suffixed by `$` to  become an anchored-match
term.
Then fzf will search for the lines that start with or end with the given string.
An anchored-match term is also an exact-match term.

## Negation

If a term is  prefixed by `!`, fzf will exclude the lines  that satisfy the term
from the result.
In this case, fzf performs exact match by default.

## Exact-match by default

If you don't  prefer fuzzy matching and  do not wish to  "quote" (prefixing with
`'`) every word, start fzf with `-e` or `--exact` option.
Note that when `--exact` is set, '-prefix "unquotes" the term.

## OR operator

A single bar character term acts as an OR operator.
For example,  the following query matches  entries that start with  core and end
with either go, rb, or py.

    ^core go$ | rb$ | py$

##
# Key Bindings

You  can customize  key  bindings of  fzf  with `--bind`  option  which takes  a
comma-separated list of key binding expressions.
Each key binding expression follows the following format: `Key:Action`.

    $ fzf --bind=ctrl-j:accept,ctrl-k:kill-line

### Available Keys (Synonyms)

    ctrl-[a-z]
    ctrl-space
    ctrl-alt-[a-z]
    alt-[a-z]
    alt-[0-9]
    f[1-12]
    enter       (return ctrl-m)
    space
    bspace      (bs)
    alt-up
    alt-down
    alt-left
    alt-right
    alt-enter
    alt-space
    alt-bspace  (alt-bs)
    alt-/
    tab
    btab        (shift-tab)
    esc
    del
    up
    down
    left
    right
    home
    end
    pgup        (page-up)
    pgdn        (page-down)
    shift-up
    shift-down
    shift-left
    shift-right
    left-click
    right-click
    double-click
    or any single character

Additionally,  a special  event named  change  is available  which is  triggered
whenever the query string is changed.

    $ fzf --bind change:top

### Action, Default Bindings (Notes)

    ┌──────────────────────┬─────────────────────────────────────────────────────────────┐
    │ abort                │ C-c  C-g  C-q  esc                                          │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ accept               │ enter   double-click                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ accept-non-empty     │ (same  as accept                                            │
    │                      │ except that it prevents fzf from exiting without selection) │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ backward-char        │ C-b  left                                                   │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ backward-delete-char │ C-h  bspace                                                 │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ backward-kill-word   │ M-bs                                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ backward-word        │ M-b   S-left                                                │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ beginning-of-line    │ C-a  home                                                   │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ cancel               │ (clears query string if not empty, aborts fzf otherwise)    │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ clear-screen         │ C-l                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ delete-char          │ del                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ delete-char/eof      │ C-d                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ deselect-all         │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ down                 │ C-j  C-n  down                                              │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ end-of-line          │ C-e  end                                                    │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ execute(...)         │ (see below for the details)                                 │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ execute-silent(...)  │ (see below for the details)                                 │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ execute-multi(...)   │ (deprecated in favor of {+} expression)                     │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ forward-char         │ C-f  right                                                  │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ forward-word         │ M-f   S-right                                               │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ ignore               │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ jump                 │ (EasyMotion-like 2-keystroke movement)                      │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ jump-accept          │ (jump and accept)                                           │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ kill-line            │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ kill-word            │ M-d                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ next-history         │ (C-n on `--history`)                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ page-down            │ pgdn                                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ page-up              │ pgup                                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ half-page-down       │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ half-page-up         │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ preview-down         │ S-down                                                      │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ preview-up           │ S-up                                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ preview-page-down    │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ preview-page-up      │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ previous-history     │ (C-p on `--history`)                                        │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ print-query          │ (print query and exit)                                      │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ replace-query        │ (replace query string with the current selection)           │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ select-all           │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle               │ (right-click)                                               │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-all           │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle+down          │ C-i  (tab)                                                  │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-in            │ (--layout=reverse* ? toggle+up : toggle+down)               │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-out           │ (--layout=reverse* ? toggle+down : toggle+up)               │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-preview       │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-preview-wrap  │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle-sort          │                                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ toggle+up            │ btab    (S-tab)                                             │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ top                  │ (move to the top result)                                    │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ unix-line-discard    │ C-u                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ unix-word-rubout     │ C-w                                                         │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ up                   │ C-k  C-p  up                                                │
    ├──────────────────────┼─────────────────────────────────────────────────────────────┤
    │ yank                 │ C-y                                                         │
    └──────────────────────┴─────────────────────────────────────────────────────────────┘

Multiple actions can be chained using `+` separator.

    $ fzf --bind 'ctrl-a:select-all+accept'

With `execute(...)` action,  you can execute arbitrary  commands without leaving
fzf.
For example, you can turn fzf into a simple file browser by binding enter key to
less command like follows.

    $ fzf --bind "enter:execute(less {})"

You can use the same placeholder expressions as in `--preview`.

If the command contains parentheses, fzf may fail to parse the expression.
In that case,  you can use any  of the following alternative  notations to avoid
parse errors.

    execute[...]
    execute~...~
    execute!...!
    execute@...@
    execute#...#
    execute$...$
    execute%...%
    execute^...^
    execute&...&
    execute*...*
    execute;...;
    execute/.../
    execute|...|
    execute:...

This is the special form that frees you  from parse errors as it does not expect
the closing character.
The catch  is that  it should  be the last  one in  the comma-separated  list of
key-action pairs.

fzf switches to the alternate screen when executing a command.
However,  if the  command  is expected  to  complete quickly,  and  you are  not
interested in  its output, you might  want to use execute-silent  instead, which
silently executes the command without the switching.
Note that fzf will not be responsive until the command is complete.
For asynchronous  execution, start  your command as  a background  process (i.e.
appending `&`).

##
##
##
# fzf-tmux
## Synopsis

    fzf-tmux [-u|-d [HEIGHT[%]]] [-l|-r [WIDTH[%]]] [--] [FZF OPTIONS]

## Description

fzf-tmux is a wrapper script for fzf that opens fzf in a tmux split pane.
It is designed to  work just like fzf except that it does  not take up the whole
screen.
You can safely use fzf-tmux instead of  fzf in your scripts as the extra options
will be silently ignored if you're not on tmux.

## Options
#### Layout

(default: `-d 50%`)

### -u [height[%]]

Split above (up).

### -d [height[%]]

Split below (down)

### -l [width[%]]

Split left

### -r [width[%]]

Split right

##
##
##
# ?

<https://www.reddit.com/r/vim/comments/6awwk5/configuring_fzf_preview/>

Essaye ça:

        fzf --preview 'cat {}'

Ça lance fzf en affichant pour chaque entrée sélectionnée une prévisualisation via `cat`.

# ?

Here's an example of integration of fzf in Vim.
We define a  custom command `:FzfSnippets` to fuzzy search  through our snippets
and their descriptions.
In practice,  it's useless if you  use `fzf.vim`, because the  latter installs a
similar command.
But I  keep this code here,  because it illustrates  how you can build  your own
commands.
It could also be useful to elminate `fzf.vim`.

Note that this code doesn't call any function from `fzf.vim`.
It relies on `fzf#run()` and `fzf#wrap()` which are installed in `~/.fzf/plugin/fzf.vim`.
The latter is installed by `fzf` itself.

    command! -bar -bang FzfSnippets call s:fzf_snippets(<bang>0)
    function! s:fzf_snippets(bang) abort
        let list = UltiSnips#SnippetsInCurrentScope()
        if empty(list)
            echohl WarningMsg | echom 'No snippets available here' | echohl None
        endif
        let aligned = sort(s:align_lists(items(list)))
        let colored = map(aligned, {i,v -> "\x1b[33m" . v[0] . "\x1b[m\t" . v[1]})
        call fzf#run(fzf#wrap('snippets', {
            \ 'source':  colored,
            \ 'options': '--ansi --tiebreak=index +m',
            \ 'sink':    function('s:inject_snippet')}, a:bang))
    endfunction
    function! s:align_lists(lists) abort
        let maxes = [0, 0]
        for list in a:lists
            call map(maxes, {i,v -> max([maxes[i], len(list[i])])})
        endfor
        for list in a:lists
            call map(list, {i,v -> printf('%-' . maxes[i] . 's', v)})
        endfor
        return a:lists
    endfunction
    function! s:inject_snippet(line) abort
        let snip = trim(split(a:line, "\t")[0])
        execute 'normal! a'.snip."\<c-r>=UltiSnips#ExpandSnippet()\<cr>"
    endfunction

# ?

When you install fzf, it comes with a Vim plugin (!= fzf.vim):

    ~/.fzf/plugin/fzf.vim

The latter  contains 2 public functions  which are used in  `fzf.vim` to install
custom Vim commands/mappings:

    fzf#run()
    fzf#wrap()

Those are  the only functions  you need  to understand how  to use, in  order to
install your own Vim commands/mappings.

There's one additional public function `fzf#shellescape()`, but it's useless.
It's just a wrapper around `shellescape()` which also supports Windows.

---

For more info about `fzf#wrap()`, see `:h fzf#wrap`:

   > By "wrapping" your options dictionary with `fzf#wrap` before passing it to
   > `fzf#run`, you can make your command also support the options.

##
##
##
# Issues
## “Failed to read /dev/tty”

It may be due to a regression in the kernel.

Try to update it.

Read these links for more info:

- <https://github.com/junegunn/fzf/issues/1486>
- <https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1813873>
- <https://wiki.ubuntu.com/Kernel/LTSEnablementStack>
- <https://wiki.ubuntu.com/Kernel/RollingLTSEnablementStack>

Wait for a kernel upgrade, or try this command:

    $ sudo apt-get install --install-recommends linux-generic-hwe-16.04

The code needs to be adapted to your current Ubuntu version.

---

If  you  also  installed  the  package  `xserver-xorg-hwe-16.04`,  and  you  get
distracting artifacts, read this:

<http://ubuntuhandbook.org/index.php/2017/02/install-remove-enablement-stacks-ubuntu-16-04/>

##
# Todo
## Simplify popup window implementation in fzf Vim plugin

Remember when @ichizok proposed a PR to prevent fzf from creating an extra process?
Here's what it looked like:
<https://github.com/junegunn/fzf/commit/07e8816ae830769dbece7ea9c7833967280eeadf>

It was  revised and  made more  complicated to  support the  case where  fzf was
invoked from a popup terminal.  It turns out that since 8.2.0791, you can't open
2 popup terminals  at the same time in  Vim anymore (which imo is  a good thing,
since it created too many issues).  So the original version of the PR is now good.

Maybe we should submit this simplified version as a PR.
If you  do, don't forget to  give all the credit  to @ichizok in the  git commit
message, since they are the original author.
Also,  make sure  not to  introduce a  regression; the  purpose of  the PR  from
@ichizok was to fix a bug; make sure it's still fixed.

Btw, this PR could also probably be undone: <https://github.com/junegunn/fzf/pull/1927>

---

Right now, we have an issue where the match created by `vim-sneak` when we press
sth like `fe`, is  not removed if we open the fzf  popup terminal without moving
the cursor before.

The issue comes from the fact that `WinLeave` is not fired:

    ~/.vim/plugged/vim-sneak/plugin/sneak.vim:254
    autocmd InsertEnter,WinLeave,BufLeave * call sneak#cancel()

We don't have this issue if we open our togglable popup terminal.
So, I suspect the issue is due to the current fzf implementation.
Once you submit your PR, make sure this issue is fixed.
If it is, open an issue on the fzf repo to increase the chances that the PR is merged.

##
## Read the README page.

<https://github.com/junegunn/fzf>

It seems that some settings are not documented anywhere else.
Like `FZF_COMPLETION_TRIGGER`.

## I have an issue with the fzf popup/floating window when invoking fzf from Vim!

You need to find a MWE.
Unfortunately, the  fzf and fzf.vim plugins  are very long, and  bisecting their
code can take a long time.

Here's a start; write this in `/tmp/vimrc`:

    " to avoid an error if you open a popup terminal on VimEnter;
    " netrw runs `:windo` on VimEnter which is forbidden while the focus is in a popup terminal
    let g:loaded_netrwPlugin = 1
    set rtp^=~/.fzf rtp-=~/.vim rtp-=~/.vim/after hidden
    " useful if you make the fzf Vim plugin just run the fzf binary;
    " in your home it would take too much time (because too many files)
    cd /tmp
    nno cd :call fzf#run()<cr>

In the fzf plugin, simplify the `fzf#run()` function definition like so:

    fu fzf#run(...) abort
      set shell=sh
      let dict = {'dir': '/tmp', 'window': {'width': 0.9, 'height': 0.6}}
      let temp = {'result': tempname()}
      let command = 'fzf >'..temp.result
      return s:execute_term(dict, command, temp)
    endfu

Finally, start Vim like this:

    $ vim -Nu /tmp/vimrc
    " press cd

You'll still have to bisect the  code in `s:execute_term()` and all script-local
functions it invokes; but if you can reproduce your issue with this code, then
you won't have to bisect:

   - your vimrc
   - the fzf.vim plugin
   - `fzf#wrap()`
   - `fzf#run()`

That's already a huge boost.

If it  doesn't work, try  to find  a better start,  and update the  code written
previously, so  that it's as  reliable as possible  for all fzf-related  bugs we
find in the future.

Also, try to bisect `s:execute_term()`, and  see whether we could remove it from
our generic MWE, so that we don't have to bisect it again and again after each bug.

In the  end, it would  be nice if  we had some generic  MWE from which  we could
quickly find another MWE for a Vim bug related to the popup/floating window, and
triggered by an fzf command.

---

Tip: Visually select a long function you want to simplify.
Then search for this pattern:

    \%V\%(end\)\@<!if

Below each match, write:

    let g:d_if_1 = 1
               ^
               increment the number after each match

Reproduce the issue, then, on the command-line, tab-complete `echo g:d_`.
Note the list of numbers which appear; e.g.:

    echo g:d_
    Tab
    echo g:d_if_2
    Tab
    echo g:d_if_5
    Tab
    echo g:d_if_8
    Tab
    echo g:d_

In this example, you know that only `d_if_2`, `d_if_5` and `d_if_8` have been created.
Remove any `if/elseif` block/clause containing  a line with a `d_if_N` variable,
`N` being a number different than `2`, `5` and `8`.

If you set `'wildmenu'`, you probably won't have to press Tab more than once.

---

Pitfall:  You may find out that after  removing `setf fzf`, pressing `Esc` in an
fzf buffer doesn't close its window anymore.
This is because of `vim-terminal` which installs these autocmds:

    au TerminalWinOpen * tno <buffer><nowait><silent> <esc><esc> <c-\><c-n>:call terminal#fire_termleave()<cr>
    au FileType fzf tunmap <buffer> <esc><esc>

The first one installs a mapping all terminal buffers; the second one removes it
in fzf buffers.  If  you don't set the filetype to fzf,  it's no longer removed,
which explains this issue.

Solution: as long  as you start Vim  with `vim-terminal`, make sure  to run this
command in an fzf buffer:

    sil! tunmap <buffer> <esc><esc>

Write  it  –  for  example  –  right after  this  line  (which  starts  fzf)  in
`s:execute_term()`:

    let fzf.buf = term_start([&shell, &shellcmdflag, command], {'curwin': 1, 'exit_cb': function(fzf.on_exit)})

---

The creation of the popup window results from this chain of function calls:

    fzf#run() → s:execute_term() → s:split() → s:popup() → s:create_popup() → popup_create()

## fzf integration is slow!

In  `~/.config/ranger/commands.py`, we  define the  `fzf_select` ranger  command
which relies on the `find(1)` shell command.
We map it  to `zz`, and the nearer  you're from the root of  the filesystem, the
slower fzf is.
Maybe we could make `zz` faster if we used `fd(1)` instead.
Learn the syntax of `fd(1)`, and try to adapt the code.

## Create commands to fuzzy search the changelist and other kind of lists

## Create mapping to fuzzy search old commit messages

It would be handy to paste an old commit messages.
Easier  than blindly  pressing `[m`  or `]m`  (custom mappings)  in a  gitcommit
buffer until we stumble upon the one we're looking for.
Since  commit messages  may be  multiline, try  to enable  the preview  pane (to
preview the files where the old commit messages are saved).

## To read

- <https://medium.com/@vdeantoni/boost-your-command-line-productivity-with-fuzzy-finder-985aa162ba5d>
- <http://blog.owen.cymru/fzf-ripgrep-navigate-with-bash-faster-than-ever-before/>
- <https://bluz71.github.io/2018/11/26/fuzzy-finding-in-bash-with-fzf.html>
- <https://bluz71.github.io/2018/12/04/fuzzy-finding-in-vim-with-fzf.html>

## Learn how to customize fzf options via `_fzf_comprun`.

<https://github.com/junegunn/fzf/commit/52154153150d0014a76ef8b429b73c590cb7f755>

## It would be nice to be able to fuzzy search through old commit messages.

See our todo in:

    ~/.vim/plugged/vim-git/after/ftplugin/gitcommit.vim

## Fix E861 when fzf is invoked from popup terminal

Invoke an fzf command from a popup terminal, and you'll get the error `E861`:

    Error detected while processing TerminalOpen Autocommands for "*":
    E861: Cannot open a second popup with a terminal
    Error detected while processing function <SNR>53_history:
    line    7:
    E171: Missing :endif

`s:split()` invoked  by `fzf#run()` should bail  out when it finds  out that the
currently focused window is a popup terminal:

    diff --git a/plugin/fzf.vim b/plugin/fzf.vim
    index 06ef99a..6a141a4 100644
    --- a/plugin/fzf.vim
    +++ b/plugin/fzf.vim
    @@ -655,6 +655,10 @@ function! s:split(dict)
             if !has('nvim') && !has('patch-8.2.191')
               throw 'Vim 8.2.191 or later is required for pop-up window'
             end
    +        " `:sil!` because if the current window is not a popup window, `E993` is raised
    +        sil! if !has('nvim') && !empty(popup_getoptions(win_getid()))
    +            throw 'E861: Cannot open a second popup with a terminal'
    +        endif
             call s:popup(a:dict.window)
             let is_popup = 1
           else

This patch is *probably* what @junegunn would want.
It fits  well in the  current code (notice how  the previous `:throw`  handles a
somewhat similar issue).  But I don't like  this patch; it makes the stack trace
even more verbose:

    Error detected while processing function <SNR>53_history[7]..fzf#vim#history[1]..<SNR>167_fzf[18]..fzf#run[58]..<SNR>52_execute_term[3]..<SNR>52_split:
    line   16:
    E605: Exception not caught: E861: Cannot open a second popup with a terminal
    Error detected while processing function <SNR>53_history:
    line    7:
    E171: Missing :endif

When you re-implement the fzf *Vim* plugin  (not the fzf binary), make sure your
code just bail out when a popup terminal is currently open.
Also, use `win_gettype()` to make the code simpler:

    if win_gettype() is# 'popup'
        return
    endif

## ?

Document that the equivalent of this shell command:

    $ fzf --preview 'cat {}'

Inside Vim is:

    :FZF --preview cat\ {}

This is because `:FZF` uses the escape sequence `<f-args>`:

    command! -nargs=* -complete=dir -bang FZF call s:cmd(<bang>0, <f-args>)

This means that Vim splits here:

    :FZF --preview 'cat {}'
                  ^    ^
                  ✔    ✘

To prevent the second split, you need to escape the space:

    :FZF --preview 'cat\ {}'
                       ^

But `<f-args>` still quotes the string  `'cat {}'` a second time, which prevents
the shell from splitting `cat(1)` from the file argument; remove the quotes, and
let Vim quote `cat {}` when replacing `<f-args>`:

    :FZF --preview cat\ {}

## ?

Install some shell functions which run filter some frequently used commands with
fzf.  Similar to what `C-g C-g` does.
The idea being that `C-g C-g` could grow too much over time; we may need to move
all commands linked to a similar topic (git, compilation, debugging, ...) behind
a shell function with a telling name.

## ?

Use fzf (and/or fzf.vim) to create a mapping which would fuzzy search inside our
abbreviations (including their {rhs}).
It would be useful in a case such as this:

   > What's the abbreviation which expands into  a command to search a character in
   > the unicode table?

    {fzf mapping} → type keyword `unicode` → look for the right abbreviation
                                           → `:ucs`

## ?

Atm, `:FzFiles` doesn't search hidden files/directories.

Solution:

    :let $FZF_DEFAULT_COMMAND = 'ag --hidden --ignore .git -g ""'

See also: <https://github.com/junegunn/fzf.vim/issues/226>

