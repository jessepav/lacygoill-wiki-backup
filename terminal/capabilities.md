# Basic

    ┌──────────┬─────────────────────────────────────────┐
    │ am       │ does automatic margins                  │
    ├──────────┼─────────────────────────────────────────┤
    │ bw       │ cub1 wraps from column 0 to last column │
    ├──────────┼─────────────────────────────────────────┤
    │ ul       │ can underline                           │
    ├──────────┼─────────────────────────────────────────┤
    │ bel=^G   │ the key to ring the bell is C-g         │
    ├──────────┼─────────────────────────────────────────┤
    │ cols#80  │ the screen has 80 columns               │
    ├──────────┼─────────────────────────────────────────┤
    │ lines#24 │ the screen has 24 lines                 │
    └──────────┴─────────────────────────────────────────┘

## What does `am` mean?

When the end of a line is reached, an automatic carriage return and line-feed is
performed.

## What does `bw` mean?

Theory: when  you move the  cursor back from  column 0, you  end up on  the last
column of the previous line.

Mnemonic: BackWards

##
# Cursor motion
## What are the coordinates of "home" for an X terminal?

    (1,1)

##
## absolute

    ┌───────────────────────┬──────────────────────────────────────┐
    │ smcup                 │ sequence to start programs using cup │
    ├───────────────────────┼──────────────────────────────────────┤
    │ rmcup                 │ sequence to end programs using cup   │
    ├───────────────────────┼──────────────────────────────────────┤
    │ cup=\E[%i%p1%d;%p2%dH │ absolute cursor motion               │
    └───────────────────────┴──────────────────────────────────────┘

`smcup` makes the terminal enter a mode  in which the programs can use the `cup`
capability (absolute cursor motion).
In Vim's builtin termcap db, it's called `t_ti`, which contains one of the first
sequence sent to the terminal.

`rmcup` makes the terminal leave this mode.
In Vim's builtin termcap db , it's called `t_te`, which contains one of the last
sequence sent to the terminal.

### What is `cup`?

The cursor motion capabilitiy.
It describes how to move the cursor directly to a specific location.

#### How is it different from most other capabilities?

Since the desired location is specified by a program at run time, the capability
must provide some mechanism for describing arguments.
The program uses this  description to figure out *what* string  it needs to send
to move the cursor to the desired location.

So, simple string capabilities tell what string to send, while `cup` – and other
string capabilities  with arguments – tell  the program *how to  calculate* what
string to send.

#### Which special character does it rely on?

The "%" escape character.

#### What is the data structure used by a terminal to process a `cup` string?

A stack which is manipulated like a Reverse Polish Notation calculator.
Arguments or constants are pushed onto  the stack, manipulated and combined, and
a single final result is output (popped from the stack).

#### Break down this value `\E[%i%p1%d;%p2%dH`.

`\E` is an escape character, while `[`, `;` and `H` are literal characters.

`%i%p1%d` and `%p2%d` encode the coordinates of the new desired cursor location.

`%i` increments the values given by one.
This is  necessary for X  terminals whose  home is based  on upper left  = (1,1)
rather than (0,0).
`%p1` pushes the first parameter onto the stack.
`%d` pops the  value as a signed  decimal number, and the  number is incremented
because of `%i`.

`%p2` pushes the second parameter onto the stack.
`%d` pops the  value as a signed  decimal number, and the  number is incremented
because of `%i`.

For more info, see page 31 of “Termcap and Terminfo” (40 of the original book).

##
## relative

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

##
# Arrow keys

    ┌────────────┬─────────────────┐
    │ kcud1=\EOB │ down  arrow key │
    ├────────────┼─────────────────┤
    │ kcuu1=\EOA │ up    arrow key │
    ├────────────┼─────────────────┤
    │ kcub1=\EOD │ left  arrow key │
    ├────────────┼─────────────────┤
    │ kcuf1=\EOC │ right arrow key │
    └────────────┴─────────────────┘

## What's the difference between `kcuu1` and `cuu1`?

`cuu1` tells a program which string to *send* to move the cursor 1 line up.

`kcuu1` tells a program which string it will *receive* when the user has pressed
the up arrow key.
The latter  could move the  cursor 1 line  up, or could  be mapped to  some user
custom function.

---

Read “Termcap and Terminfo”, page 89 (156 of the original book).

I think this excerpt applies to capabilities prefixed by `k`:
> [...] not listing  a key may cause  serious problems while running  a program if
> the unlisted key were accidentally hit.
> The  program will  not be  able to  translate the  sequence into  a recognizable
> function key  sequence and will  be forced to interpret  the sequence as  if the
> characters had been typed, which may be disastrous.

> Many of these  capabilities have "twin" capabilities elsewhere  in termcap and
> terminfo.
> For example, in  termcap, kC= specifies the  code sent by the  CLEAR SCREEN key,
> and cl= is the string that programs use to clear the screen.
> The capabilities in this section describe what is sent when a key is pressed, so
> that programs know what  special keys are available and to  realize when one has
> been pressed.
> The twin capabilities for each of  these keys (described elsewhere in this book)
> are the  functional capabilities, which  is how  programs learn what  strings to
> send to produce the desired action.

> Although  in most  cases the  twins will  be identical  twins, there  are a  few
> reasons and special cases where the twins will not be identical.
> [...] you might want to [...] use the keys to indicate something other than they
> say on them (for  example, using the arrow keys for  something other than moving
> the cursor in application programs).
> In these cases, your program would turn  off echoing and watch the input for the
> characters sent by the redefined keys.
> [...] Thus,  while it is  often redundant to  have twin capabilities,  there are
> cases when it is useful, and it is historically ingrained.

When the  excerpt uses  the word  “echo”, I think  it refers  to the  fact that,
often, when you press a non-function key  like `a`, the terminal sends it to the
program, and then the  program sends it back to the terminal to  write it on the
screen; in this sense, it echoes the character:

             message: the user has pressed `a`
             v
    terminal → editor
    terminal ← editor
             ^
             message: ok, write it as is

## What happens if `kcuu1` is not properly set?

When the user presses the up arrow key, each key in the emitted sequence will be
processed independently.

As an experiment, run this in Vim:

    :set t_ku=

Then, press the up arrow key in normal mode.
The `A` character is inserted above the current line.
This is because, pressing the up arrow  key makes the terminal send the sequence
`Esc O A`, and  without `'t_ku'` being properly set, Vim  is unable to recognize
this sequence.

---

But why can't I reproduce this experiment for the shell?

    $ infocmp -x >entry
    $ vim entry
    :%s/kcuu1=\zs[^,]*//
    :x
    $ tic -sx entry

Press the up key: it still correctly recalls the previous command!

I think that's because the shell is not a TUI application.
This is explained here:
<https://invisible-island.net/xterm/xterm.faq.html#xterm_arrows>

> Since   termcaps  and   terminfo  descriptions   are  written   for  full-screen
> applications,  shells and  similar programs  often  rely on  **built-in tables**  of
> escape sequences which they use instead.
> Defining keys  in terms of  the termcap/terminfo  entry (e.g., by  capturing the
> string sent by tputs) is apt to confuse the shell.

##
# Clearing

    ┌────────────────┬─────────────────────────┐
    │ clear=\E[H\E[J │ clear the screen        │
    ├────────────────┼─────────────────────────┤
    │ ed=\E[J        │ clear to end of display │
    ├────────────────┼─────────────────────────┤
    │ el=\E[K        │ clear to end of line    │
    └────────────────┴─────────────────────────┘

# Adding and deleting

    ┌───────────┬────────────────────┐
    │ dch1=\E[P │ delete 1 character │
    ├───────────┼────────────────────┤
    │ dl1=\E[M  │ delete 1 line      │
    ├───────────┼────────────────────┤
    │ ich1=\E[@ │ insert 1 character │
    ├───────────┼────────────────────┤
    │ il1=\E[L  │ insert 1 line      │
    └───────────┴────────────────────┘

# Styles

Standout mode:

    ┌─────────────┬─────────────────────┐
    │ smso=\E[3m  │ start standout mode │
    ├─────────────┼─────────────────────┤
    │ rmso=\E[23m │ exit standout mode  │
    └─────────────┴─────────────────────┘

Memotechnics:

smso = Starts  Mode StandOut
rmso = Removes Mode StandOut

---

Underline mode:

    ┌─────────────┬──────────────────────┐
    │ smul=\E[4m  │ start underline mode │
    ├─────────────┼──────────────────────┤
    │ rmul=\E[24m │ exit underline mode  │
    └─────────────┴──────────────────────┘

# Function key definitions

    ┌──────────┬────────┐
    │ kf1=\EOP │ F1 Key │
    ├──────────┼────────┤
    │ kf2=\EOQ │ F2 Key │
    ├──────────┼────────┤
    │ kf3=\EOR │ F3 Key │
    ├──────────┼────────┤
    │ ...      │ ...    │
    └──────────┴────────┘

#
# Terminfo Extensions
## What's a terminfo extension?

An extended capability not found in standard terminfo, which was first supported
in xterm, and later may have been implemented in other terminals.

### How can I list all of them?

    $ infocmp -x xterm+tmux
    #       Reconstructed via infocmp from file: /home/user/.terminfo/x/xterm+tmux~
    xterm+tmux|advanced xterm features used in tmux,~
            Cr=\E]112\007, Cs=\E]12;%p1%s\007,~
            Ms=\E]52;%p1%s;%p2%s\007, Se=\E[2 q, Ss=\E[%p1%d q,~

Here, you can see 5 capabilities:

   - Cr
   - Cs
   - Ms
   - Se
   - Ss

##
## What's `Ms`?

It's a  way for the terminal  to tell the  applications (such as tmux)  how they
should encode and send  some arbitrary text, if they want  the terminal to store
it into the clipboard.

### Where can I find more information about it?

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ vim terminfo.src
    /\m\C\<Ms\>

### What's its default value?

    Ms=\E]52;%p1%s;%p2%s\007

#### What's the meaning of the two parameters?

   - p1 = the storage unit (clipboard, selection or cut buffer)
   - p2 = the base64-encoded clipboard content.

##
# Miscellaneous
## What are the different types of terminal capabilities?

There are 3 types of capabilities, depending on the type of values they receive:

    ┌─────────┬─────────┬─────────────────────────────────────────┐
    │ type    │ example │                 meaning                 │
    ├─────────┼─────────┼─────────────────────────────────────────┤
    │ boolean │ am      │ does automatic margins                  │
    ├─────────┼─────────┼─────────────────────────────────────────┤
    │ numeric │ cols#80 │ the terminal has 80 columns             │
    ├─────────┼─────────┼─────────────────────────────────────────┤
    │ string  │ cuu1=^K │ the sequence `C-k` will move the cursor │
    │         │         │ up one line                             │
    └─────────┴─────────┴─────────────────────────────────────────┘

### How to infer the type of a capability from its name?

If it contains:

   - `#`, it's a numeric one
   - `=`, it's a string one
   - neither `#` nor `=`, it's a boolean one

##
## How to insert a control character when you edit an entry of the terminfo db?

Use the caret notation.

Do *not* insert the character literally.
For example, to express `C-k`, you must *not* press `C-v C-k` in Vim.
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

The screen is saved with `$ tput smcup`, then restored with `$ tput rmcup`.

Saving/restoring the screen  is not the primary purpose of  `smcup` and `rmcup`;
it's just a – here useful – side-effect.
The purpose of these capabilities is to  make the terminal enter/leave a mode in
which the programs can use the `cup` capability.

`$ clear` is used to move the cursor back to home.

