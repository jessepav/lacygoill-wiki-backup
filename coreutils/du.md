# What does `du` do?

It estimates file space usage.

It reports the amount  of disk space used by the set of  specified files and for
each subdirectory (of directory arguments).

# Synopsis

    $ du [OPTION]... [FILE]...

With no arguments, `du` reports the disk space for the current directory.
Normally the  disk space  is printed  in units of  1024 bytes,  but this  can be
overridden.

# Options
## `-0`, `--null`

Output a zero byte at the end of each line, rather than a newline.
This option  enables other programs  to parse the  output even when  that output
would contain data with embedded newlines.

## `-a`, `--all`

Show counts for all files, not just directories.

## `--apparent-size`

Print apparent sizes, rather than disk usage.
The apparent  size of  a file  is the  number of  bytes reported  by `$ wc  -c` on
regular files, or more generally, `$ ls -l --block-size=1` or `$ stat --format=%s`.
For example, a file containing the word  ‘zoo’ with no newline would, of course,
have an apparent size of 3.
Such a small file  may require anywhere from 0 to 16 KiB  or more of disk space,
depending on  the type and  configuration of the file  system on which  the file
resides.
However, a sparse file created with this command:

    $ dd bs=1 seek=2GiB if=/dev/null of=big

has an  apparent size of  2 GiB,  yet on most  modern systems, it  actually uses
almost no disk space.

## `-B SIZE`, `--block-size=SIZE`

Scale sizes by SIZE before printing them.
For example, `-BG` prints sizes in units of 1,073,741,824 bytes.

## `-b`, `--bytes`

Equivalent to `--apparent-size --block-size=1`.

## `-c`, `--total`

Print a grand total of all arguments after all arguments have been processed.
This can be  used to find out  the total disk usage  of a given set  of files or
directories.

## `-D`, `--dereference-args`

Dereference symbolic links that are command line arguments.
Does not affect other symbolic links.
This  is  helpful  for finding  out  the  disk  usage  of directories,  such  as
`/usr/tmp`, which are often symbolic links.

## `-d DEPTH`, `--max-depth=DEPTH`

Show the total for each directory (and file if –all) that is at most `MAX_DEPTH`
levels down from the root of the hierarchy.
The root is at level 0, so `du --max-depth=0` is equivalent to `du -s`.

## `--files0-from=FILE`

Disallow processing files  named on the command line, and  instead process those
named in file FILE; each name being terminated by a zero byte (ASCII NUL).
This is  useful when  the list of  file names is  so long  that it may  exceed a
command line length limitation.
In such  cases, running `du`  via `xargs` is  undesirable because it  splits the
list into pieces and makes `du` print  with the `--total` (`-c`) option for each
sublist rather than for the entire list.
One way to produce a list of ASCII NUL terminated file names is with GNU `find`,
using its `-print0` predicate.
If FILE is `-`  then the ASCII NUL terminated file names  are read from standard
input.

## `-H`

Equivalent to `--dereference-args` (`-D`).

## `-h`, `--human-readable`

Append a size letter to each size, such as `M` for mebibytes.
Powers of 1024 are used, not 1000; `M` stands for 1,048,576 bytes.
This option is equivalent to `--block-size=human-readable`.
Use the `--si` option if you prefer powers of 1000.

## `--inodes`

List inode usage information instead of block usage.
This option  is useful  for finding  directories which  contain many  files, and
therefore eat  up most of the  inodes space of  a file system (see  `df`, option
`--inodes`).
It can  well be combined  with the options `-a`,  `-c`, `-h`, `-l`,  `-s`, `-S`,
`-t` and  `-x`; however,  passing other  options regarding  the block  size, for
example `-b`, `-m` and `--apparent-size`, is ignored.

## `-k`

Print sizes in 1024-byte blocks, overriding the default block size.
This option is equivalent to `--block-size=1K`.

## `-L`, `--dereference`

Dereference symbolic  links (show the disk  space used by the  file or directory
that the link points to instead of the space used by the link).

## `-l`, `--count-links`

Count the  size of  all files,  even if they  have appeared  already (as  a hard
link).

## `-m`

Print sizes in 1,048,576-byte blocks, overriding the default block size.
This option is equivalent to `--block-size=1M`.

## `-P`, `--no-dereference`

For each symbolic links encountered by `du`, consider the disk space used by the
symbolic link.

## `-S`, `--separate-dirs`

Normally, in the output of `du`  (when not using `--summarize`), the size listed
next to a directory name, D, represents  the sum of sizes of all entries beneath
D as well as the size of D itself.
With `--separate-dirs`, the size reported for  a directory name, D, will exclude
the size of any subdirectories.

## `--si`

Append an SI-style abbreviation to each size, such as `M` for megabytes.
Powers of 1000 are used, not 1024; `M` stands for 1,000,000 bytes.
This option is equivalent to `--block-size=si`.
Use the `-h` or `--human-readable` option if you prefer powers of 1024.

## `-s`, `--summarize`

Display only a total for each argument.

## `-t SIZE`, `--threshold=SIZE`

Exclude entries based on a given SIZE.
The SIZE refers  to used blocks in  normal mode, or inodes  count in conjunction
with the `--inodes` option.

If SIZE is positive, then `du` will  only print entries with a size greater than
or equal to that.

If SIZE is negative, then `du` will  only print entries with a size smaller than
or equal to that.

Although  GNU `find`  can  be used  to  find  files of  a  certain size,  `du`’s
`--threshold` option  can be used  to also filter  directories based on  a given
size.

Please  note   that  the   `--threshold`  option  can   be  combined   with  the
`--apparent-size` option,  and in  this case  would elide  entries based  on its
apparent size.

Please note  that the `--threshold` option  can be combined with  the `--inodes`
option, and in this case would elide entries based on its inodes count.

Here’s how you  would use `--threshold` to find directories  with a size greater
than or equal to 200 megabytes:

    $ du --threshold=200MB

Here's how you would use `--threshold` to  find directories and files - note the
`-a` - with an apparent size smaller than or equal to 500 bytes:

    $ du -a -t -500 --apparent-size

Here's how  you would  use `--threshold`  to find directories  on the  root file
system with more than 20000 inodes used in the directory tree below:

    $ du --inodes -x --threshold=20000 /

## `--time`

Show time of the  most recent modification of any file in  the directory, or any
of its subdirectories.

## `--time=ctime`, `--time=status`, `--time=use`

Show the most recent  status change time (the `ctime` in the  inode) of any file
in the directory, instead of the modification time.

## `--time=atime`, `--time=access`

Show the most recent  access time (the `atime` in the inode) of  any file in the
directory, instead of the modification time.

##
## `--time-style=STYLE`

List timestamps in style STYLE.
This option has an effect only if the `--time` option is also specified.

You  can  specify the  default  value  of  the  `--time-style` option  with  the
environment variable `TIME_STYLE`; if `TIME_STYLE`  is not set the default style
is `long-iso`.
For compatibility  with `ls`,  if `TIME_STYLE`  begins with  `+` and  contains a
newline,  the newline  and any  later  characters are  ignored; if  `TIME_STYLE`
begins with `posix-` the `posix-` is ignored; and if `TIME_STYLE` is `locale` it
is ignored.

The STYLE should be one of the following:

### `+FORMAT`

List  timestamps using  FORMAT,  where  FORMAT is  interpreted  like the  format
argument of `date` (see `$ info -n 'date invocation' coreutils`).
For example, `--time-style="+%Y-%m-%d %H:%M:%S"`  causes `du` to list timestamps
like `2002-03-30 23:45:56`.
As  with `date`,  FORMAT’s interpretation  is affected  by the  `LC_TIME` locale
category.

### `full-iso`

List timestamps in full using ISO 8601 date, time, and time zone components with
nanosecond precision, e.g., ‘2002-03-30 23:45:56.477817180 -0700’.
This style is equivalent to `+%Y-%m-%d %H:%M:%S.%N %z`.

### `long-iso`

List ISO 8601 date and  time components with minute precision, e.g., `2002-03-30
23:45`.
These timestamps  are shorter than  `full-iso` timestamps, and are  usually good
enough for everyday work.
This style is equivalent to `+%Y-%m-%d %H:%M`.

### `iso`

List ISO 8601 dates for timestamps, e.g., `2002-03-30`.
This style is equivalent to `+%Y-%m-%d`.

##
## `-X FILE`, `--exclude-from=FILE`

Like `--exclude`, except take the patterns to exclude from FILE, one per line.
If FILE is `-`, take the patterns from standard input.

## `--exclude=PATTERN`

When recursing, skip subdirectories or files matching PATTERN.
For example, `du --exclude='*.o'` excludes files whose names end in `.o`.

## `-x`, `--one-file-system`

Skip  directories that  are on  different  file systems  from the  one that  the
argument being processed is on.

On BSD systems,  `du` reports sizes that  are half the correct  values for files
that are NFS-mounted from HP-UX systems.
On HP-UX systems, it  reports sizes that are twice the  correct values for files
that are NFS-mounted from BSD systems.
This is due to a flaw in HP-UX; it also affects the HP-UX `du` program.

An exit status of zero indicates success, and a nonzero value indicates failure.

##
# Block size

This section was obtained with `:.!info -n block coreutils`

Some GNU programs (at least `df`, `du`, and `ls`) display sizes in “blocks”.
You can  adjust the block  size and  method of display  to make sizes  easier to
read.
The block size used for display is independent of any file system block size.
Fractional block counts are rounded up to the nearest integer.

The  default  block  size  is  chosen by  examining  the  following  environment
variables in turn; the first one that is set determines the block size.

## `DF_BLOCK_SIZE`

This specifies the default block size for the `df` command.
Similarly, `DU_BLOCK_SIZE`  specifies the  default for `du`  and `LS_BLOCK_SIZE`
for `ls`.

## `BLOCK_SIZE`

This  specifies the  default block  size for  all three  commands, if  the above
command-specific environment variables are not set.

## `BLOCKSIZE`

This specifies the  default block size for all values  that are normally printed
as blocks,  if neither `BLOCK_SIZE`  nor the above  command-specific environment
variables are set.
Unlike the other environment variables,  `BLOCKSIZE` does not affect values that
are normally printed as  byte counts, e.g., the file sizes  contained in `ls -l`
output.

## `POSIXLY_CORRECT`

If neither `COMMAND_BLOCK_SIZE`,  nor `BLOCK_SIZE`, nor `BLOCKSIZE`  is set, but
this variable is set, the block size defaults to 512.

If none  of the above  environment variables are  set, the block  size currently
defaults to  1024 bytes  in most  contexts, but  this number  may change  in the
future.
For `ls` file sizes, the block size defaults to 1 byte.

A  block size  specification can  be a  positive integer  specifying the  number
of  bytes  per  block, or  it  can  be  `human-readable`  or `si`  to  select  a
human-readable format.
Integers may  be followed  by suffixes  that are upward  compatible with  the SI
prefixes  (<http://www.bipm.org/en/publications/si-brochure/chapter3.html>)  for
decimal multiples and with the  ISO/IEC 80000-13 (formerly IEC 60027-2) prefixes
(<http://physics.nist.gov/cuu/Units/binary.html>) for binary multiples.

With human-readable formats, output sizes are  followed by a size letter such as
`M` for megabytes.
`BLOCK_SIZE=human-readable` uses powers of 1024; `M` stands for 1,048,576 bytes.
`BLOCK_SIZE=si` is similar, but uses powers of 1000 and appends `B`; `MB` stands
for 1,000,000 bytes.

A block size  specification preceded by `'` causes output  sizes to be displayed
with thousands separators.
The `LC_NUMERIC` locale specifies the thousands separator and grouping.
For example, in an American  English locale, `--block-size="'1kB"` would cause a
size of 1234000 bytes to be displayed as `1,234`.
In the default C locale, there is no thousands separator so a leading `'` has no
effect.

An integer block size can be followed by  a suffix to specify a multiple of that
size.
A bare size letter,  or one followed by `iB`, specifies  a multiple using powers
of 1024.
A size letter followed by `B` specifies powers of 1000 instead.
For  example, `1M`  and `1MiB`  are equivalent  to `1048576`,  whereas `1MB`  is
equivalent to `1000000`.

A plain suffix without a preceding integer acts as if `1` were prepended, except
that it causes a size indication to be appended to the output.
For example, `--block-size="kB"` displays 3000 as `3kB`.

Block size defaults can be overridden by an explicit `--block-size=SIZE` option.
The `-k` option is equivalent to  `--block-size=1K`, which is the default unless
the `POSIXLY_CORRECT` environment variable is set.
The     `-h`    or     `--human-readable`     option     is    equivalent     to
`--block-size=human-readable`.
The `--si` option is equivalent to `--block-size=si`.
Note for `ls` the `-k` option does  not control the display of the apparent file
sizes, whereas the `--block-size` option does.

The following suffixes are defined.
Large sizes like `1Y` may be rejected by your computer due to limitations of its
arithmetic.

### `kB`

kilobyte: 10^3 = 1000.

### `k`, `K`, `KiB`

kibibyte: 2^{10} = 1024.
`K` is special:  the SI prefix is  `k` and the ISO/IEC 80000-13  prefix is `Ki`,
but tradition and POSIX use `k` to mean `KiB`.

### `MB`

megabyte: 10^6 = 1,000,000.

### `M`, `MiB`

mebibyte: 2^{20} = 1,048,576.

### `GB`

gigabyte: 10^9 = 1,000,000,000.

### `G`, `GiB`

gibibyte: 2^{30} = 1,073,741,824.

### `TB`

terabyte: 10^{12} = 1,000,000,000,000.

### `T`, `TiB`

tebibyte: 2^{40} = 1,099,511,627,776.

### `PB`

petabyte: 10^{15} = 1,000,000,000,000,000.

### `P`, `PiB`

pebibyte: 2^{50} = 1,125,899,906,842,624.

### `EB`

exabyte: 10^{18} = 1,000,000,000,000,000,000.

### `E`, `EiB`

exbibyte: 2^{60} = 1,152,921,504,606,846,976.

### `ZB`

zettabyte: 10^{21} = 1,000,000,000,000,000,000,000

### `Z`, `ZiB`

2^{70} = 1,180,591,620,717,411,303,424.

### `YB`

yottabyte: 10^{24} = 1,000,000,000,000,000,000,000,000.

### `Y`, `YiB`

2^{80} = 1,208,925,819,614,629,174,706,176.

