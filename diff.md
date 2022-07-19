For all these tools, mandatory arguments to long options are mandatory for short options too.

# diff
## Synopsis

        diff [OPTION]... FILES

## Description

Compare FILES line by line.

---

        -q, --brief

report only when files differ

        -s, --report-identical-files

report when two files are the same

        -c, -C NUM, --context[=NUM]

output NUM (default 3) lines of copied context

        -u, -U NUM, --unified[=NUM]

output NUM (default 3) lines of unified context

        -e, --ed

output an ed script

        -n, --rcs

output an RCS format diff

        -y, --side-by-side

output in two columns

        -W, --width=NUM

output at most NUM (default 130) print columns

        --left-column

output only the left column of common lines

        --suppress-common-lines

do not output common lines

        -p, --show-c-function

show which C function each change is in

        -F, --show-function-line=RE

show the most recent line matching RE

        --label LABEL

use LABEL instead of file name (can be repeated)

        -t, --expand-tabs

expand tabs to spaces in output

        -T, --initial-tab

make tabs line up by prepending a tab

        --tabsize=NUM

tab stops every NUM (default 8) print columns

        --suppress-blank-empty

suppress space or tab before empty output lines

        -l, --paginate

pass output through `pr` to paginate it

        -r, --recursive

recursively compare any subdirectories found

        -N, --new-file

treat absent files as empty

        --unidirectional-new-file

treat absent first files as empty

        --ignore-file-name-case

ignore case when comparing file names

        --no-ignore-file-name-case

consider case when comparing file names

        -x, --exclude=PAT

exclude files that match PAT

        -X, --exclude-from=FILE

exclude files that match any pattern in FILE

        -S, --starting-file=FILE

start with FILE when comparing directories

        --from-file=FILE1

compare FILE1 to all operands; FILE1 can be a directory

        --to-file=FILE2

compare all operands to FILE2; FILE2 can be a directory

        -i, --ignore-case

ignore case differences in file contents

        -E, --ignore-tab-expansion

ignore changes due to tab expansion

        -Z, --ignore-trailing-space

ignore white space at line end

        -b, --ignore-space-change

ignore changes in the amount of white space

        -w, --ignore-all-space

ignore all white space

        -B, --ignore-blank-lines

ignore changes whose lines are all blank

        -I, --ignore-matching-lines=RE

ignore changes whose lines all match RE

        -a, --text

treat all files as text

        --strip-trailing-cr

strip trailing carriage return on input

        -D, --ifdef=NAME

output merged file with `#ifdef NAME` diffs

        --GTYPE-group-format=GFMT

format GTYPE input groups with GFMT

        --line-format=LFMT

format all input lines with LFMT

        --LTYPE-line-format=LFMT

format LTYPE input lines with LFMT

These  format options  provide fine-grained  control  over the  output of  diff,
generalizing -D/--ifdef.

LTYPE is `old`, `new`, or `unchanged`.
GTYPE is LTYPE or `changed`.

GFMT (only) may contain:

           %<     lines from FILE1

           %>     lines from FILE2

           %=     lines common to FILE1 and FILE2

           %[-][WIDTH][.[PREC]]{doxX}LETTER
                  printf-style spec for LETTER

                  LETTERs are as follows for new group, lower case for old group:

           F      first line number

           L      last line number

           N      number of lines = L-F+1

           E      F-1

           M      L+1

           %(A=B?T:E)
                  if A equals B then T else E

                  LFMT (only) may contain:

           %L     contents of line

           %l     contents of line, excluding any trailing newline

           %[-][WIDTH][.[PREC]]{doxX}n
                  printf-style spec for input line number

                  Both GFMT and LFMT may contain:

           %%     %

           %c'C'  the single character C

           %c'\OOO'
                  the character with octal code OOO

           C      the character C (other characters represent themselves)

        -d, --minimal

try hard to find a smaller set of changes

        --horizon-lines=NUM

keep NUM lines of the common prefix and suffix

        --speed-large-files

assume large files and many scattered small changes


--help display this help and exit

        -v, --version

output version information and exit

---

FILES are `FILE1 FILE2` or `DIR1 DIR2` or `DIR FILE...` or `FILE... DIR`.

If --from-file or --to-file is given, there are no restrictions on FILE(s).

If a FILE is `-`, read standard input.

Exit status is 0 if inputs are the same, 1 if different, 2 if trouble.

## See Also

        patch(1) (requires the `rcs` package)

##
# cmp
## Synopsis

       cmp [OPTION]... FILE1 [FILE2 [SKIP1 [SKIP2]]]

## Description

Compare two files byte by byte.

The  optional SKIP1  and  SKIP2 specify  the  number  of bytes  to  skip at  the
beginning of each file (zero by default).

        -b, --print-bytes

print differing bytes

        -i, --ignore-initial=SKIP

skip first SKIP bytes of both inputs

        -i, --ignore-initial=SKIP1:SKIP2

skip first SKIP1 bytes of FILE1 and first SKIP2 bytes of FILE2

        -l, --verbose

output byte numbers and differing byte values

        -n, --bytes=LIMIT

compare at most LIMIT bytes

        -s, --quiet, --silent

suppress all normal output


--help display this help and exit

        -v, --version

output version information and exit

---

SKIP values may be followed by the following multiplicative suffixes: kB 1000, K
1024, MB  1,000,000, M 1,048,576, GB  1,000,000,000, G 1,073,741,824, and  so on
for T, P, E, Z, Y.

If a FILE is `-` or missing, read standard input.
Exit status is 0 if inputs are the same, 1 if different, 2 if trouble.

##
# diff3
## Synopsis

       diff3 [OPTION]... MYFILE OLDFILE YOURFILE

## Description

Compare three files line by line.

        -A, --show-all

output all changes, bracketing conflicts

        -e, --ed

output ed script incorporating changes from OLDFILE to YOURFILE into MYFILE

        -E, --show-overlap

like -e, but bracket conflicts

        -3, --easy-only

like -e, but incorporate only nonoverlapping changes

        -x, --overlap-only

like -e, but incorporate only overlapping changes


-X like -x, but bracket conflicts


-i append `w` and `q` commands to ed scripts

        -m, --merge

output actual merged file, according to -A if no other options are given

        -a, --text

treat all files as text

        --strip-trailing-cr

strip trailing carriage return on input

        -T, --initial-tab

make tabs line up by prepending a tab

        --diff-program=PROGRAM

use PROGRAM to compare files

        -L, --label=LABEL

use LABEL instead of file name (can be repeated up to three times)

       --help

display this help and exit

        -v, --version

output version information and exit

The default  output format  is a somewhat  human-readable representation  of the
changes.

The -e,  -E, -x, -X (and  corresponding long) options  cause an ed script  to be
output instead of the default.

Finally, the  -m (--merge) option  causes diff3 to  do the merge  internally and
output the actual merged file.
For unusual input, this is more robust than using ed.

If a FILE is `-`, read standard input.
Exit status is 0 if successful, 1 if conflicts, 2 if trouble.

##
# sdiff
## Synopsis

       sdiff [OPTION]... FILE1 FILE2

## Description

Side-by-side merge of differences between FILE1 and FILE2.

        -o, --output=FILE

operate interactively, sending output to FILE

        -i, --ignore-case

consider upper- and lower-case to be the same

        -E, --ignore-tab-expansion

ignore changes due to tab expansion

        -Z, --ignore-trailing-space

ignore white space at line end

        -b, --ignore-space-change

ignore changes in the amount of white space

        -W, --ignore-all-space

ignore all white space

        -B, --ignore-blank-lines

ignore changes whose lines are all blank

        -I, --ignore-matching-lines=RE

ignore changes whose lines all match RE

        --strip-trailing-cr

strip trailing carriage return on input

        -a, --text

treat all files as text

        -w, --width=NUM

output at most NUM (default 130) print columns

        -l, --left-column

output only the left column of common lines

        -s, --suppress-common-lines

do not output common lines

        -t, --expand-tabs

expand tabs to spaces in output

        --tabsize=NUM

tab stops at every NUM (default 8) print columns

        -d, --minimal

try hard to find a smaller set of changes

        -H, --speed-large-files

assume large files, many scattered small changes

        --diff-program=PROGRAM

use PROGRAM to compare files


--help display this help and exit

        -v, --version

output version information and exit

If a FILE is `-`, read standard input.
Exit status is 0 if inputs are the same, 1 if different, 2 if trouble.

##
# wdiff
## Synopsis

       wdiff [OPTION]... FILE1 FILE2
       wdiff -d [OPTION]... [FILE]

## Description

wdiff - Compares words in two files and report differences.

        -1, --no-deleted

inhibit output of deleted words

        -2, --no-inserted

inhibit output of inserted words

        -3, --no-common

inhibit output of common words

        -a, --auto-pager

automatically calls a pager

        -d, --diff-input

use single unified diff as input

        -h, --help

display this help then exit

        -i, --ignore-case

fold character case while comparing

        -l, --less-mode

variation of printer mode for "less"

        -n, --avoid-wraps

do not extend fields through newlines

        -p, --printer

overstrike as for printers

        -s, --statistics

say how many words deleted, inserted etc.

        -t, --terminal

use termcap as for terminal displays

        -v, --version

display program version then exit

        -w, --start-delete=STRING

string to mark beginning of delete region

        -x, --end-delete=STRING

string to mark end of delete region

        -y, --start-insert=STRING

string to mark beginning of insert region

        -z, --end-insert=STRING

string to mark end of insert region

## Compatibility

Some  options that  used  to provide  some unique  functionality  are no  longer
recommended, but still recognized for the sake of backward compatibility.

        -K, --no-init-term

Now synonymous to --terminal, which never initializes the terminal.

##
# ?

    vim -d file1 file2

            Lancer Vim en chargeant 2 fichiers dans 2  fenêtres, et en activant le mode 'diff' dans
            chacune d'elles.


    diff file1 file2 | vim -R -

            Affiche les différences entre 2 fichiers dans un buffer Vim.


    vim -d  =(ls -l dir1)  =(ls -l dir2)

            Afficher les éléments différents contenus dans dir1/ et dir2/.

            =(cmd) est une construction propre à zsh qui est automatiquement
            développée en un nom de fichier (situé ds /tmp) contenant le résultat de `cmd`.

            Il paraît que  =(cmd)  est plus puissant  <(cmd) , car cette dernière
            construction repose sur des pipes qui peuvent poser pb qd la sortie
            de `cmd` est importante et que `vimdiff` a besoin de faire une seconde
            pass sur les fichiers.


    Afficher les différences entre:

            ┌──────────────────────┬────────────────────────────────────────┐
            │ diff -u file1 file2  │ 2 fichiers                             │
            │                      │                                        │
            │                      │ -u = afficher 3 lignes de contexte     │
            │                      │      unifié                            │
            ├──────────────────────┼────────────────────────────────────────┤
            │ diff -ui file1 file2 │ idem mais en ignorant la casse         │
            │ diff -ub file1 file2 │ "                     les whitespace   │
            │ diff -uB file1 file2 │ "                     les lignes vides │
            │                      │                                        │
            │                      │ B = Blank lines                        │
            ├──────────────────────┼────────────────────────────────────────┤
            │ diff -ur dir1/ dir2/ │ 2 dossiers                             │
            ├──────────────────────┼────────────────────────────────────────┤
            │ diff <(cmd1) <(cmd2) │ la sortie de 2 commandes shell         │
            └──────────────────────┴────────────────────────────────────────┘

    diff -q file1 file2

            Si les fichiers sont différents, affiche un message et retourne 1.
            Autrement, retourne 0.


    diff -s version1 version2

            Si les fichiers sont différents, affiche un message et retourne 0.
            Autrement, affiche les lignes qui diffèrent et retourne 0.

