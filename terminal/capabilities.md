# Terminfo capabilities
## Basic

    ┌──────────┬─────────────────────────────────────────┐
    │ lines#24 │ screen has 24 lines                     │
    ├──────────┼─────────────────────────────────────────┤
    │ cols#80  │ screen has 80 columns                   │
    ├──────────┼─────────────────────────────────────────┤
    │ am       │ does automatic margins                  │
    ├──────────┼─────────────────────────────────────────┤
    │ bel=^G   │ C-g rings the bell                      │
    ├──────────┼─────────────────────────────────────────┤
    │ bw       │ cub1 wraps from column 0 to last column │
    ├──────────┼─────────────────────────────────────────┤
    │ gn       │ generic device                          │
    ├──────────┼─────────────────────────────────────────┤
    │ ul       │ can underline                           │
    └──────────┴─────────────────────────────────────────┘

`am` means that when the end of  a line is reached, an automatic carriage return
and line-feed is performed.

`bw` = BackWards

`gn` tells the  program which queries the  db, that it's working  with a generic
entry, and so if  it's unable to perform a task, it can  ask the user to specify
what terminal type they are really using.

## Cursor motion

    Absolute:
    ┌───────────────────────┬──────────────────────────────────────┐
    │ smcup                 │ sequence to start programs using cup │
    ├───────────────────────┼──────────────────────────────────────┤
    │ rmcup                 │ sequence to end programs using cup   │
    ├───────────────────────┼──────────────────────────────────────┤
    │ cup=\E[%i%p1%d;%p2%dH │ absolute cursor motion               │
    └───────────────────────┴──────────────────────────────────────┘

`smcup` makes the terminal enter a mode  in which the programs can use the `cup`
capability (absolute cursor motion).
In Vim's builtin termcap db, it's called 't_ti', which contains one of the first
sequence emitted to the terminal.

`rmcup` makes the terminal leave this mode.
In Vim's builtin termcap db , it's called 't_te', which contains one of the last
sequence emitted to the terminal.

TODO: break `cup` down.


    Relative:
    ┌───────────┬───────────────────────────────────────────────┐
    │ cbt=\E[Z  │ backtab                                       │
    ├───────────┼───────────────────────────────────────────────┤
    │ cr=^M     │ return                                        │
    ├───────────┼───────────────────────────────────────────────┤
    │ cub1=^H   │ move CUrsor Back 1 column                     │
    ├───────────┼───────────────────────────────────────────────┤
    │ cuf1=\E[C │ move CUrsor Forward 1 column                  │
    ├───────────┼───────────────────────────────────────────────┤
    │ cud1=^J   │ move CUrsor Down 1 line                       │
    ├───────────┼───────────────────────────────────────────────┤
    │ cuu1=\EM  │ move CUrsor Up 1 line                         │
    ├───────────┼───────────────────────────────────────────────┤
    │ home=^^   │ move cursor home                              │
    ├───────────┼───────────────────────────────────────────────┤
    │ ht=^I     │ move cursor to next 8-space hardware tab stop │
    ├───────────┼───────────────────────────────────────────────┤
    │ ind=^J    │ scroll forward                                │
    │ ri=\EI    │ scroll backward                               │
    ├───────────┼───────────────────────────────────────────────┤
    │ kbs=\177  │ backspace key                                 │
    │           │ (177 is the octal code of C-?)                │
    ├───────────┼───────────────────────────────────────────────┤
    │ nel=\EE   │ newline (behaves like cr followed by lf)      │
    └───────────┴───────────────────────────────────────────────┘

## Arrow keys

    ┌────────────┬─────────────────┐
    │ kcud1=\EOB │ down  arrow key │
    ├────────────┼─────────────────┤
    │ kcuu1=\EOA │ up    arrow key │
    ├────────────┼─────────────────┤
    │ kcub1=\EOD │ left  arrow key │
    ├────────────┼─────────────────┤
    │ kcuf1=\EOC │ right arrow key │
    └────────────┴─────────────────┘

What's the difference between `kcud1` and `cud1`?

Theory:

`cud1` is used when a program needs to know how to move the cursor 1 line down.

`kcud1` is used when a program needs to  know when the user has pressed the down
arrow key.
The latter could  move the cursor 1 line  down, or could be mapped  to some user
custom function.

## Clearing

    ┌────────────────┬─────────────────────────┐
    │ clear=\E[H\E[J │ clear the screen        │
    ├────────────────┼─────────────────────────┤
    │ ed=\E[J        │ clear to end of display │
    ├────────────────┼─────────────────────────┤
    │ el=\E[K        │ clear to end of line    │
    └────────────────┴─────────────────────────┘

## Adding and deleting

    ┌───────────┬────────────────────┐
    │ dch1=\E[P │ delete 1 character │
    ├───────────┼────────────────────┤
    │ dl1=\E[M  │ delete 1 line      │
    ├───────────┼────────────────────┤
    │ ich1=\E[@ │ insert 1 character │
    ├───────────┼────────────────────┤
    │ il1=\E[L  │ insert 1 line      │
    └───────────┴────────────────────┘

## Styles

    Standout mode:
    ┌─────────────┬─────────────────────┐
    │ smso=\E[3m  │ start standout mode │
    ├─────────────┼─────────────────────┤
    │ rmso=\E[23m │ exit standout mode  │
    └─────────────┴─────────────────────┘

Memotechnics:

smso = Starts  Mode StandOut
rmso = Removes Mode StandOut


    Underline mode:
    ┌─────────────┬──────────────────────┐
    │ smul=\E[4m  │ start underline mode │
    ├─────────────┼──────────────────────┤
    │ rmul=\E[24m │ exit underline mode  │
    └─────────────┴──────────────────────┘

## Function key definitions

    ┌──────────┬────────┐
    │ kf1=\EOP │ F1 Key │
    ├──────────┼────────┤
    │ kf2=\EOQ │ F2 Key │
    ├──────────┼────────┤
    │ kf3=\EOR │ F3 Key │
    ├──────────┼────────┤
    │ ...      │ ...    │
    └──────────┴────────┘

## What's the meaning of a capability whose description matches 'X key'?

When you read a description such as 'do_X', it answers the question:

>     Which sequence must I SEND TO the terminal to use the functionality X?
>                         │
>                         └ the program querying the terminfo db

When you read a description such as 'X key', it answers the question:

>     Which sequence will I RECEIVE FROM the terminal if the user presses the key X?

#
# Termcap capabilities
## Basic

    ┌───────┬──────────────────────────────────┐
    │ li#24 │ screen has 24 lines              │
    ├───────┼──────────────────────────────────┤
    │ co#80 │ screen has 80 columns            │
    ├───────┼──────────────────────────────────┤
    │ am    │ automatic margin                 │
    ├───────┼──────────────────────────────────┤
    │ bl=^G │ C-g rings the bell               │
    ├───────┼──────────────────────────────────┤
    │ bs    │ C-h performs a backspace         │
    ├───────┼──────────────────────────────────┤
    │ bw    │ can backspace to previous line   │
    ├───────┼──────────────────────────────────┤
    │ gn    │ generic device                   │
    ├───────┼──────────────────────────────────┤
    │ ul    │ can underline but not overstrike │
    └───────┴──────────────────────────────────┘

## Cursor motion

    Absolute:
    ┌─────────────┬────────────────────────────┐
    │ cm=\E=%+ %+ │ sequence for cursor motion │
    │             │                            │
    │             │ Esc                        │
    │             │ =                          │
    │             │ the desired row            │
    │             │ a space                    │
    │             │ the desired column         │
    └─────────────┴────────────────────────────┘

TODO:
better break it down; what does `%+` mean?


    Relative:
    ┌────────┬────────────────────────────────────┐
    │ cr=^M  │ carriage return                    │
    ├────────┼────────────────────────────────────┤
    │ nd=^L  │ move cursor 1 char to the right    │
    ├────────┼────────────────────────────────────┤
    │ up=^K  │ move cursor up 1 line              │
    ├────────┼────────────────────────────────────┤
    │ do=^J  │ move cursor down                   │
    ├────────┼────────────────────────────────────┤
    │ ho=^^  │ move cursor home                   │
    ├────────┼────────────────────────────────────┤
    │ ta=^I  │ move to the next hardware tab      │
    ├────────┼────────────────────────────────────┤
    │ bt=\EI │ move to previous tabstop (backtab) │
    ├────────┼────────────────────────────────────┤
    │ sr=\EI │ scroll backwards one line          │
    └────────┴────────────────────────────────────┘

## Arrow keys

    ┌───────┬─────────────────┐
    │ kl=^H │ Left arrow Key  │
    ├───────┼─────────────────┤
    │ kr=^L │ Right arrow Key │
    ├───────┼─────────────────┤
    │ ku=^K │ Up arrow Key    │
    ├───────┼─────────────────┤
    │ kd=^J │ Down arrow Key  │
    ├───────┼─────────────────┤
    │ kb=^H │ Backspace Key   │
    ├───────┼─────────────────┤
    │ kh=^^ │ Home Key        │
    └───────┴─────────────────┘

## Clearing

    ┌───────────┬───────────────────────────────────────┐
    │ cd=\EJ    │ clear after cursor to end of screen   │
    ├───────────┼───────────────────────────────────────┤
    │ ce=\EK    │ clear to eol                          │
    ├───────────┼───────────────────────────────────────┤
    │ cl=\EH\EJ │ clear screen and moves cursor to home │
    └───────────┴───────────────────────────────────────┘

## Adding and deleting

    ┌────────┬─────────────────────────────┐
    │ al=\EE │ add 1 line above cursor     │
    ├────────┼─────────────────────────────┤
    │ dl=\ER │ delete current line         │
    ├────────┼─────────────────────────────┤
    │ ic=\EQ │ insert a single blank space │
    ├────────┼─────────────────────────────┤
    │ dc=\EW │ delete character at cursor  │
    └────────┴─────────────────────────────┘

## Styles

    Standout Mode:
    ┌─────────┬─────────────────────────────────┐
    │ so=\EG4 │ start standout mode             │
    ├─────────┼─────────────────────────────────┤
    │ se=\EG0 │ end standout mode               │
    ├─────────┼─────────────────────────────────┤
    │ sg#1    │ when changing to standout mode, │
    │         │ 1 additional space is output    │
    │         │                                 │
    │         │ Standout Glitch                 │
    └─────────┴─────────────────────────────────┘

    Underline:
    ┌─────────┬──────────────────────────────────┐
    │ us=\EG8 │ start underline mode             │
    ├─────────┼──────────────────────────────────┤
    │ ue=\EG0 │ end underline mode               │
    ├─────────┼──────────────────────────────────┤
    │ ug#1    │ when changing to underline mode, │
    │         │ 1 additional space is output     │
    │         │                                  │
    │         │ Underline Glitch                 │
    └─────────┴──────────────────────────────────┘

## Function key definitions

    ┌──────────┬────────┐
    │ k1=^A@^M │ F1 Key │
    ├──────────┼────────┤
    │ k2=^AA^M │ F2 Key │
    ├──────────┼────────┤
    │ k3=^AB^M │ F3 Key │
    ├──────────┼────────┤
    │ ...      │ ...    │
    └──────────┴────────┘

#
# Miscellaneous
## What are the different types of terminal capabilities?

There are 3 types of capabilities, depending on the type of values they receive:

    ┌─────────┬───────────────────┬────────────────────┬─────────────────────────────────────────┐
    │ type    │ example (termcap) │ example (terminfo) │                  meaning                │
    ├─────────┼───────────────────┼────────────────────┼─────────────────────────────────────────┤
    │ boolean │ am                │ am                 │ does automatic margins                  │
    ├─────────┼───────────────────┼────────────────────┼─────────────────────────────────────────┤
    │ numeric │ co#80             │ cols#80            │ the terminal has 80 columns             │
    ├─────────┼───────────────────┼────────────────────┼─────────────────────────────────────────┤
    │ string  │ up=^K             │ cuu1=^K            │ the sequence `C-k` will move the cursor │
    │         │                   │                    │ up one line                             │
    └─────────┴───────────────────┴────────────────────┴─────────────────────────────────────────┘

## How to insert a control character when you edit an entry of the terminfo db?

Use the caret notation.

Do NOT insert the character literally.
For example, to  express `C-k`, you must NOT  press `C-v C-k` in Vim.
Instead, insert the 2 characters `^` and `K`.

## How to express common unprintable characters?

    ┌──────────────────────────────────────┬─────────────────────────┐
    │ C-x                                  │ ^X                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ escape                               │ \E                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ backspace                            │ \b                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ formfeed                             │ \f                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ linefeed                             │ \l                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ newline                              │ \n                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ return                               │ \r                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ space                                │ \s                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ tab                                  │ \t                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ character whose octal value is `123` │ \123                    │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ null                                 │ \0    \000 doesn't work │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ caret                                │ \^                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ backslash                            │ \\                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ comma                                │ \,                      │
    ├──────────────────────────────────────┼─────────────────────────┤
    │ colon                                │ \:                      │
    └──────────────────────────────────────┴─────────────────────────┘

Some of them are specific to terminfo, or have another representation in termcap.
See page 20 in the book `Termcap and Terminfo` (O'Reilly).

## How to temporarily clear the screen while executing arbitrary code?

        $ tput smcup
        $ clear
        # arbitrary code
        $ tput rmcup

The screen is saved with `tput smcup`, then restored with `tput rmcup`.

Saving/restoring the screen  is not the primary purpose of  `smcup` and `rmcup`;
it's just a (here useful) side-effect.
The purpose of these capabilities is to  make the terminal enter/leave a mode in
which the programs can use the `cup` capability.

`clear` is used to move the cursor back to home.

