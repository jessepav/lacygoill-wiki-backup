# ?

man zshmisc

REDIRECTIONS WITH NO COMMAND

When a simple command consists of one  or more redirection operators and zero or
more parameter assignments, but no command name, zsh can behave in several ways.

If the parameter  NULLCMD is set, its value  will be used as a  command with the
given redirections.
If both NULLCMD  and READNULLCMD are set,  then the value of the  latter will be
used instead of that of the former when the redirection is an input.
The default for NULLCMD is `cat` and for READNULLCMD is `pager`.
Thus:

              < file

shows  the contents  of  file on  standard  output,  with paging  if  that is  a
terminal.
NULLCMD and READNULLCMD may refer to shell functions.

# ?

man zshmisc

REDIRECTION

If a command  is followed by & and  job control is not active,  then the default
standard input for the command is the empty file /dev/null.
Otherwise, the  environment for  the execution  of a  command contains  the file
descriptors of the invoking shell as modified by input/output specifications.

The following may appear anywhere in a simple command or may precede or follow a
complex command.
Expansion occurs before word or digit is used except as noted below.
If  the  result  of  substitution  on word  produces  more  than  one  filename,
redirection occurs for each separate filename in turn.

       < word

Open file word for reading as standard input.

       <> word

Open file word for reading and writing as standard input.
If the file does not exist then it is created.

       > word

Open file word for writing as standard output.
If the file does not exist then it is created.
If the  file exists,  and the  CLOBBER option  is unset,  this causes  an error;
otherwise, it is truncated to zero length.

       >| word
       >! word

Same as >, except  that the file is truncated to zero length  if it exists, even
if CLOBBER is unset.

       >> word

Open file word for writing in append mode as standard output.
If the  file does not  exist, and  the CLOBBER option  is unset, this  causes an
error; otherwise, the file is created.

       >>| word
       >>! word

Same as  >>, except  that the  file is  created if  it does  not exist,  even if
CLOBBER is unset.

       <<[-] word

The  shell input  is read  up to  a line  that is  the same  as word,  or to  an
end-of-file.
No parameter expansion, command substitution or filename generation is performed
on word.
The resulting document, called a here-document, becomes the standard input.

If any  character of word is  quoted with single or  double quotes or a  `\`, no
interpretation is placed upon the characters of the document.
Otherwise, parameter and command substitution  occurs, `\` followed by a newline
is removed, and `\` must be used  to quote the characters `\`, `$`, backtick and
the first character of word.

Note that word itself does not undergo shell expansion.
Backquotes in word do not have their usual effect; instead they behave similarly
to  double quotes,  except that  the  backquotes themselves  are passed  through
unchanged.
(This  information is  given for  completeness and  it is  not recommended  that
backquotes be  used.)  Quotes in the  form $'...' have their  standard effect of
expanding backslashed references to special characters.

If  <<- is  used, then  all leading  tabs are  stripped from  word and  from the
document.

       <<< word

Perform shell expansion on word and pass the result to standard input.
This is known as a here-string.
Compare the  use of word  in here-documents above,  where word does  not undergo
shell expansion.

       <& number
       >& number

The  standard  input/output  is  duplicated from  file  descriptor  number  (see
dup2(2)).

       <& -
       >& -

Close the standard input/output.

       <& p
       >& p   The input/output from/to the coprocess is moved to the standard input/output.

       >& word
       &> word

(Except where `>&  word` matches one of  the above syntaxes; `&>`  can always be
used  to avoid  this ambiguity.)   Redirects both  standard output  and standard
error (file descriptor 2) in the manner of `> word`.
Note that this does not have the same effect as `> word 2>&1` in the presence of
multios (see the section below).

       >&| word
       >&! word
       &>| word
       &>! word

Redirects both  standard output and  standard error  (file descriptor 2)  in the
manner of `>| word`.

       >>& word
       &>> word

Redirects both  standard output and  standard error  (file descriptor 2)  in the
manner of `>> word`.

       >>&| word
       >>&! word
       &>>| word
       &>>! word

Redirects both  standard output and  standard error  (file descriptor 2)  in the
manner of `>>| word`.

If one of the above is preceded by a digit, then the file descriptor referred to
is that specified by the digit instead of the default 0 or 1.
The order in which redirections are specified is significant.
The shell  evaluates each redirection  in terms  of the (file  descriptor, file)
association at the time of evaluation.
For example:

              ... 1>fname 2>&1

first associates file descriptor 1 with file fname.
It  then  associates file  descriptor  2  with  the  file associated  with  file
descriptor 1 (that is, fname).
If  the  order  of  redirections  were reversed,  file  descriptor  2  would  be
associated with the terminal (assuming file descriptor 1 had been) and then file
descriptor 1 would be associated with file fname.

The  `|&`  command  separator  described  in  Simple  Commands  &  Pipelines  in
zshmisc(1) is a shorthand for `2>&1 |`.

The various  forms of process  substitution, `<(list)`, and `=(list)`  for input
and `>(list)` for output, are often used together with redirection.
For example, if word in an output  redirection is of the form `>(list)` then the
output is piped to the command represented by list.
See Process Substitution in zshexpn(1).

# ?

man zshexpn

PROCESS SUBSTITUTION

Each part  of a  command argument  that takes the  form `<(list)`,  `>(list)` or
`=(list)` is subject to process substitution.
The expression  may be  preceded or  followed by other  strings except  that, to
prevent clashes with commonly occurring strings and patterns, the last form must
occur at the start  of a command argument, and the forms  are only expanded when
first parsing command or assignment arguments.
Process substitutions may be used following redirection operators; in this case,
the substitution must appear with no trailing string.

Note that `<<(list)` is  not a special syntax; it is  equivalent to `< <(list)`,
redirecting standard input from the result of process substitution.
Hence all the following documentation applies.
The second form (with the space) is recommended for clarity.

In the  case of  the < or  > forms,  the shell  runs the commands  in list  as a
subprocess of the job executing the shell command-line.
If the system  supports the /dev/fd mechanism, the command  argument is the name
of the device file corresponding to  a file descriptor; otherwise, if the system
supports named pipes (FIFOs), the command argument will be a named pipe.
If the form  with > is selected  then writing on this special  file will provide
input for list.
If <  is used,  then the file  passed as  an argument will  be connected  to the
output of the list process.
For example,

              paste <(cut -f1 file1) <(cut -f3 file2) |
              tee >(process1) >(process2) >/dev/null

cuts fields  1 and  3 from the  files file1 and  file2 respectively,  pastes the
results together, and sends it to the processes process1 and process2.

If =(...) is used instead of <(...), then the file passed as an argument will be
the name of a temporary file containing the output of the list process.
This may be used instead of the <  form for a program that expects to lseek (see
lseek(2)) on the input file.

There is an optimisation for substitutions of the form `=(<<<arg)`, where arg is
a single-word argument to the here-string redirection `<<<`.
This  form  produces  a  file  name  containing  the  value  of  arg  after  any
substitutions have been performed.
This is handled entirely within the current shell.
This is effectively  the reverse of the special form  `$(<arg)` which treats arg
as a file name and replaces it with the file's contents.

The = form  is useful as both  the /dev/fd and the named  pipe implementation of
<(...) have drawbacks.
In the former case, some programmes  may automatically close the file descriptor
in question before examining the file  on the command-line, particularly if this
is necessary for security reasons such as when the programme is running setuid.
In  the second  case, if  the programme  does not  actually open  the file,  the
subshell  attempting to  read from  or  write to  the  pipe will  (in a  typical
implementation, different operating systems  may have different behaviour) block
for ever and have to be killed explicitly.
In both cases, the shell actually supplies the information using a pipe, so that
programmes that expect to lseek (see lseek(2)) on the file will not work.

Also  note that  the  previous example  can be  more  compactly and  efficiently
written (provided the MULTIOS option is set) as:

              paste <(cut -f1 file1) <(cut -f3 file2) \
              > >(process1) > >(process2)

The  shell uses  pipes instead  of  FIFOs to  implement the  latter two  process
substitutions in the above example.

There is  an additional  problem with  >(process); when this  is attached  to an
external command, the parent shell does not wait for process to finish and hence
an immediately following command cannot rely on the results being complete.
The problem  and solution are  the same as described  in the section  MULTIOS in
zshmisc(1).
Hence in a simplified version of the example above:

              paste <(cut -f1 file1) <(cut -f3 file2) > >(process)

(note that no  MULTIOS are involved), process will be  run asynchronously as far
as the parent shell is concerned.
The workaround is:

              { paste <(cut -f1 file1) <(cut -f3 file2) } > >(process)

The extra processes here  are spawned from the parent shell  which will wait for
their completion.

Another  problem arises  any time  a  job with  a substitution  that requires  a
temporary file is disowned  by the shell, including the case  where `&!` or `&|`
appears at the end of a command containing a substitution.
In that case  the temporary file will not  be cleaned up as the  shell no longer
has any memory of the job.
A workaround is to use a subshell, for example,

              (mycmd =(myoutput)) &!

as the  forked subshell  will wait  for the  command to  finish then  remove the
temporary file.

A general workaround to ensure a process substitution endures for an appropriate
length of time  is to pass it as  a parameter to an anonymous  shell function (a
piece of shell code that is run immediately with function scope).
For example, this code:

              () {
                 print File $1:
                 cat $1
              } =(print This be the verse)

outputs something resembling the following

              File /tmp/zsh6nU0kS:
              This be the verse

The temporary file created by the  process substitution will be deleted when the
function exits.

# ?

man bash

REDIRECTION

Before a  command is executed,  its input and output  may be redirected  using a
special notation interpreted by the shell.
Redirection allows commands' file handles to be duplicated, opened, closed, made
to refer to different files, and can change the files the command reads from and
writes to.
Redirection  may also  be  used to  modify  file handles  in  the current  shell
execution environment.
The  following redirection  operators may  precede or  appear anywhere  within a
simple command or may follow a command.
Redirections are processed in the order they appear, from left to right.

Each redirection that may be preceded by a file descriptor number may instead be
preceded by a word of the form {varname}.
In this case, for  each redirection operator except >&- and  <&-, the shell will
allocate a file descriptor greater than or equal to 10 and assign it to varname.
If >&- or  <&- is preceded by  {varname}, the value of varname  defines the file
descriptor to close.

In the following descriptions, if the file descriptor number is omitted, and the
first character of the redirection operator  is <, the redirection refers to the
standard input (file descriptor 0).
If the first character of the  redirection operator is >, the redirection refers
to the standard output (file descriptor 1).

The  word following  the  redirection operator  in  the following  descriptions,
unless  otherwise  noted, is  subjected  to  brace expansion,  tilde  expansion,
parameter and  variable expansion,  command substitution,  arithmetic expansion,
quote removal, pathname expansion, and word splitting.
If it expands to more than one word, bash reports an error.

Note that the order of redirections is significant.
For example, the command

              ls > dirlist 2>&1

directs both standard  output and standard error to the  file dirlist, while the
command

              ls 2>&1 > dirlist

directs only the standard output to file dirlist, because the standard error was
duplicated from the standard output before the standard output was redirected to
dirlist.

Bash handles several filenames specially when  they are used in redirections, as
described in the following table:

              /dev/fd/123
                     file descriptor 123 is duplicated.
              /dev/stdin
                     File descriptor 0 is duplicated.
              /dev/stdout
                     File descriptor 1 is duplicated.
              /dev/stderr
                     File descriptor 2 is duplicated.

A failure to open or create a file causes the redirection to fail.

Redirections using file descriptors greater than  9 should be used with care, as
they may conflict with file descriptors the shell uses internally.

Note that  the exec  builtin command  can make redirections  take effect  in the
current shell.

   Redirecting Input

Redirection of  input causes the file  whose name results from  the expansion of
word to be opened for reading on  file descriptor n, or the standard input (file
descriptor 0) if n is not specified.

The general format for redirecting input is:

              [n]<word

   Redirecting Output

Redirection of output  causes the file whose name results  from the expansion of
word to be opened for writing on file descriptor n, or the standard output (file
descriptor 1) if n is not specified.
If the file  does not exist it is  created; if it does exist it  is truncated to
zero size.

The general format for redirecting output is:

              [n]>word

If the redirection  operator is >, and  the noclobber option to  the set builtin
has been enabled, the redirection will fail  if the file whose name results from
the expansion of word exists and is a regular file.
If the  redirection operator  is >|, or  the redirection operator  is >  and the
noclobber option to  the set builtin command is not  enabled, the redirection is
attempted even if the file named by word exists.

   Appending Redirected Output

Redirection of  output in this fashion  causes the file whose  name results from
the expansion of  word to be opened  for appending on file descriptor  n, or the
standard output (file descriptor 1) if n is not specified.
If the file does not exist it is created.

The general format for appending output is:

              [n]>>word

   Redirecting Standard Output and Standard Error

This  construct allows  both the  standard output  (file descriptor  1) and  the
standard error  output (file descriptor  2) to be  redirected to the  file whose
name is the expansion of word.

There are two formats for redirecting standard output and standard error:

              &>word
       and
              >&word

Of the two forms, the first is preferred.
This is semantically equivalent to

              >word 2>&1

When using the second form, word may not expand to a number or -.
If it does, other redirection  operators apply (see Duplicating File Descriptors
below) for compatibility reasons.

   Appending Standard Output and Standard Error

This  construct allows  both the  standard output  (file descriptor  1) and  the
standard error output (file descriptor 2) to  be appended to the file whose name
is the expansion of word.

The format for appending standard output and standard error is:

              &>>word

This is semantically equivalent to

              >>word 2>&1

(see Duplicating File Descriptors below).

   Here Documents

This type  of redirection  instructs the  shell to read  input from  the current
source until a line containing only delimiter (with no trailing blanks) is seen.
All of the lines read up to that point are then used as the standard input for a
command.

The format of here-documents is:

              <<[-]word
                      here-document
              delimiter

No parameter and variable expansion, command substitution, arithmetic expansion,
or pathname expansion is performed on word.
If any  characters in  word are  quoted, the  delimiter is  the result  of quote
removal on word, and the lines in the here-document are not expanded.
If word is  unquoted, all lines of the here-document  are subjected to parameter
expansion,  command  substitution,  and   arithmetic  expansion,  the  character
sequence \<newline> is ignored, and \ must be used to quote the characters \, $,
and backtick.

If the redirection operator is <<-, then all leading tab characters are stripped
from input lines and the line containing delimiter.
This allows  here-documents within  shell scripts  to be  indented in  a natural
fashion.

   Here Strings

A variant of here documents, the format is:

              <<<word

The  word undergoes  brace expansion,  tilde expansion,  parameter and  variable
expansion, command substitution, arithmetic expansion, and quote removal.
Pathname expansion and word splitting are not performed.
The result is supplied as a single string to the command on its standard input.

   Duplicating File Descriptors

The redirection operator

              [n]<&word

is used to duplicate input file descriptors.
If word expands to one or more digits,  the file descriptor denoted by n is made
to be a copy of that file descriptor.
If  the digits  in word  do not  specify  a file  descriptor open  for input,  a
redirection error occurs.
If word evaluates to -, file descriptor n is closed.
If n is not specified, the standard input (file descriptor 0) is used.

The operator

              [n]>&word

is used similarly to duplicate output file descriptors.
If n is not specified, the standard output (file descriptor 1) is used.
If  the digits  in word  do not  specify a  file descriptor  open for  output, a
redirection error occurs.
If word evaluates to -, file descriptor n is closed.
As a  special case, if  n is omitted,  and word does not  expand to one  or more
digits or -, the standard output  and standard error are redirected as described
previously.

   Moving File Descriptors

The redirection operator

              [n]<&digit-

moves the  file descriptor  digit to  file descriptor n,  or the  standard input
(file descriptor 0) if n is not specified.
digit is closed after being duplicated to n.

Similarly, the redirection operator

              [n]>&digit-

moves the  file descriptor digit  to file descriptor  n, or the  standard output
(file descriptor 1) if n is not specified.

   Opening File Descriptors for Reading and Writing

The redirection operator

              [n]<>word

causes  the file  whose name  is the  expansion of  word to  be opened  for both
reading and writing  on file descriptor n, or  on file descriptor 0 if  n is not
specified.
If the file does not exist, it is created.

# ?

There is a problem when an output multio is attached to an external program.
A simple example shows this:

        cat file >file1 >file2
        cat file1 file2

        cat file* V

Here, it is possible that the second `cat` will not display the full contents of
file1 and file2 (i.e. the original contents of file repeated twice).

The reason  for this is that  the multios are  spawned after the cat  process is
forked from the parent shell, so the  parent shell does not wait for the multios
to finish writing data.
This means the command  as shown can exit before file1  and file2 are completely
written.
As a workaround, it is  possible to run the cat process as part  of a job in the
current shell:

        { cat file } >file >file2

Here, the {...} job will pause to wait for both files to be written.

# ?

If the  user tries to  open a  file descriptor for  reading more than  once, the
shell opens it  as a pipe to a  process that copies all the  specified inputs to
its output in the order specified, similar to cat.
Thus:

        sort <foo <foobar

or even:

        sort <foo{,bar}

is equivalent to `cat foo foobar | sort`.

Expansion of  the redirection argument  occurs at  the point the  redirection is
opened, at the point described above for the expansion of the variable in
>&$myfd.

Note that a pipe is an implicit redirection; thus:

        cat bar | sort <foo

is equivalent to `cat bar foo | sort` (note the order of the inputs).

# ?

If the  user tries to  open a  file descriptor for  writing more than  once, the
shell opens it as a pipe to a process that copies its input to all the specified
outputs, similar to tee.
Thus:

        date >foo >bar

writes the date to two files, named `foo` and `bar`.
Note that a pipe is an implicit redirection; thus

        date >foo | cat

writes the date to the file `foo`, and also pipes it to cat.

Note also that redirections are always expanded in order.
For example,  the meaning  of the  expression >&1 will  change after  a previous
redirection:

        date >&1 >output

In the  case above, the >&1  refers to the standard  output at the start  of the
line; the result is similar to the tee command.
However, consider:

        date >output >&1

As redirections are evaluated in order, when the >&1 is encountered the standard
output is  set to the file  output and another  copy of the output  is therefore
sent to that file.
This is unlikely to be what is intended.

If the  MULTIOS option  is set, the  word after a  redirection operator  is also
subjected to filename generation (globbing).
Thus:

        : > *

will truncate all files in the current directory, assuming there's at least one.
(Without  the  MULTIOS option,  it  would  create  an  empty file  called  `\*`.)
Similarly, you can do

        echo exit 0 >> *.sh

# ?

OPENING FILE DESCRIPTORS USING PARAMETERS

When  the  shell  is parsing  arguments  to  a  command,  and the  shell  option
IGNORE_BRACES is not set, a different form of redirection is allowed: instead of
a  digit before  the operator  there  is a  valid shell  identifier enclosed  in
braces.
The shell will open  a new file descriptor that is guaranteed to  be at least 10
and set the parameter named by the identifier to the file descriptor opened.
For example:

               ┌ no whitespace is allowed between the closing brace
               │ and the redirection operator
               │
        : {myfd}>&1
        echo $myfd
        11~

This opens a  new file descriptor that  is a duplicate of file  descriptor 1 and
sets the parameter myfd  to the number of the file descriptor,  which will be at
least 10.
The new file descriptor can be written to using the syntax >&$myfd.

It is  an error  to open or  close a  file descriptor in  this fashion  when the
parameter is readonly.
However, it is not an error to read or write a file descriptor using <&$param or
>&$param if param is readonly.

If the option CLOBBER is unset, it is an error to open a file descriptor using a
parameter that is already set to an open file descriptor previously allocated by
this mechanism.
Unsetting the parameter before using it  for allocating a file descriptor avoids
the error.

Note that this  mechanism merely allocates or closes a  file descriptor; it does
not perform any redirections from or to it.
It  is usually  convenient to  allocate a  file descriptor  prior to  use as  an
argument to exec.
The syntax does not  in any case work when used around  complex commands such as
parenthesised subshells or loops, where the opening brace is interpreted as part
of a command list to be executed in the current shell.

The following shows a typical sequence of allocation, use, and closing of a file
descriptor:

      integer myfd
      exec {myfd}>~/logs/mylogfile.txt
      print This is a log message. >&$myfd
      exec {myfd}>&-
           ├───────┘
           └ close the file descriptor stored in $myfd

Note that the expansion of the variable  in the expression >&$myfd occurs at the
point the redirection is opened.
This is after  the expansion of command arguments and  after any redirections to
the left on the command-line have been processed.

# ?

        cmd <<EOF

Rediriger tout ce qui est tapé au clavier (jusqu'au tag EOF) en entrée à cmd.

Les données tapées subissent 2 développements et une substitution:

        - parameter expansion
        - arithmetic expansion
        - command substitution

On peut le vérifier en tapant la commande: `cat <<EOF`.
Puis en tapant $PATH au sein des données.

Pour empêcher tout développement/substitution, il faut quoter le tag:

        cmd <<'EOF'

##
##
##
# Can several processes use the terminal to write their output simultaneously?

Yes.

# Can several processes use the keyboard to read their input simultaneously?

No.

##
# What does `3>&-` do?

It closes fd3.

`>&-` is an alternative syntax to `>/dev/null`.

# What does `4>&3` do?

It duplicates fd4 from fd3.

IOW, it opens  fd4 (if it didn't  exist) or reconnects it (if  it existed), with
write mode, to the same file to which fd3 is connected.

##
# Where are the errors go after executing `ls /tmp /foo 2>&1 | less`?

Inside the less pager.

`2>&1` duplicates the fd2 of `ls` from fd1, which is connected to the pipe.

Without `2>&1`, the output of `ls` would be printed in the pager, but not the errors.
The latter would be printed on the terminal.

# Where are the errors be printed after executing `ls /tmp /foo 2>&1 >file`?

In the terminal.

Indeed, when `2>&1` is processed, fd1 is connected to the terminal.

# Where are the stdout and stderr of `ls` printed after executing `ls /tmp /foo 2>&1 >file | less`?

The stdout is written in `file`.
The stderr in the pager.

Indeed, `>file` is processed after `|`, and so has the last word on where stdout goes.
And, when `2>&1` is processed, fd1 is connected to the pipe, so fd2 is too.

# What does the pager print after executing `ls /tmp /foo >file 2>&1 | less`?

Nothing.

Initially,  all the  streams  are redirected  to  the pipe,  but  then they  are
successively redirected to `file`.

##
# What does the redirection in `echo 'hello' >file` do?

It reconnects echo's fd1 with write mode from the terminal to `file`.

##
# What will this command output: `cd ~ ; echo '/tmp' | ls` ?

The contents of `~`.
It won't list the contents of `/tmp`, because `$ ls` doesn't read its stdin.

Many other commands ignore their stdin: `cd`, `cp`, `readlink`, ...

---

If you really wanted to pass the output of  a command to `$ ls`, you could use a
command substitution:

        ls $(echo '/tmp')

Or `$ xargs`:

        echo '/tmp' | xargs ls

##
# When I start a shell, which file descriptors does the kernel open for the latter?

        0
        1
        2

# How are they often called?

        ┌───┬────────┐
        │ 0 │ stdin  │
        ├───┼────────┤
        │ 1 │ stdout │
        ├───┼────────┤
        │ 2 │ stderr │
        └───┴────────┘

# With which modes are they opened?

        ┌────────┬────────┐
        │ stdin  │ read   │
        ├────────┼────────┤
        │ stdout │ write  │
        ├────────┼────────┤
        │ stderr │ append │
        └────────┴────────┘

# Which file(s) are they connected to?

Stdin is connected to the keyboard via the terminal.

Stdout and stderr are connected to the terminal.

# Why does the kernel do that?

The shell needs places to read and write information.

#
# Why does `echo hello` write 'hello' on the terminal?

The `$ echo` process is a child of the current shell.
As a result, it has inherited its file descriptors.
In particular, the fd1 of the shell is by default connected, with write mode, to
the current terminal.
So, the fd1 of `$ echo` is also the current terminal.

#
# If I give a filename as a parameter to a unix command (`grep`, `less`, ...), what is its stdin connected to?

It's not connected to anything.
It's unused.

Which is logical, as the stdin can't be connected to the filename.
Indeed, you can  often pass several filenames  to a unix command,  but the stdin
couldn't be connected to all of them simultaneously.

# If I don't give a filename as a parameter to a unix command, what is its stdin connected to?

Usually, the keyboard via the terminal.

#
# What's the difference between `sort <file` and `sort file`?

The stdin of `sort` is used in the first command, not in the other.

        sort <file
    ⇔
        cat file | sort

##
# Can a command detect whether its stdout is connected to the terminal or to a file?

Yes.

    $ touch file{1..3}

    $ ls
    file1 file2 file3~

    $ ls >file && cat file
    file~
      file1~
      file2~
      file3~

The first `ls` wrote the files on a line, but the second did it on a column.
This is  because `ls` saw that  its stdin was  connected to the terminal  in the
first case, but to a file in the second one.

##
# How to get the set of file descriptors opened for a process?

        $ ls /proc/PID/fd

Example:

        $ ls /proc/$$/fd
        list of the fds opened for the current shell~

##
# How to redirect in a file all the messages and errors of the processes started from the current script?

        exec >file 2>&1

Don't use it for the current shell.
It works, but it messes up with interactive programs such as Vim.
Maybe because they expect their stdout to be connected to a terminal...

##
# How to do the same thing, but without losing the ability of printing a message or error on the terminal?

        exec 3>&1 4>&2
        exec 1>file 2>&1

Now, when you want  a command to print a message/error on  the terminal, use fd3
and/or fd4.

Example:

        cmd >&3 2>&1

It works, because before redirecting the stdout/stderr of the script, we've made
duplicates of the files to which they were originally connected to.
Through them, we can still write on the terminal.

---

Note that usually, stdin and stdout are both connected to the terminal.
So, you probably don't need to duplicate fd4 from fd2.

##
# How to redirect the output of `ls /tmp /foo` to `less`, and the errors to `wc -m`?

        { { ls /tmp /foo | less >&3 ;} 2>&1 | wc -m ;} 3>&1

Explanation:

First naive attempt:

        ls /tmp /foo | less | wc -m

            ✘: the stderr of `ls` is written on the terminal
            ✘: the stdout of `ls` is written on the stdin of `wc`

Second attempt:

        { ls /tmp /foo | less ;} 2>&1 | wc -m
        ^^                   ^^^ ^^^^

            ✔: the stderr of `ls` is written on the stdin of `wc`
            ✘: the stdout of `ls` is written on the stdin of `wc`

Why the `{ ... ;} 2>&1`?

We need to redirect the errors from `ls`, so we'll use `2>`.
We want to redirect them to the input of `wc`.
Which fd is connected to the input of `wc`? The stdout of `less`.
So, we need to redirect the errors to the stdout of `less`:

        ls /tmp /foo | less 2>&1 | wc -m
                            ^^^^
                            ✘ this doesn't redirect the errors of `ls`, but of `less`

We need a way to refer to the stderr of `ls` from the `less` command.
That's why we use `{ ... ;}`.

Note that this wouldn't work:

        ls /tmp /foo 2>&1 | less | wc -m
                       ^^
                       ✘ after the pipe, the stdout and the stderr will be mixed,
                         you won't have any way to determine which text is an error

Third attempt:

        # ✔
        { { ls /tmp /foo | less >&3 ;} 2>&1 | wc -m ;} 3>&1
        ^^                      ^^^                ^^^ ^^^^

Why `{ ... ;} 3>&1`?

Now, we need to prevent the stdout of `ls` to be redirected from `less` to `wc`.
So, we'll use `>` in the `less` command to redirect its output to the terminal.
But we don't have a fd for the terminal, so we create a duplicate with `{ ... ;} 3>&1`.

# How to close the fd 3 for all commands where it's unused?

        { { ls /tmp /foo 3>&- | less >&3 3>&- ;} 2>&1 | wc -l 3>&- ;} 3>&1
                         ^^^^            ^^^^                 ^^^^

# If the `less` command raises an error, it will be sent to `wc`.  How to send it to the terminal instead?

Duplicate  the fd  used initially  for the  errors of  the shell  (using fd  4),
because we know it's connected to what we need: the terminal.
And use it to reconnect the errors of `less` to the terminal:

        { { ls /tmp /foo | less >&3 2>&4 ;} 2>&1 | wc -l ;} 3>&1 4>&2
        ^^                          ^^^^^^^             ^^^      ^^^^

##
# How to save the contents of a file in a variable?

        var=$(<file)

# How to save the 9 words in a string inside separate variables?

        $ str='the quick brown fox jumps over the lazy dog'
        $ <<<"${str}" read word_{1..9}
        $ printf -- '%s\n' $word_{1..9}

By default, the stdin of `read` is connected to the keyboard (via the terminal).
But here, we reconnect it to a string.

##
##
##
# Concepts
## What's a file descriptor?

A positive integer.

## Where is it used as an index?

Inside a per-process (i.e. local to a process) file descriptor table.

## What does it point to?

A mode.

## What's that?

A mode describes how a file is accessed (read: <, write: >, append: <<).

## Where is it used as an index?

Inside a global file table.

## What does it point to?

An inode (inside a global inode table).

##

## What does a redirection do?

It changes the file to which an existing fd is connected, or it opens a new fd.

## What does “opening a fd” mean?

It's the act of creating a fd and connecting it to a file with a given mode.

## What does “closing a fd” mean?

It's  the act  of removing  the  file to  which  the fd  was connected,  without
replacing it with a new one.

## What does “duplicating a fd” mean?

It's the act of creating a new fd  (or using an existing one), and connect it to
the same file than another fd.

Every time you see `>&`, there's a fd duplication.

##
## What does “terminal” refer to, in the context of a redirection?

If you're in a pseudo terminal:

        /dev/pts/123

If you're in a console terminal:

        /dev/tty123

##
# Order
## When are the redirections inside `{ list ;}` processed, compared to the ones outside?  What about `(list)`?

The ones outside have the priority.

---

You need the spaces and the semicolon in the first syntax, but only in bash:

        { list ;}
         ^    ^^

## What's the consequence of this?

The commands inside `list` inherit the redirections done outside.

## When are the explicit redirections processed, compared to the ones to a pipe?

The pipe has priority.

## In which order are the other redirections processed?

From the left to the right of the command-line.

##
# pipe
## What's the effect of the pipe operator?

It makes the  shell redirect the stdout  of the left process (fd1)  to a special
file (pipe), and redirect the stdin of the right process (fd0) to this same file
(pipe).

## Are all the commands in a pipeline executed in the current shell?

No, they are all executed in a subshell.

As a result, variables  you add or reset in a pipeline won't  take effect in the
current shell.

MWE:

        $ cd /tmp | true
        the cwd is NOT changed~

        $ var=hello | true
        $ echo $var
        ∅~

---

Exception: in  zsh, the  last simple command  of a pipeline  is executed  in the
current shell.

MWE:

        % true | cd /tmp
        the cwd IS changed~

        % true | var=hello
        % echo $var
        hello~

##
# process substitution
## What does `>(cmd)` mean?

   1. create a temporary file
   2. anything which will be written inside, send it to the stdin of `cmd`

---

Example:

    $ echo 'hello' > >(wc -m)
    6~

This example was equivalent to:

    $ echo 'hello' >/tmp/file
                    ├───────┘
                    └ anything written here will be sent the stdin of `wc -m`

    $ echo hello | wc -m

## What are the 3 main differences between `<()` and `>()`?

Both are replaced by a temporary file.

With `<(cmd)`, the file is populated with the output of `cmd`.
With `>(cmd)`, the file is populated with nothing.

With `<(cmd)`, the file is opened with read mode.
With `>(cmd)`, the file is opened with write mode.

With `<(cmd)`, `cmd` is used to populate the file.
With `>(cmd)`, `cmd` is passed the file on its stdin.

##
# zsh
## What does the MULTIOS option control?

When set, it allows you to redirect standard streams of a process to several files.
Example:

    % echo hello >foo >bar

## What happens if I execute `echo hello >foo >bar`, while the MULTIOS option is unset?

`foo` will be truncated.
'hello' will be written into `bar`.

This is because  each redirection for a given file  descriptor (here we redirect
for the fd 1) replaces the previous redirection for the same file descriptor.

##
# Issues
## Why doesn't this command work as expected: `cmd some_file >some_file`?

When the  shell parses the  command, and sees  the `>` redirection  operator, it
immediately empties/truncates the contents of `some_file`.

As a result, `cmd` will read an empty file.

---

Instead, you should use a temporary file:

        $ cmd some_file >temp_file
        $ cat temp_file >some_file
        $ rm temp_file

Or, try to find an option in the manpage of `cmd` to operate in-place.
Example:

        # ✘
        sed -e 's/foo/bar/' file >file

        # ✔
        sed -i 's/foo/bar/' file
             ^
             in-place option

## How to move the contents of `file1` in `file2` without breaking the hard link `ln file2 hardlink`?

        $ cp file1 file2
Or:
        $ cat file1 >file2 && rm file1

`$ cp` and  a redirection will both  preserve the hard link,  because they don't
create a new file if they don't need to.
They just overwrite the contents of an existing file when they can.
So the inode number is left unchanged.

Do NOT use `$ mv`.
If `file2` is a  hard link referring to an existing file, `$  mv` will break the
link because it creates a new file `file2` with a new inode number.

---

In the following examples, `file2` is a hard link.
Watch what happens to it in the three following commands:

        $ echo 'hello' >file1  && \
          echo 'bye'   >file3  && \
          ln file3 file2       && \
          mv file1 file2       && \
          cat file2 file3
          hello~
          bye~

        # `file2` and `file3` do NOT have the same inode number anymore


        $ echo 'hello' >file1  && \
          echo 'bye'   >file3  && \
          rm file2             && \
          ln file3 file2       && \
          cp file1 file2       && \
          cat file2 file3
          hello~
          hello~

        $ echo 'hello' >file1           && \
          echo 'bye'   >file3           && \
          rm file2                      && \
          ln file3 file2                && \
          cat file1 >file2 && rm file1  && \
          cat file2 file3
          hello~
          hello~

In the last two commands, `file2` and `file3` STILL have the same inode number.

##
## Why does this command fail:  `sudo echo '# hello' >>/etc/apt/sources.list`?

Because the shell processes the redirection before executing the command.
And  when it  does,  it tries  to open  `/etc/apt/sources.list`,  but fails  to,
because it doesn't have enough rights (`sudo` hasn't been started yet).

For more info, see:
        https://unix.stackexchange.com/a/279489/289772

## How to append the output of a command to a system file?

        $ cmd | sudo tee -a system_file

It works because there's no redirection to `system_file`.
`$ tee` writes the output of `$ cmd` on the terminal and append it to `system_file`.
It can because it's started as if it was by the root user.

---

Alternatively, you could start a root shell:

        $ sudo sh -c 'cmd >>system_file'

