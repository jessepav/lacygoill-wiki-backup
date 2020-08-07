# Document:
## `--files-without-match`

It's supported by `grep(1)` and `rg(1)`.
For `grep(1)`, you can also use the short flag `-L`.

This  option  is useful  to  populate  the qfl  with  a  subset of  files  *not*
containing an arbitrary pattern:

    call setqflist(getqflist({'lines': systemlist('grep -L pattern files 2>/dev/null'), 'efm': '%f'}).items)
                                                        ^^

## `-c`

>     -c, --count
>            Suppress  normal output; instead print a count of matching lines
>            for each input file.  With the -v,  --invert-match  option  (see
>            below), count non-matching lines.

So, it seems that this is an anti-pattern:

    $ grep pat file | wc -l

Instead, you should run:

    $ grep -c pat file

##
# ?

    $ \rg -LS foobar /etc
    error: The argument '--follow' was provided more than once, but cannot be used multiple times~

    $ \rg -SL foobar /etc
    error: The argument '--smart-case' was provided more than once, but cannot be used multiple times~

Is it a bug?  If so, report it.

It looks similar to this other bug:
<https://github.com/BurntSushi/ripgrep/issues/884>

# ?

Document that it seems that only ripgrep  (and ag) can print several matches, on
a single input line,  on multiple dedicated output lines *with*  the rest of the
input line.

grep can  do the same thing  with `-o` but it  only prints the matches,  not the
rest of the line.

Also, only ripgrep (and ag) can print the column position of the match.
I think that grep can print the byte offset from the start of the file, which is
entirely different (and not very useful imo).

# ?

Document the fact that grep supports PCRE  (which is much more powerful than BRE
and ERE), provided that you pass it the option `-P`.

Note that PCRE is not fully compatible with Perl regexes:
<https://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions#Differences_from_Perl>

Read our book about regexes to fully exploit Perl regexes.

# ?

Document that the metacharacters `[]` can  be used to express a character class,
not only in a *grep* pattern, but also in a shell *file* pattern:

    $ touch file{1..5}
    $ echo 'pat' | tee file{2..4}
    $ grep pat file[24]
    file2:pat~
    file4:pat~

---

Also document  that you can't  include a closing  square bracket in  a character
class by escaping it.
You have to put it in first position:

    # ✘
    $ grep '[a\]b]' file

    # ✔
    $ grep '[]ab]' file
             ^

And if the character class is reversed, put it in second position:

    # ✔
    $ grep '[^]ab]' file
              ^

# ?

    grep -o pattern file        N'afficher que le pattern trouvé, autant de fois qu'il y a de matchs
                                et à chaque fois sur une ligne différente.
                                Par défaut, grep retourne toute la ligne sur laquelle un match a été trouvé.
                                -o, --only-matching

    grep -q pattern file        Ne rien afficher sur la sortie standard,
                                et s'arrêter dès qu'un match est trouvé en produisant le code de sortie 0.

                                Utile dans un script pour vérifier la présence d'une chaîne dans un fichier ou
                                sur la sortie standard d'une précédente commande suivie d'un pipe.

    grep -Rn pattern *          chercher pattern dans tous les fichiers et dossiers du répertoire courant,
                                récursivement (-R) et en faisant précéder chaque match du n° de la ligne du fichier
                                sur laquelle il se trouve (-n)

    grep pattern file               search a file for a pattern

    grep -in pattern file           Case insensitive search (with line numbers)

    grep -R pattern folder          Recursively grep for string <pattern> in folder

    grep -f pattern_file file       Read search patterns from a file (one per line)

    grep -v pattern file            Find lines NOT containing pattern

You can grep with regular expressions
    grep "^00" file  #Match lines starting with 00
    grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" file  #Find IP add

Find all files which match {pattern} in {directory}
This will show: "file:line my research"
    grep -rnw 'directory' -e "pattern"

Exclude grep from your grepped output of ps.
Add [] to the first letter.  Ex: sshd -> [s]shd
    ps aux | grep '[h]ttpd'

Colour in red {bash} and keep all other lines
    ps aux | grep -E --color 'bash|$'

