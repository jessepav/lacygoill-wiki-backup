# general
## review `printf` everywhere

unnecessary  double quotes,  extract interpolations  using %s  items, replace  a
multi-line printf with a here-doc ...

## Precedence of the shell logical operators &&, ||

<https://unix.stackexchange.com/a/88851/289772>

## Do these substitutions: `~ → ${HOME}` and `"${HOME}"/file → "${HOME}/file"`

    [ ... ] → [[ ... ]] (noa vim /\s\[\s/gj ~/bin/**/*.sh | cw)

## When should we quote `HOME`?

Search for `HOME` in zshrc/bashrc.
Should we quote all the time?
Example:

            v                           v v                                v
    fpath=( "${HOME}/.zsh/my-completions" "${HOME}/.zsh/zsh-completions/src" $fpath )
                                                                              ^----^
                                                                              what about that?
                                                                              ${fpath}?
                                                                              "${fpath}"?
Example:

    [[ -f "${HOME}/.fzf.zsh" ]] && . "${HOME}/.fzf.zsh"
          ^                ^

Example:

    export CDPATH=:"${HOME}":/tmp
                   ^       ^

See: <https://unix.stackexchange.com/a/68748/289772>

## How do I extract data from an HTML or XML file?

<http://mywiki.wooledge.org/BashFAQ/113>

##
# Miscellaneous
## learn factoids from greybot (bot on irc channel `#bash` on freenode)

            │ !greybot
    greybot │ I'm a bot. I'm written in perl. My source, factoids, and stats are at http://wooledge.org/~greybot/
            │  See !help for a list of my commands. git mirror https://github.com/im14/greybot

You can find all the factoids here: <http://wooledge.org/~greybot/meta/>
In each factoid, you'll often find the commands `learn` and `forget`.
I think that `learn` make the bot register a factoid, while `forget` unregister it.
Anyway, always read the last `learn` command, because all the previous ones are outdated.

##
# scripts
## ideas to improve our scripts:

When a script  bugs several times, immediately consider adding  a DEBUG variable
set by default to 0.
Then, write `printf`  statements in the most useful locations,  to get debugging
info.
Guard those statements by checking the value of `DEBUG`.
Have a look at what we did in upp.

---

They should better handle errors  (no stacktrace, show a human-readable message;
take inspiration from `mv garb age`).

---

Usage when the script is called without arguments.
Should we delegate this to a library function to avoid repeating always the same
kind of code?

---

Use the output streams correctly.

Write error messages on stderr, not on stdout.
This way, if you pipe the output of your script to another utility, and an error
is raised, the message won't be sent to the utility.
There's no sense piping an error message to anything.
Same thing  for a usage message  (which can be seen  as a special kind  of error
message).
And if  the user really  wants to  pipe the error  message, they still  can with
`2>&1 |` (or `|&`).

---

An error message should always contain  the name of the script/function which is
executed:

    script_name: error message

Example:

    $ mv x y
     → mv: cannot stat 'x': No such file or directory
       ^^

This  is  useful  when you  execute  it  in  a  pipeline, because  it  lets  you
immediately know from which simple command in the pipeline the error comes.

However, don't write the name literally.
Use `$0`  in a  function, and  `$(basename "$0")` in  a script,  so that  if you
change the name of the script/function later, the message remains valid.

---

Any error should be accompanied by an `exit` statement, so that:

    ./script.sh && echo 'success'

doesn't print 'success' if the script fails.

Use `exit  1` for a random  error, `exit 64` for  a usage message, `65`  for bad
user input, and `77` for not enough permission.
See here for which code to use:
<https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html>

It's not an obligation to use this page, just a useful convention.

---

Write a manpage for the script.

---

Split a long command using an array whose elements are arguments of the latter:
<https://unix.stackexchange.com/a/473257/289772>

---

Use lowercase characters for variables/parameters, and uppercase for environment
variables It's just a convention suggested on page 74 of “from bash to z shell”.
It's not really followed in this zshrc:
<http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc>

It doesn't seem there's any convention in this file.
Except that most  of the time, the  local variables in a  function use lowercase
characters.

---

Read: <http://www.kfirlavi.com/blog/2012/11/14/defensive-bash-programming/>

## Make sure to never abuse the `local` keyword.

Remember the issue we had created in `gifrec`.
Note that  the variables set  by a script should  not affect the  current shell,
because the script is executed in a subshell.
So, is it recommended to use `local` in the functions of a script?

Update:
The google style guide recommends to always use them.
Maybe  we should  re-use `local`  in `gifrec`,  and pass  the variables  as
arguments between functions...
What about `VERSION` inside `upp`? Should we make this variable local?

Update:
These variables are indeed in a function, but they don't have to.
We  could remove the  functions, and just execute  the code directly  from the
script.
We've put them in functions to make the code more readable.
IOW, I think they are supposed to be accessible from the whole script.

##
# zsh
## Implement your own version of the `tldr` command.

Write files named `tldr/mycmd.txt` in various wikis.
Inside, write the most useful invocations of `mycmd`.
Extract them from your notes (e.g. strace.md).
Your notes should  not contains shortcuts (that's better for  a cheatsheet), nor
should they contain one-liner answers (those should be in a tldr file).
Why?
Because, these information would be quicker to access that way.

Then, write  a shell  `td` command  (Too long Didn't  read) which  suggests such
files and echo them in the terminal, just like `tldr`.
Inside the files,  use escape sequences via `tput(1)` to  add some styles (bold,
italic, bold+italic):

    $ printf 'some %s bold %s text' $(tput bold) $(tput sgr0)
    $ printf 'some %s bold %s text' $(tput sitm) $(tput sgr0)
    $ printf 'some %s bold+italic %s text' "$(tput bold)$(tput sitm)" $(tput sgr0)

Use  this  command to  print  the  file, so  that  the  sequences are  correctly
interpreted:

    $ while read -r line; do printf -- "$line\n"; done </tmp/file

Try to give the files a dedicated filetype, and conceal the escape sequences.

---

Use fzf to fuzzy search through all tldr files.
Same thing for the cheatsheets.

---

Write your files in a `tldr/` subdirectory, and use markdown (for folding).

---

Install a mapping (`-D`?) to get a tldr window when you press it on a command name.
Same thing for a cheatsheet window.

---

Install a local key binding in any tldr file to fuzzy search through all shell
commands given in answers.
In  the preview  pane,  make fzf  display a  description  (maybe the  question
associated with the command).
When you select a command, make fzf write  it in the clipboard, so that we can
paste it immediately on the shell's command-line.

## Add a preview window for our zsh snippets.  Like what we did with `:Rg`.

## Think about how we could better leverage our zsh history.

For  example,   whenever  you  press   `C-r`  several  times  to   retrieve  the
same  old  command, immediately  consider  adding  it  to  our zsh  snippets  in
`~/.config/zsh-snippet/`.

Also, try  to build  a script  or Vim  command to  remove as  much noise  in the
history.

Also, try  to build an awk  script to extract  relevant info; like what  are the
most used commands.
Act upon this info, write scripts or  snippets to reduce the invocation of these
commands.

Also, take  the habit of  prefixing your commands with  a space when  you're not
sure they work.
Otherwise, you may end up with broken commands in your history.
Those are not interesting, and may be even dangerous.

## sometimes the distance between tab-completed candidates is too unconsistent

Type `$ vim Tab` (press Tab right after `vim`, don't insert a space).
Look at the distance between the suggestions in the `shell function` section.
It's too big.
The result feels jarring compared to the other sections.
I think it's  because zsh tries to use  a certain width for the  whole menu, and
divides it by `n` (`n` being the number of suggestions on a given line).
If `n` is small  (atm we only have 3 shell functions  beginning with `vim`), the
width of each suggestion on a line is needlessly big.

It seems that  the completion menu splits the suggestions  on several lines once
there're 10 of them (at least if their size is similar to `vim_cfg`).

How to control the geometry of the zsh completion menu?
Width of the suggestions, max number of entries on a single line ... It would be
useful to tell zsh that if we have  less than, say, 10 suggestions, we want them
each on a separate line.
Or better yet, how to ask zsh to fill columns, before filling lines?

The  `list_rows_first` option  doesn't seem  to help... The  latter changes  the
position of  entries in a  completion menu: For example, the  2nd one is  on the
right of the 1st one, instead of below.

## automatically highlight in red special characters on the command line

Use this regex to find all non ascii characters:

    [^\x00-\x7F]

Read `man zshzle`, section `special widgets`:

>     zle-line-pre-redraw
>            Executed  whenever  the  input  line  is  about  to be redrawn,
>            providing an opportunity to update the region_highlight array.

Also read this:
<https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/docs/highlighters/regexp.md>

## outrageously-useful-tips-to-master-your-z-shell

Read this tuto:
<http://reasoniamhere.com/2014/01/11/outrageously-useful-tips-to-master-your-z-shell/>

## implement the key binding `M-Del` to delete from the cursor back to the previous whitespace.

There's also a `quote-line` command bound to M-' by default.
As the name suggests, it quotes the entire line.
No need to select a region.

## check that none of our alias can shadow a future command from the repos

    $ apt-file update
    $ apt-file -x search '/myalias$'

## how-to-deal-with-filenames-containing-a-single-quote-inside-a-zsh-completion-fun

Read and understand this:
<https://unix.stackexchange.com/questions/366549/how-to-deal-with-filenames-containing-a-single-quote-inside-a-zsh-completion-fun>

## assimilate pure.zsh plugin (zsh prompt)

<https://github.com/sindresorhus/pure>
(≈ 550 sloc, 2 fichiers: pure.zsh, async.zsh)

## read this (about glob qualifiers)

<https://unix.stackexchange.com/a/471081/289772>

## Install a key binding to kill ffmpeg.

It would be useful when we record our desktop, or the sound...

## Make zsh eat a dollar sign at the start of a pasted command.

Add this alias:

    alias \$=''

Source: <https://github.com/zpm-zsh/undollar/blob/master/undollar.plugin.zsh>

We can't do it now, because it would raise this error:

    zsh-syntax-highlighting: BUG: _zsh_highlight_main_highlighter_expand_path: called without argument~

This is due to: <https://github.com/zsh-users/zsh-syntax-highlighting/issues/565>
Wait for this other issue to be fixed, then add the alias.

## deploy-message

<https://gist.github.com/lacygoill/8019977145e6411ebb0fea516f7033e0>

