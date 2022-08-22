# a
## alternate screen

The alternate screen is used by many interactive programs such as vim, htop, less ...
It's like a different buffer of  the terminal content, which disappears when the
application exits,  so the whole  terminal gets restored  and it looks  like the
application hasn't output anything.

In  the alternate  screen,  the scrollback  buffer is  disabled  to prevent  the
interactive program from messing it up.

It can be manually entered by running `$ tput smcup`.
And you can leave it by running `$ tput rmcup`.

See:

   - <https://github.com/tmux/tmux/issues/1795#issuecomment-502384443>
   - <https://stackoverflow.com/questions/11023929/using-the-alternate-screen-in-a-bash-script>

See also `man tmux /alternate-screen`:

   > This  option configures  whether  programs  running inside  the  pane may  use
   > the  terminal alternate  screen  feature,  which allows  the  smcup and  rmcup
   > terminfo(5) capabilities.
   > The  alternate screen  feature  preserves the  contents of  the  window when  an
   > interactive  application starts  and restores  it on  exit, so  that any  output
   > visible before the application starts reappears unchanged after it exits.

##
# b
## bit/baud rate

    bit rate = bits per second
    baud rate = symbols per second

In digital  communications, the baud  rate is the  number of symbol  changes, or
waveform changes, across the transmission medium per time unit.

The symbol rate is measured in baud (Bd) or symbols per second.

Each symbol can convey one or several bits of data.
The symbol rate is related to the bitrate expressed in bits per second.

For example, if each symbol conveys 5 bits of information, then:

    bitrate = 5 * baud rate

---

How can a symbol convey several bits?
Imagine you can communicate with somebody via a deck of 32 cards.

    1 bit  can ONLY express 2  information.
    2 bits "                4  "
    3 bits "                8  "
    4 bits "                16 "
    5 bits "                32 "

You need at least 5 bits to encode any card of the deck.
So, every card conveys 5 bits.


Another way of looking at it:

The more complex a system is (ex: a deck of cards),
the more symbols you need to describe its state (ex: a picked card),
the more bits you would need to do the same thing as your symbols.

There are only TWO bits.
So, as soon as you have a system  with more than two states, you need to COMBINE
bits  to make  up for  the lack  of  expressiveness of  this very  small set  of
symbols:  {0,1}


Yet another way of looking at it:

A symbol EXPRESSES a state of the system:  it has meaning (it's like a word).
A bit is just a COMPONENT of a symbol:     it has no meaning (it's like a letter in a word).

##
# c
## CSI

Control Sequence Introducer:  ESC [

   - <https://en.wikipedia.org/wiki/C0_and_C1_control_codes>
   - <https://vt100.net/docs/vt510-rm/chapter4.html#S4.3.3>
   - <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-C1-_8-Bit_-Control-Characters>

## capability

It can refer both  to an actual terminal characteristic (ex:  number of lines on
the screen), and to the terminfo syntax for describing that characteristic.

There's no canonical list of capabilities.
IOW, a  terminal can invent a  non-standard capability, found nowhere  else, for
some special need.
But the terminal has to respect some convention to describe it.

## curses

Higher-level subroutine, similar to `terminfo`,  whose purpose is to make easier
for developers to write terminal-independent programs.

The name “curses” comes from “cursor manipulation”.

##
# d
## DCS

Device Control String:  Esc P

- <https://en.wikipedia.org/wiki/C0_and_C1_control_codes>
- <https://vt100.net/docs/vt510-rm/chapter4.html#S4.3.4>
- <http://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-C1-_8-Bit_-Control-Characters>

## device file

Interface to  a device driver  that appears in  a file system  as if it  were an
ordinary file.

It allows an application  program to interact with a device  by using its device
driver via standard input/output system calls.

Using  standard  system  calls  simplifies many  programming  tasks,  and  leads
to  consistent  user-space I/O  mechanisms  regardless  of device  features  and
functions.

## ?

device type

In general, in order to obtain a file descriptor to some device, a process would
open a device file living in `/dev`.

Each  such device  is  either  a block  device  (buffered)  or character  device
(unbuffered), and if a single device can  act as either block or character, then
there will be two device nodes for that file: one block, one character.

Each device node also has an associated major and minor device type number.

If you rename a  device node, it'll still refer to the  same device, because the
major and minor numbers determine which device it refers to.

You can see the major and minor numbers in the output of stat(1):

    $ stat /dev/... | awk -F': ' '/Device type/{print $NF}'

##
# o
## OSC

Operating System Command:  Esc ]

- <https://en.wikipedia.org/wiki/C0_and_C1_control_codes>
- <https://vt100.net/docs/vt510-rm/chapter4.html#S4.5>
- <http://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-C1-_8-Bit_-Control-Characters>

##
# p
## *Pm*

A  multiple  numeric  parameter  composed   of  any  number  of  single  numeric
parameters, separated by ; character(s).
Individual values for the parameters are listed with Ps.

## *Ps*

selective Parameter

It is a single numeric parameter.
It selects an action associated with the specific parameter.

- <https://vt100.net/docs/vt510-rm/chapter4.html#S4.3.3.2>
- <http://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Definitions>

## *Pt*

A text parameter composed of printable characters.
For a color, it could be a name (red), or a hex number.

##
## parity check / bit

A parity bit is a bit added to a  string of binary code to ensure that the total
number of 1-bits in the string is even (or odd).

The check makes sure that the number of 1-bits is even (or odd).

Parity bits are used as the simplest form of error detecting code.

##
## physical terminal

Hardware device attached to a computer allowing humans to interact with the latter.

Example of physical terminals:

   - keyboard + monitor
   - touch-screen monitor (e.g. at an airline kiosk)

Note that a monitor alone is not a terminal, because it can only output data.
And a keyboard is not a terminal, because it can only input data.

### What is the physical terminal in
#### a desktop computer?

Everything that isn't part of the tower:

   - keyboard
   - mouse
   - joystick
   - monitor
   - speakers
   - printer
   - scanner

#### a laptop?

It's fused with the non-human-facing parts.

###
### I have 3 monitors on my desktop pc.  How many physical terminals do I have?

1

Even with several monitors,  only one person can use the computer  at a time, so
it doesn't matter how many you have.

### A thin client is a kind of physical terminal.  But what is it exactly?

A computer  that is relatively  useless on its own,  but has a  keyboard, mouse,
monitor, maybe  one or  two USB  ports, and a  local area  connection to  a more
powerful server machine that actually runs user programs.

Often found in professional environment, or in student computer labs.

##
# s
## serial line interface

Users can affect serial line parameters with the `stty` command.
These parameters include:

   - baud rate

   - parity check

   - translation of carriage returns generated by most terminals into linefeeds
     expected by most programs

   - division of input into lines

   - definition of special control characters for erasing a character, killing
     a line of input, or interrupting a running process

## system console

Technically, it's the screen and keyboard used for system administration:
<https://en.wikipedia.org/wiki/System_console>

But the term is  also used to refer to the only  virtual terminal available when
Linux is in single-user mode (called rescue mode in systemd).
The latter can be accessed on an OS using systemd by running either of:

    $ telinit 1
    $ systemctl rescue
    $ systemctl isolate rescue.target

---

Its tty is `/dev/console` (device type 5:1).

##
# t
## termcap

Combination of a database and a subroutine library.

The database describes the capabilities of different terminals.
The subroutine lets programs query the database and use the capability values it
contains.

It  controls visual  attributes of  the  terminal, and  tells a  screen-oriented
program (as opposed to a line-oriented program like `sed`):

   - how big the screen is
   - how to move the cursor to any point on the screen
   - how to refresh the screen
   - how to enter/exit any special display mode (like blinking or underlining)
   - ...

It was written initially by Bill Joy for Vi on BSD.

## termcap entry

List  of names  for a  given  terminal, followed  by  a list  of the  terminal's
capabilities.

The names are separated with bars.

The first name is the canonical name of the terminal, the others are aliases.
Ex:

        screen-256color|GNU Screen with 256 colors
        └─────────────┤ └────────────────────────┤
                      │                          └ alias (long name)
                      └ canonical name

## terminfo

Database similar to `termcap`.
It's used  by screen-oriented  programs such as  nvi(1), rogue(1)  and libraries
such as ncurses(3NCURSES).

There are 5 differences between the 2 db:

   - `terminfo`  is  compiled to improve efficiency, whereas `termcap` is
     a human-readable text

   - `terminfo` consists of a directory hierarchy of individual compiled
     terminal descriptions, whereas `termcap` is a file

     In a terminfo  db, the directory `s/` contains the  descriptions of all the
     terminals whose name begin with `s`.
     Same thing for every other letter.

   - while the  capabilities in  both db  are equivalent  for the most part,
     only a few of the capability names are the same

   - `termcap`  only allows  2-character capability  names, while `terminfo`
     uses up to 5 characters

   - the syntax for encoding some capabilities is different

###
## terminal device (aka TTY)

Device file living in `/dev`, that  provides a software abstraction to a virtual
terminal, in the same way that  (for example) `/dev/sda1` might represent a hard
drive or `/dev/dsp` the speakers.

Thus, if  you write to `/dev/tty1`,  for example, characters will  appear on the
first virtual terminal's  virtual screen, which you  will be able to  see if you
then switch to it.

### In which way can it be considered as a software abstraction?

An application program which wants to  interact with a virtual terminal, doesn't
need  to  know its  features  or  functions; the  program  can  use the  virtual
terminal's device driver via standard I/O system calls on the tty.

#### Which benefit(s) does this give?

This **simplifies** the program and leads to **consistent** user-space I/O mechanisms.

###
### To finish
#### The following terminal devices are found on a typical system:
#### seven virtual terminals

The seven virtual terminals, with corresponding device nodes `/dev/tty1` through
`/dev/tty7` (4:1, …, 4:7).

On some system, there can be more; for example up to 63 (4:3f).

#### /dev/tty

The device node `/dev/tty` (5:0) refers to the controlling terminal of the process
that opens it (more on this later).

So if I have bash running on tty1 and  tty2, and I launch a program from bash on
tty1 and that  program opens `/dev/tty`, the  effect will be identical  to if it
had opened `/dev/tty1`,  but if I launched  the same program from  bash on tty2,
then the effect would be identical to if it had opened `/dev/tty2`.

This device node is also required to exist by POSIX.

If a program  with no controlling terminal tries to  open `/dev/tty`, the result
(on Linux, at least) will be ENXIO.
From `man 2 open`:

   > ENXIO [...] the file is a device special file and no corresponding device exists.

#### /dev/tty0

Some systems have a `/dev/tty0` (4:0).

Now, the virtual terminals are always numbered starting from one, but several of
the Linux-specific terminal ioctl(2)s that take  a virtual terminal number as an
argument  will  happily accept  0,  which  means  the currently  active  virtual
terminal.

In analogy, opening `/dev/tty0` will give you a file descriptor to the currently
active virtual terminal.

On a headless  machine (with, therefore, no active virtual  terminal), trying to
open this device, again, yields ENXIO.

#### /dev/ttyS0 ... /dev/ttyS3

You will  typically find serial  consoles on a Linux  system as well;  my Ubuntu
system has four,  with device nodes `/dev/ttyS0` through  `/dev/ttyS3` (4:40, …,
4:43), regardless of how many serial ports are actually present on the machine.

If you read from or write to one of these, the system will attempt to receive or
transmit data through a serial port presumably connected to another computer.

(If there  is no connection,  you'll simply get  an EIO.) I probably  won't talk
about these much.

#### BSD-style pseudoterminals

I  will probably  devote  an entire  part  to pseudoterminals,  and  I will  not
explain what  they are  right now;  however, a pseudoterminal  has two  parts, a
master  and  slave  part,  where  the  master is  exposed  as  the  device  node
`/dev/pty([a-e]|[p-z])[0-f]` and the slave `/dev/tty([a-e]|[p-z])[0-f]`.

(So, `/dev/ptya0` and so on: a total of 256 pairs.) The major device number is 2
for each master and  3 for each slave; the minor device numbers  start at 00 for
ttyp0 or  ptyp0, 01 for ttyp1,  and so on, and  increase up to af  for ttyzf, at
which point they wrap, so b0 for ttya0, and so on up to ff for ttyef.

(Presumably, it starts at “p” because this  is the first letter of “pseudo”, and
it wraps around the alphabet just because it has to.)

#### Unix98 pseudoterminals

Unix98 pseudoterminals,  consisting of the master  multiplexer `/dev/ptmx` (5:2)
and the  slaves `/dev/pts/n` generated  on demand, that is,  `/dev/pts/0` (88:0,
not sure whether that's set in stone) and so on.

Note that a pseudoterminal  is often called a pty, and  the term “tty” sometimes
includes pseudoterminals  and serial  consoles, and at  other times  it includes
only the system console and numbered virtual terminals.
You'll have to figure it out by context.

##
# v
## virtual screen

Each virtual  terminal has its own  virtual screen, but only  one virtual screen
can be on the physical terminal's monitor at any given time.

## virtual terminal (aka virtual console)

Conceptual combination of the keyboard and display for a computer user interface.

On  the physical  terminal of  a typical  Linux system,  there are  seven usable
virtual terminals  by default; one can  switch between them to  access unrelated
user interfaces.

Even though only one person can use  a physical terminal at any given time, that
person may maintain several distinct sessions, one on each virtual terminal.

### What does the seventh virtual terminal run on Ubuntu?

The graphical environment.

### What does Alt+Fn do, formally?

It  activates the  virtual  terminal number  `n`, which  means  that the  latter
receives  all  keyboard and  mouse  input  exclusively,  and only  that  virtual
terminal's virtual screen is shown on the physical terminal.

