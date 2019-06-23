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
## A terminal can use colors outside the palette.  Usually, what do they colorize?

It depends on  the terminal, but, among other things,  they're used to colorize
some elements of the UI:

   - text foreground
   - terminal background
   - cursor
   - tab activity
   - text selection
   - bold text
   ...

The colors used for these don't belong to the palette.
They are not meant to be used by a program to color an *arbitrary* element of its UI.
Their only purpose is to color some *fixed* elements of the UI of the terminal.

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

---

Also, in some terminals, you can still use the sequence:

    OSC 4 ; c ; spec ST

to change a color of the palette.
Where `c`  is the index (in  the palette) of the  color you want to  change, and
`spec` is the name of a color or an RGB specification.

Try this:

    $ palette

Look at the color 159 (it's cyan).

    $ printf '\e]4;159;yellow\e\\'

The  color of  the  characters  displaying `159`  should  immediately change  to
yellow; if it doesn't, it means the terminal doesn't support the sequence.

#
# True Color
## What's the benefit of true color?

When a program uses a color in the 256color palette, it sends an escape sequence
containing a decimal code  which refers to a color in the  palette, which can be
configured by the USER.

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

