# Color systems
## What is a color system?

A system which mixes a small set of primary colors to create a big set of colors.

## What are primary colors?

They are mixed by a color system to create a big set of colors.

You can choose any colors to be the primary colors of your color system, but not
all color systems are equally effective.
For instance, you can  create a color system where light  blue, medium blue, and
violet are your primary colors.
But  it won't  be very  useful because  no amount  of mixing  will produce  red,
orange, yellow, etc.

## What is the color gamut?

The set of colors created by mixing the primary colors of a color system.

The bigger the gamut, the more effective the color system is.

A color system with  a large gamut is more able to  effectively represent a wide
variety of images containing different colors.

## What is an additive color system?

A system that creates light directly.

The term  “additive” comes from  the fact  that the final  beam of light  is the
result of the addition of different light sources.

Computer screens are an example of additive color system.
Each  pixel is  just  a small  collection of  light  sources emitting  different
colors.

If you  display an  image of  a pumpkin on  your computer  screen, you  have not
really turned on any orange-emitting light sources in the screen.
Rather, you  have turned  on tiny  red and green-emitting  light sources  in the
screen, and the red and green light add together to make orange.

The most effective additive color system is red-green-blue (RGB) because it best
matches the  human eye which contains  cells detecting only the  red, green, and
blue colors.

Mixing all primary colors of this system gives the color white.

## What is a subtractive color system?

A System that removes colors through absorption.

The term “subtractive” comes  from the fact that the final  color is achieved by
starting with white light (which contains  all colors) and then subtracting away
certain colors, leaving other colors.

Examples of subtractive color systems are paints, pigments, and inks.
An orange pumpkin that you see printed in a newspaper is not necessarily created
by spraying orange ink on the paper.
Rather, 2 inks may be sprayed onto the paper:

   - yellow ink
   to absorb blue light (from the white light beam), and a little green and red

   - magenta ink
   to absorb green light, and a little blue and red

... leaving only orange to be reflected back.

The most effective subtractive color system is cyan-magenta-yellow (CMY) because
it's the opposite of red-green-blue:

   - Cyan     is the opposite of red    and is halfway between green and blue
     (water vs fire)

   - Magenta  is the opposite of green  and is halfway between blue  and red
     (evil vs nature)

   - Yellow   is the opposite of blue   and is halfway between red   and green
     (day vs night)

This is  why most  printed images contain  a grid of  little cyan,  magenta, and
yellow dots of ink.

Mixing all primary colors of this system gives the color black.


                                     NOTE:

It seems  that mixing  colors in  an additive OR  subtractive system  produces a
color somewhere in the middle.
The exact position depends  on the quantity of each color  (it matches some sort
of barycenter).

For example, if you mix:

   - twice as much yellow as magenta ink
   - twice as much red    as green   light source

You get orange.

See here for a better visualization:

<http://wtamu.edu/~cbaird/sq/images/rgb_color_wheel.png>


TODO:

Those explanations would be much easier to follow if we had local diagrams.
Try to reproduce those with tikz:

   - <http://wtamu.edu/~cbaird/sq/images/rgb_color_wheel.png>
   - <http://wtamu.edu/~cbaird/sq/images/color_mixing.png>

## How to create your own color scheme / palette?

<https://github.com/thezbyg/gpick/wiki/Guide>

Wiki of the gpick program.

In the upper-left corner  of the color picker tab, there are  6 cells forming an
hexagon, and a 7th in the center.
They allow you to store and compare up to 6 colors.
To store  a color in a  cell, right click in  the one in the  middle (7th), then
hover your cursor over the color in which you're interested, and hit space.

## Why do computer screens use red, green, and blue?
... and why are red, yellow, and blue the primary colors in painting?

<http://wtamu.edu/~cbaird/sq/2015/01/22/why-are-red-yellow-and-blue-the-primary-colors-in-painting-but-computer-screens-use-red-green-and-blue/>

#
# 256 Colors Palette
## What characterizes a 256color capable terminal?

It can provide a built-in palette of 256 colors that the programs (like Vim) can
use to color the text or various elements of their UI.

##
## What are the 3 categories of colors in a 256 colors palette?

   - 16  ANSI colors
   - 216 colors from a built-in palette
   - 24  shades of gray (grayscale from black to white)

---

Note that I write “gray” instead of “grey”.
Both spellings  are correct, but  I prefer the second  one because it's  used in
american english, and usually we use the latter (color vs colour), so let's stay
consistent.

If you've got difficulty to remember which spelling is american, remember this:

> E for England, A for America.

<https://english.stackexchange.com/questions/255435/gray-or-grey-which-one-should-i-use/255437#comment558850_255436>

### Which color names are chosen for the first 8 ones?

   - black
   - red
   - green
   - yellow
   - blue
   - magenta
   - cyan
   - white

#### for the next 8 ones?

The same 8 colors but brighter/more intense.

#### Why these colors in particular?

<http://wtamu.edu/~cbaird/sq/2015/01/22/why-are-red-yellow-and-blue-the-primary-colors-in-painting-but-computer-screens-use-red-green-and-blue/>

Black and white are obvious.

red,  green, blue  because they  are the  primary colors  of the  most effective
additive color system.

cyan, magenta, yellow because they are  the primary colors of the most effective
subtractive color system.

###
### How are the 216 colors in the middle of a palette chosen by default?

Theory:

The terminal's developers *choose* 6 shades of red, 6 of green and 6 of blue.
They *mix* all possible combinations (6×6×6 = 216).
They *index* them with the following formula:

    16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)

Source: <https://en.wikipedia.org/wiki/ANSI_escape_code#Colors>

---

More generally, if you  want to encode n numbers a₁,...,aₙ, with 0  ≤ aᵢ < B, then
encode it as:

    a₁ + a₂B + ⋯ + aₙBₙ₋₁

Source: <https://mathoverflow.net/a/69250>

#### Why the number 216?

This is the biggest cube we can use which fits in 1 byte (256 codes).

    6×6×6 = 216 ✔
    7×7×7 = 343 ✘

#### Are they defined with the same hex color codes, from one terminal to the other?

It seems so.

Run `$ palette` in  a terminal, start Gpick, and hover your  cursor over a given
color; you'll always find the same hex color code.
It seems to indicate that most (all?)  terminals use the same last 216+24 colors
in their palette, probably inspired by xterm.

##
### Why 24 shades of gray?

That's what's left after removing the cube of 216 colors and the 16 ANSI colors:

    256 - 6×6×6 - 16 = 24

#### What scheme is usually followed by the hex color code of any of these?

It follows the scheme `#xyxyxy`, where `x` and `y` are hex digits.

This can  help you to  quickly determine whether an  arbitrary hex color  code –
found with Gpick  and used to color  some text/UI element – is  in the grayscale
part of the terminal's palette.
For example, `#123456` shouldn't be a shade of gray, while `#121212` could be.

##
## `$ palette`
### What do the colors in the same column in the output of `$ palette` have in common?

They end with the same digits.

This can  help you to  quickly determine whether an  arbitrary hex color  code –
found with Gpick and used to color some text/UI element – is in a given column.

For example, if you're looking for `#123456`,  you pick a color in a column, and
its hex color code  is `#789abc`, there's no need to  compare `#123456` with any
other color in the column, because `56` doesn't match `bc`.

### What do the colors in the same 6x6 square in the output of `$ palette` have in common?

They start with the same digits.

This can  help you to  quickly determine whether an  arbitrary hex color  code –
found with Gpick and used to color some text/UI element – is in a given square.

For example, if you're looking for `#123456`,  you pick a color in a square, and
its hex color code  is `#789abc`, there's no need to  compare `#123456` with any
other color in the square, because `12` doesn't match `78`.

##
## How to change a color used in the palette?

Usually, you can tweak  the first 16 ANSI colors via a  menu in the preferences,
but not the remaining 240 ones.

urxvt and  xterm are exceptions;  they allow you to  redefine all colors  of the
palette via `~/.Xresources`.

### How to do it at run time?

In some terminals, you can use this sequence:

    OSC 4 ; c ; spec ST
            │   │
            │   └ desired color
            └ index of the color in the palette

`spec` can be a name or RGB specification as per XParseColor.
The latter includes the syntax `#RRGGBB`.
`#RRGGBB` is an old and not encouraged syntax (see `man XParseColor`).

To test the sequence, first run:

    $ palette

And look at the color 159 (it's cyan).
Then run:

    $ printf '\e]4;159;yellow\a'

The  color of  the  characters  displaying `159`  should  immediately change  to
yellow; if it doesn't, it means the terminal doesn't support the sequence.

#### How to change several colors in one single command?

Any number of `c`/`spec` pairs may be given.

    OSC 4 ; c1 ; spec1 ; c2 ; spec2 ; ... ; ST

Example:

    $ printf '\e]4;0;red;1;green\a'
                   ├───┘ ├─────┘
                   │     └ set the color 1 to green
                   └ set the color 0 to red

#### How to reset all the colors to their default values?

Restart a new terminal.

If you're  inside tmux, first  close the terminal  or detach, then  re-attach to
your tmux session.

##
## How to get the rgb specification of a color used in the palette?

Use this sequence:

    OSC 4 ; <color index> ; ? BEL

Example:

    $ printf '\e]4;123;?\a'

See `OSC Ps ; Pt BEL`:

> If a "?" is given rather than  a name or RGB specification, xterm replies with
> a control sequence of the same form which can be used to set the corresponding
> color.

---

To capture the terminal's reply in a variable, run `$ read`:

    $ printf '\e]4;123;?\a' ; read -d $'\a' -s -t 0.1

The reply should be in `$REPLY`.
If you  want to  inspect its contents,  don't simply echo  it (you  wouldn't see
anything because it starts with an Escape); use `$ od` instead:

    $ printf -- '%s' ${REPLY#$(printf "\e]4;")[0-9]*;rgb:} | od -t c

### It doesn't work in st!

Yes, the sequence is not supported by all terminals.
xterm does support it though; no idea about the other terminals.

##
# True Color
## What's the benefit of true color?

When a program uses a color in the 256color palette, it sends an escape sequence
containing a decimal code  which refers to a color in the  palette, which can be
configured by the *user*.

OTOH, when a program  uses a true color, it sends  an escape sequence containing
the exact  quantity of  red, green,  blue to  produce the  color desired  by the
program *developer*.

So, true color gives  total control to the developer of a  program on the colors
it will use.

## What's the effect of true color in Vim?

With true color, the color of any  HG is defined by `guifg` and `guibg`, instead
of `ctermfg` and `ctermbg`.

## How to enable true color in Vim?

Vim supports true color in the terminal, if:

   - the terminal supports true color
   - `'tgc'` is set

Sometimes setting  `'tgc'` is  not enough and  one has to  set the  `'t_8f'` and
`'t_8b'` options explicitly.
The default values of these options are:

    ^[[38;2;%lu;%lu;%lum
    ^[[48;2;%lu;%lu;%lum
             ││
             │└ `man 3 printf`:
             │
             │       The unsigned int argument is converted to unsigned decimal
             │
             └ `man 3 printf`:

                   A following  integer conversion corresponds  to a long  int or
                   unsigned long int argument

... respectively, but they are only set when `$TERM` is `xterm`.

The syntax with colons which is more compatible but less widely supported.

Interesting comment about the two syntaxes:
<https://gist.github.com/XVilka/8346728#gistcomment-2008553>

## How to enable true color in Neovim?

Nvim supports true color in the terminal, if:

   - the terminal supports true color
   - 'termguicolors' is set
   - the 'setrgbf' and 'setrgbb' terminfo extensions are correctly set

Nvim adds constructed  'setrgbf' and 'setrgbb' capabilities in  the terminfo db,
if they're missing and:

   - the 'Tc' terminfo extension *is* set (in the external db)
   - the 'Tc' terminfo extension is *not* set, but $TERM is:

   - 'rxvt'
   - 'linux'
   - 'st'
   - 'tmux'
   - 'iterm'

   ... or the terminal is:

   - Konsole
   - genuine Xterm
   - a libvte terminal emulator version 0.36 or later
   - a terminal emulator that sets the COLORTERM environment variable to 'truecolor'

## How does Vim encode true colors?

For a given HG,  Vim converts the hex colors of its `fg`  and `bg` attributes in
GUI (set  via the  arguments `guifg` and  `guibg` passed to  `:hi`), into  a rgb
triplet  `(red, green,  blue)`.
Each hex  number in this triplet  expresses the intensity of  the red/green/blue
component of the color and is in the range 00-FF.

The  triplet is  then used  to expand  the printf-like  format specified  in the
options `'t_8f'` and `'t_8b'`.
Each component is stored  in 1 byte, thus a true color needs  3 bytes or 24 bits
to be stored.

The hex  numbers are pushed onto  a stack (`%p1`, `%p2`,  `%p3`),from which they
are popped and converted into signed decimal numbers (`%d`).

The syntax of the sequence can be found here:

<http://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Functions-using-CSI-_-ordered-by-the-final-character_s_>

>    CSI Pm m  Character Attributes (SGR).
>
>    ...
>
>    This variation on ISO-8613-6 is supported for compatibility with KDE konsole:
>
>>       Pm = 3 8 ; 2 ; Pr; Pg; Pb
>>       Set foreground color to the closest match in xterm's palette for
>>       the given RGB Pr/Pg/Pb.
>>
>>       Pm = 4 8 ; 2 ; Pr; Pg; Pb
>>       Set background color to the closest match in xterm's palette for
>>       the given RGB Pr/Pg/Pb.

## Does true color work in xterm, urxvt, xfce4-terminal?

When  we enable  true color  in xterm,  the colors  are too  different from  the
intended ones.

It may be due to:

> it uses nearest colour in RGB colour space, with a usual false assumption
> about orthogonal axes

<https://github.com/neovim/neovim/issues/793#issuecomment-48106948>

What does this mean?

Theory:
When xterm  must display a  true color,  it looks for  the closest color  in its
built-in palette.

But to  determine the closest  color, it has to  compute a “distance”  between 2
colors  in a  24bit space:  the asked  true color  and an  approximation in  the
palette.

The  definition of  the distance  between 2  points in  a space  depends on  the
relative position of its axes (which angle do they form?).
When xterm computes the  distance between a true color and one  if its color, it
assumes that the axes are orthogonal.
This is is wrong,  thus xterm fails to find the best  approximation, and ends up
choosing a poor color in its palette.

---

Also, for  true color  to work in  urxvt and xfce4-terminal,  you need  a recent
version of the programs.

## Where can I find more info on true color?

   - <https://gist.github.com/XVilka/8346728>
   - <https://en.wikipedia.org/wiki/ANSI_escape_code#Colors>

##
# Text color attributes
## How to apply a color whose index in the terminal palette is
### between 0 and 7?  (2)

Use the SGR sequence, whose syntax is:

    CSI Pm m

and replace Pm with `30 + <color index>`:

    $ printf '\e[30m  text in black    \e[0m\n'
    $ printf '\e[31m  text in red      \e[0m\n'
    $ printf '\e[32m  text in green    \e[0m\n'
    $ printf '\e[33m  text in yellow   \e[0m\n'
    $ printf '\e[34m  text in blue     \e[0m\n'
    $ printf '\e[35m  text in magenta  \e[0m\n'
    $ printf '\e[36m  text in cyan     \e[0m\n'
    $ printf '\e[37m  text in white    \e[0m\n'

Or with `38;5;<color index>`:

    $ printf '\e[38;5;0m  text in black    \e[0m\n'
    $ printf '\e[38;5;1m  text in red      \e[0m\n'
    $ printf '\e[38;5;2m  text in green    \e[0m\n'
    $ printf '\e[38;5;3m  text in yellow   \e[0m\n'
    $ printf '\e[38;5;4m  text in blue     \e[0m\n'
    $ printf '\e[38;5;5m  text in magenta  \e[0m\n'
    $ printf '\e[38;5;6m  text in cyan     \e[0m\n'
    $ printf '\e[38;5;7m  text in white    \e[0m\n'

Prefer the second syntax; the first one is a legacy one.

Note that even though we wrote color names in the previous examples, you may get
different colors when you run these commands.
This is because  they apply the colors  of the terminal palette,  and the latter
may have been arbitrarily changed by the user.

### between 8 and 15?  (2)

In the SGR sequence, replace Pm with `90 + <color index>`.

    $ printf '\e[90m  text in black    \e[0m\n'
    $ printf '\e[91m  text in red      \e[0m\n'
    $ printf '\e[92m  text in green    \e[0m\n'
    $ printf '\e[93m  text in yellow   \e[0m\n'
    $ printf '\e[94m  text in blue     \e[0m\n'
    $ printf '\e[95m  text in magenta  \e[0m\n'
    $ printf '\e[96m  text in cyan     \e[0m\n'
    $ printf '\e[97m  text in white    \e[0m\n'

Or with `38;5;<color index>`.

    $ printf '\e[38;5;8m   text in black    \e[0m\n'
    $ printf '\e[38;5;9m   text in red      \e[0m\n'
    $ printf '\e[38;5;10m  text in green    \e[0m\n'
    $ printf '\e[38;5;11m  text in yellow   \e[0m\n'
    $ printf '\e[38;5;12m  text in blue     \e[0m\n'
    $ printf '\e[38;5;13m  text in magenta  \e[0m\n'
    $ printf '\e[38;5;14m  text in cyan     \e[0m\n'
    $ printf '\e[38;5;15m  text in white    \e[0m\n'

### beyond 15?

In the SGR sequence, replace Pm with `38;5;<color index>`.

    $ printf '\e[38;5;123m text colored with 123th color of palette \e[0m\n'

###
## How to apply a true color?

In the SGR sequence, replace Pm  with `38;2;rr;gg;bb`, where `rr`, `gg` and `bb`
are the quantity of red, green and  blue present in the desired color, expressed
by a number in the range `[0-255]`.

    $ printf '\e[38;2;123;234;45m text in this true color \e[0m\n'

Whether it  works and whether  the color is  reliably rendered, or  the terminal
just chooses the closest match in its palette, depends on the terminal.
More  specifically,  it  depends  on  whether/how it  supports  the  true  color
capability.

## How to apply a color to the *background* of the text?

Add 10 to the first number in Pm.

                 ┌ 30 + 10
                 ├┐
    $ printf '\e[40m  background in black    \e[0m\n'
    $ printf '\e[41m  background in red      \e[0m\n'
    $ printf '\e[42m  background in green    \e[0m\n'
    $ printf '\e[43m  background in yellow   \e[0m\n'
    $ printf '\e[44m  background in blue     \e[0m\n'
    $ printf '\e[45m  background in magenta  \e[0m\n'
    $ printf '\e[46m  background in cyan     \e[0m\n'
    $ printf '\e[47m  background in white    \e[0m\n'

                 ┌ 90 + 10
                 ├─┐
    $ printf '\e[100m  background in black    \e[0m\n'
    $ printf '\e[101m  background in red      \e[0m\n'
    $ printf '\e[102m  background in green    \e[0m\n'
    $ printf '\e[103m  background in yellow   \e[0m\n'
    $ printf '\e[104m  background in blue     \e[0m\n'
    $ printf '\e[105m  background in magenta  \e[0m\n'
    $ printf '\e[106m  background in cyan     \e[0m\n'
    $ printf '\e[107m  background in white    \e[0m\n'

                 ┌ 38 + 10
                 ├┐
    $ printf '\e[48;5;0m  background in black    \e[0m\n'
    $ printf '\e[48;5;1m  background in red      \e[0m\n'
    $ printf '\e[48;5;2m  background in green    \e[0m\n'
    $ printf '\e[48;5;3m  background in yellow   \e[0m\n'
    $ printf '\e[48;5;4m  background in blue     \e[0m\n'
    $ printf '\e[48;5;5m  background in magenta  \e[0m\n'
    $ printf '\e[48;5;6m  background in cyan     \e[0m\n'
    $ printf '\e[48;5;7m  background in white    \e[0m\n'

    $ printf '\e[48;5;8m   background in black    \e[0m\n'
    $ printf '\e[48;5;9m   background in red      \e[0m\n'
    $ printf '\e[48;5;10m  background in green    \e[0m\n'
    $ printf '\e[48;5;11m  background in yellow   \e[0m\n'
    $ printf '\e[48;5;12m  background in blue     \e[0m\n'
    $ printf '\e[48;5;13m  background in magenta  \e[0m\n'
    $ printf '\e[48;5;14m  background in cyan     \e[0m\n'
    $ printf '\e[48;5;15m  background in white    \e[0m\n'

    $ printf '\e[48;5;123m background colored with 123th color of palette \e[0m\n'

    $ printf '\e[48;2;123;234;45m background in true color \e[0m\n'

##
# UI
## How to change the color of some element of the terminal's UI?

In some terminals, you can use this sequence:

    OSC Ps ; Pt ST
        │    │
        │    └ specifies the new color (can be a name or a hexcode like `#ab1234`)
        └ specifies a UI element

### How to replace Ps if I want to set the color of
#### the terminal foreground?

10

    $ printf '\e]10;yellow\a\n'
    $ printf '\e]10;#ab1234\a\n'

This affects the default  color of the text, when it's  not highlighted, as well
as the cursor.

#### the terminal background?

11

    $ printf '\e]11;yellow\a\n'
    $ printf '\e]11;#ab1234\a\n'

#### the cursor foreground?

12

    $ printf '\e]12;yellow\a\n'
    $ printf '\e]12;#ab1234\a\n'

##
# Issues
## Some text is wrongly colored in the terminal!
### How to find out its hex color code?

Run Gpick and hover your cursor over the text.
If positioning the cursor accurately is too hard, because the text is too small,
temporarily configure your terminal to use a much bigger font.

### How to find out which color from the terminal's palette, if any, is used?

Let's assume the color – found with Gpick – is `#ab1234`.

Comparing `#ab1234` to *each* color in the terminal's palette would take too much time.
But you don't have to.

First, `#ab1234`  is not repeating  the same  2 digits, so  it's not a  shade of
gray, and you don't have to compare it to the last 24 colors in the palette.
OTOH, if  your color *was* following  the scheme `#xyxyxy`, then  you would only
have to compare it to the last 24 colors in the palette.

Next, compare `#ab1234` to each of the first 16 colors (ANSI palette).

If there's no match, then consider the last two digits of `#ab1234`; i.e. `34`.
Compare them to the last two digits in *any* color of a given column in the palette.
If it doesn't match, `#ab1234` is not in this column.
Repeat until you find a color in a column whose last two digits are `34`; if you
don't find one, `#ab1234` is not in the palette.

If you've found a  color whose last two digits are `34`,  consider the first two
digits in `#ab1234`, i.e. `ab`.
Compare them to the first two digits in *any* color of a square.
If it doesn't match `ab`, `#ab1234` is not in this square.
Repeat until you  find a color in a  square whose first two digits  are `ab`; if
you don't find one, `#ab1234` is not in the palette.

If you've found a  color whose first two digits are `ab`, all  you have to do is
compare each of the  six colors which are simultaneously in  the `ab` square and
in the `34` column.

At worst, you have 16 (ANSI colors) + 6 (columns) + 6 (squares) + 6 (lines) = 34
comparisons to do.

---

Alternatively, use `~/bin/is_it_in_the_palette.sh`, but be aware of the
limitations of this script; they're documented at the top of the file.

##
## I'm trying to combine the color black with the bold attribute.  I get some light grey!

In some sequences, bold is interpreted as bright:

<https://askubuntu.com/questions/875102/gnome-terminal-use-bright-colors-for-bold>

---

The bold  attribute (`\e[1m`) is interpreted  as bold when combined  with direct
RGB colors (true  colors), and with the colors of  the 256-color palette, beyond
the first 16.

However,  the first  16 colors  in the  256-color palette  can be  accessed with
escape sequences  using the numbers 30–37  (first 8), 90–97 (following  8 bright
variants), or 38;5;0–15.

And  if you  combine the  sequences using  the numbers  30–37 with  `\e[1m`, the
latter is interpreted as bold**+bright** (for legacy compatibility reasons).

So, this prints the text “hello” in bold black:

    $ printf '\e[38;5;0;1m  hello  \e[0m\n'

While this prints the same text in bold grey:

    $ printf '\e[30;1m  hello  \e[0m\n'

If you  want to know which  sequence is used by  a program to encode  one of the
first 16 foreground colors in the 256-color palette, have a look at the value of
your terminal's `setaf` capability.

---

Note that st doesn't suffer from this issue provided you applied this patch:
<https://st.suckless.org/patches/bold-is-not-bright/>

