# I have a command which generates a completion function to complete some command.  How to use it?

Run it and save its output in a file in a directory of `$fpath`.
For example, for `$ pandoc`:

     $ pandoc --bash-completion >~/.zsh/my-completions/_pandoc
     $ sed -i '1i#compdef pandoc\n' ~/.zsh/my-completions/_pandoc

Add these commands to your script which  updates your system so that the code is
updated regularly.

Do *not* generate the code dynamically every  time you start a shell, by writing
for example sth like this in your zshrc:

     eval "$(pandoc --bash-completion)"

Or:

     . =(pandoc --bash-completion)

It would probably increase the starting time of a new shell.

##
# Issues
## I'm trying to use a bash completion function with bashcompinit, but it doesn't work!

It may not work, but try to add this to your zshrc:

     bash_source() {
       alias shopt=':'
       alias _expand=_bash_expand
       alias _complete=_bash_comp
       emulate -L sh
       setopt KSH_GLOB BRACE_EXPAND
       unsetopt SH_GLOB
       source "$@"
     }
     have() {
       unset have
       (( ${+commands[$1]} )) && have=yes
     }
     bash_source /path/to/my/completion_function

---

This makes  zsh ignore the bash  `shopt` builtin, and avoids  issues with common
bash functions that have the same name as zsh ones.

Source: <https://web.archive.org/web/20180404080213/http://zshwiki.org/home/convert/bash>

###
## I need to press Tab twice when trying to complete `$ tldr`! Why?

It's only necessary the first time you try to complete it in a new shell.
After that, pressing Tab once is enough.
I think the  first time you press  Tab, the completion fails,  but zsh sources
the completion function, which is why it works the second time.

### Is there a fix?

Yes, source the function from your zshrc:

     . ~/.zsh/my-completions/_tldr

#### Why don't you use it?

Starting a shell would take more time, because it runs an external process:

    $ tldr 2>/dev/null --list

##
# ?

Read `From  bash to  zsh` chapters  10, 15, and  maybe 13  (to learn  more about
autoloadable functions).

# ?

select-prompt

If this  is set for  the default  tag, its value  will be displayed  during menu
selection (see the  menu style above) when  the completion list does  not fit on
the screen as a whole.
The same  escapes as for the  list-prompt style are understood,  except that the
numbers refer to the match or line the mark is on.
A default prompt is used when the value is the empty string.

# ?

list-prompt

If this style is set for the default tag, completion lists that don't fit on the
screen  can be  scrolled  (see the  description of  the  zsh/complist module  in
zshmodules(1)).
The value, if not the empty string,  will be displayed after every screenful and
the shell will prompt for a key press;  if the style is set to the empty string,
a default prompt will be used.

The value may contain the escape sequences: `%l` or `%L`, which will be replaced
by the number of the last line displayed  and the total number of lines; `%m` or
`%M`, the number  of the last match  shown and the total number  of matches; and
`%p` and `%P`, `Top` when at the beginning of the list, `Bottom` when at the end
and the position shown as a percentage of the total length otherwise.
In each case the form with the uppercase  letter will be replaced by a string of
fixed width, padded to  the right with spaces, while the  lowercase form will be
replaced by a variable width string.
As in other  prompt strings, the escape sequences `%S`,  `%s`, `%B`, `%b`, `%U`,
`%u` for  entering and leaving the  display modes standout, bold  and underline,
and `%F`,  `%f`, `%K`, `%k` for  changing the foreground background  colour, are
also available,  as is the form  `%{...%}` for enclosing escape  sequences which
display with zero (or, with a numeric argument, some other) width.

After  deleting this  prompt the  variable LISTPROMPT  should be  unset for  the
removal to take effect.

# ?

        list-colors

If  the zsh/complist  module is  loaded, this  style can  be used  to set  color
specifications.
This mechanism  replaces the  use of the  ZLS_COLORS and  ZLS_COLOURS parameters
described in  the section  `The zsh/complist Module`  in zshmodules(1),  but the
syntax is the same.

If this style is set for the default  tag, the strings in the value are taken as
specifications that are to be used everywhere.
If it is set for other tags, the specifications are used only for matches of the
type described by the tag.
For this to work best, the group-name style must be set to an empty string.

In addition  to setting  styles for specific  tags, it is  also possible  to use
group  names  specified explicitly  by  the  group-name  tag together  with  the
`(group)` syntax allowed by the ZLS_COLORS and ZLS_COLOURS parameters and simply
using the default tag.

It  is possible  to use  any color  specifications already  set up  for the  GNU
version of the ls command:

        zstyle ':completion:*:default' list-colors \
             ${(s.:.)LS_COLORS}

The default colors are the same as for the GNU ls command and can be obtained by
setting the style to an empty string (i.e. '').

# ?

group-name

The completion  system can  group different  types of  matches, which  appear in
separate lists.
This style can be used to give the names of groups for particular tags.
For  example, in  command  position  the completion  system  generates names  of
builtin and external commands, names  of aliases, shell functions and parameters
and reserved words as possible completions.
To have the external commands and shell functions listed separately:

        zstyle ':completion:*:*:-command-:*:commands' \
             group-name commands

        zstyle ':completion:*:*:-command-:*:functions' \
             group-name functions

As a  consequence, any match  with the  same tag will  be displayed in  the same
group.

If the name given  is the empty string the name of the  tag for the matches will
be used as the name of the group.
So, to  have all different types  of matches displayed separately,  one can just
set:

        zstyle ':completion:*' group-name ''

All matches  for which no  group name is  defined will be  put in a  group named
-default-.

# ?

format

If this style is set for the descriptions  tag, its value is used as a string to
display above matches in completion lists.
The sequence `%d`  in this string will  be replaced with a  short description of
what these matches are.
This  string  may  also  contain  the  following  sequences  to  specify  output
attributes  as  described  in  the  section EXPANSION  OF  PROMPT  SEQUENCES  in
zshmisc(1): `%B`, `%S`, `%U`,  `%F`, `%K` and their lower  case counterparts, as
well as `%{...%}`.
`%F`, `%K` and `%{...%}` take arguments in the same form as prompt expansion.
Note that the sequence `%G` is not available; an argument to `%{` should be used
instead.

The style is tested with each tag  valid for the current completion before it is
tested for the descriptions tag (see 'man zshcompsys' > 'standard tags').
Hence different format strings can be defined for different types of match.

Note also that some completer functions define additional `%`-sequences.
These are described for the completer functions that make use of them.

Some completion  functions display  messages that may  be customised  by setting
this style for the messages tag.
Here, the `%d` is replaced with a message given by the completion function.

Finally, the format string  is looked up with the warnings tag,  for use when no
matches could be generated at all.
In this  case the `%d`  is replaced with the  descriptions for the  matches that
were expected separated by spaces.
The sequence `%D` is replaced with the same descriptions separated by newlines.

# ?

        _complete_help (^Xh)

This widget  displays information  about the  context names,  the tags,  and the
completion functions used when completing at the current cursor position.
If given a  numeric argument other than  1 (as in `ESC-2 ^Xh`),  then the styles
used and the contexts for which they are used will be shown, too.

Note that  the information  about styles  may be incomplete;  it depends  on the
information available  from the  completion functions called,  which in  turn is
determined by the user's own styles and other settings.

---

        _complete_help_generic

Unlike other commands listed  here, this must be created as  a normal ZLE widget
rather than a completion widget (i.e. with zle -N).
It is used for generating help with a widget bound to the `_generic` widget that
is described above.

If this widget is  created using the name of the function, as  it is by default,
then when executed it will read a key sequence.
This is expected  to be bound to a  call to a completion function  that uses the
`_generic` widget.
That widget will  be executed, and information provided in  the same format that
the `_complete_help` widget displays for contextual completion.

If  the widget's  name contains  debug, for  example if  it is  created as  `zle
-N  _complete_debug_generic _complete_help_generic`,  it will  read and  execute
the  keystring for  a  generic widget  as before,  but  then generate  debugging
information as done by `_complete_debug` for contextual completion.

If the widget's name  contains noread, it will not read  a keystring but instead
arrange that the  next use of a generic  widget run in the same  shell will have
the effect as described above.

The widget works  by setting the shell  parameter ZSH_TRACE_GENERIC_WIDGET which
is read by `_generic`.
Unsetting the parameter cancels any pending effect of the noread form.

For example, after executing the following:

      zle -N _complete_debug_generic _complete_help_generic
      bindkey '^x:' _complete_debug_generic

typing `C-x  :` followed  by the key  sequence for a  generic widget  will cause
trace output for that widget to be saved to a file.

# ?

        file-patterns

This is used by the standard function for completing filenames, `_files`.
If the style is unset, up to three tags are offered:

        - globbed-files
        - directories
        - all-files

depending on the types of files expected by the caller of `_files`.
`globbed-files`  and `directories`  are  normally offered  together  to make  it
easier to complete files in sub-directories.

The file-patterns style provides alternatives to the default tags, which are not
used.
Its  value consists  of  elements of  the form  `pattern:tag`;  each string  may
contain any number of such specifications separated by spaces.

The pattern is used to generate filenames.
Any occurrence of the sequence `%p` is  replaced by any pattern(s) passed by the
function calling `_files`.
Colons  in  the   pattern  must  be  preceded  by  a   backslash  to  make  them
distinguishable from the colon before the tag.
If more  than one pattern  is needed, the patterns  can be given  inside braces,
separated by commas.

The tags  of all strings in  the value will be  offered by `_files` and  used when
looking up other styles.
Any tags  in the same  word will be  offered at the  same time and  before later
words.
If no `:tag` is given the `files` tag will be used.

The tag  may also  be followed by  an optional second  colon and  a description,
which will  be used for the  `%d` in the value  of the format style  (if that is
set) instead of the default description supplied by the completion function.
If the description given here contains itself  a `%d`, that is replaced with the
description supplied by the completion function.

For example, to  make the rm command  first complete only names  of object files
and then the names of all files if there is no matching object file:

        zstyle ':completion:*:*:rm:*:*' file-patterns \
          '*.o:object-files' '%p:all-files'

To alter  the default  behaviour of  file completion --  offer files  matching a
pattern and directories  on the first attempt,  then all files --  to offer only
matching files on the first attempt, then directories, and finally all files:

        zstyle ':completion:*' file-patterns \
          '%p:globbed-files' '*(-/):directories' '*:all-files'

This works  even where there is  no special pattern: `_files`  matches all files
using the pattern `*` at the first step and stops when it sees this pattern.
Note also  it will never try  a pattern more  than once for a  single completion
attempt.

During the  execution of  completion functions, the  EXTENDED_GLOB option  is in
effect,  so  the characters  `#`,  `~`  and `^`  have  special  meanings in  the
patterns.

# ?

I think that there are 2 kinds of tags ('man compsys' > 'standard tags'):

> Some of the following  are only used when looking up  particular styles and do
> not refer to a type of match.

There's a category of tags which seem to be applied to matches.
And another category which is only used to configure some settings...

Here are the 10 default standard tags which are not applied to matches:

## accounts

Used to look up the users-hosts style.

---

        users-hosts

The values of this style should be of the form `user@host` or `user:host`.
It is used for commands that need pairs of user- and hostnames.
These commands will complete usernames from this style (only), and will restrict
subsequent hostname  completion to  hosts paired  with that user  in one  of the
values of the style.

It is possible to group values for  sets of commands which allow a remote login,
such as rlogin and ssh, by using the my-accounts tag.
Similarly,  values for  sets of  commands which  usually refer  to the  accounts
of  other  people,  such as  talk  and  finger,  can  be grouped  by  using  the
other-accounts tag.
More ambivalent commands may use the accounts tag.

## descriptions

Used when looking up the value of  the format style to generate descriptions for
types of matches.

## messages

Used to look up the format style for messages.

## my-accounts

Used to look up the users-hosts style.

What's the difference with the 'accounts' style?

## other-accounts

Used to look up the users-hosts style.

What's the difference with the '[my-]accounts' style?

## paths

Used to look up the values of the expand, ambiguous and special-dirs styles.

---

        ambiguous

This applies when  completing non-final components of filename  paths, IOW those
with a trailing slash.
If it is  set, the cursor is  left after the first ambiguous  component, even if
menu completion is in use.
The style is always tested with the paths tag.

---

        expand

This style is used when completing strings consisting of multiple parts, such as
path names.

If one of its  values is the string `prefix`, the partially  typed word from the
line  will be  expanded as  far as  possible even  if trailing  parts cannot  be
completed.

If one of its values is the string `suffix`, matching names for components after
the first ambiguous one will also be added.
This means that the resulting string is the longest unambiguous string possible.
However, menu completion can be used to cycle through all matches.

---

        special-dirs

Normally, the completion code will not  produce the directory names `.` and `..`
as possible completions.
If this  style is  set to  `true`, it  will add  both `.`  and `..`  as possible
completions; if it is set to `..`, only `..` will be added.

The  following example  sets special-dirs  to `..`  when the  current prefix  is
empty, is a single `.`, or consists only of a path beginning with `../`.
Otherwise the value is `false`.

         zstyle -e ':completion:*' special-dirs \
            '[[ $PREFIX = (../)#(|.|..) ]] && reply=(..)'

## processes-names

Used to  look up the  command style when generating  the names of  processes for
killall.

---

        command

In many places, completion functions need  to call external commands to generate
the list of completions.
This style  can be  used to  override the command  that is  called in  some such
cases.
The elements  of the  value are  joined with  spaces to  form a  command-line to
execute.
The value can also start with a hyphen,  in which case the usual command will be
added to  the end;  this is most  useful for putting  `builtin` or  `command` in
front to make sure  the appropriate version of a command  is called, for example
to avoid calling a shell function with the same name as an external command.

As an example, the completion function for  process IDs uses this style with the
processes tag  to generate  the IDs  to complete  and the  list of  processes to
display (if the verbose style is `true`).
The list produced by the command should look like the output of the ps command.
The first line is not displayed, but is searched for the string `PID` (or `pid`)
to find the position of the process IDs in the following lines.
If the line does not contain `PID`, the first numbers in each of the other lines
are taken as the process IDs to complete.

Note that  the completion function generally  has to call the  specified command
for each attempt to generate the completion list.
Hence care should  be taken to specify  only commands that take a  short time to
run, and in particular to avoid any that may never terminate.

## urls

Used to look up the urls and local styles when completing URLs.

---

        urls

This is used together with the urls tag by functions completing URLs.

If the value  consists of more than one  string, or if the only  string does not
name a file or directory, the strings are used as the URLs to complete.

If the  value contains only one  string which is the  name of a normal  file the
URLs are taken from that file (where the URLs may be separated by white space or
newlines).

Finally,  if the  only string  in  the value  names a  directory, the  directory
hierarchy rooted at this directory gives the completions.
The top level directory should be the file access method, such as `http`, `ftp`,
`bookmark` and so on.
In many cases the next level of directories will be a filename.
The directory hierarchy can descend as deep as necessary.

For example:

         zstyle ':completion:*' urls ~/.urls
         mkdir -p ~/.urls/ftp/ftp.zsh.org/pub

allows completion of  all the components of the  URL ftp://ftp.zsh.org/pub after
suitable commands such as `netscape` or `lynx`.
Note, however, that access methods and files are completed separately, so if the
hosts style is set hosts can be completed without reference to the urls style.

See the  description in the function  `_urls` itself for more  information (e.g.
`more $^fpath/_urls(N)`).

## variant

Used by  `_pick_variant` to  look up  the command to  run when  determining what
program is installed for a particular command name.

---

       _pick_variant [ -b builtin-label ] [ -c command ] [ -r name ]
                     label=pattern ... label [ arg ... ]

This function is used to resolve situations where a single command name requires
more than one type  of handling, either because it has more  than one variant or
because there is a name clash between two different commands.

The command  to run is taken  from the first  element of the array  words unless
this is overridden by the option -c.
This command is run and its output is compared with a series of patterns.
Arguments to be passed to the command can  be specified at the end after all the
other arguments.
The patterns to  try in order are  given by the arguments  label=pattern; if the
output of  `command arg  ...` contains  pattern, then label  is selected  as the
label for the command variant.
If none of the patterns match, the  final command label is selected and status 1
is returned.

If  the `-b  builtin-label` is  given, the  command is  tested to  see if  it is
provided as a shell builtin, possibly autoloaded; if so, the label builtin-label
is selected as the label for the variant.

If the  `-r name` is given,  the label picked  is stored in the  parameter named
name.

The results are also cached in the _cmd_variant associative array indexed by the
name of the command run.

## warnings

Used to look up the format style for warnings.

# ?

        zstyle [ -L [ pattern [ style ] ] ]
        zstyle [ -e | - | -- ] pattern style string ...
        zstyle -d [ pattern [ style ... ] ]
        zstyle -g name [ pattern [ style ] ]
        zstyle -{a|b|s} context style name [ sep ]
        zstyle -{T|t} context style [ string ... ]
        zstyle -m context style pattern

This builtin command is used to define and lookup styles.
Styles are pairs of names and values,  where the values consist of any number of
strings.
They are stored  together with patterns and  lookup is done by  giving a string,
called the `context`, which is compared to the patterns.
The definition stored for the first matching pattern will be returned.

For ordering of  comparisons, patterns are searched from most  specific to least
specific, and  patterns that are equally  specific keep the order  in which they
were defined.
A pattern  is considered to  be more specific than  another if it  contains more
components  (substrings  separated  by  colons)  or  if  the  patterns  for  the
components are  more specific, where  simple strings  are considered to  be more
specific than patterns  and complex patterns are considered to  be more specific
than the pattern `*`.

The first form (without arguments) lists the definitions.
Styles are shown in alphabetic order and  patterns are shown in the order zstyle
will test them.

If the -L option is given, listing is done in the form of calls to zstyle.
The  optional first  argument is  a pattern  which will  be matched  against the
string  supplied as  the pattern  for  the context;  note that  this means,  for
example, `zstyle -L  ":completion:*"` will match any  supplied pattern beginning
`:completion:`,  not just  `":completion:*"`:  use  `":completion:\*"` to  match
that.
The  optional second  argument limits  the  output to  a specific  style (not  a
pattern).
-L is not compatible with any other options.

The other forms are the following:

        zstyle [ - | -- | -e ] pattern style string ...

Defines the given style for the pattern with the strings as the value.
If  the -e  option is  given,  the strings  will be  concatenated (separated  by
spaces) and  the resulting string will  be evaluated (in  the same way as  it is
done by the eval builtin command) when the style is looked up.
In this case the parameter `reply` must  be assigned to set the strings returned
after the evaluation.
Before evaluating the value, reply is unset,  and if it is still unset after the
evaluation, the style is treated as if it were not set.

       zstyle -d [ pattern [ style ... ] ]

Delete style definitions.
Without arguments  all definitions are  deleted, with a pattern  all definitions
for that pattern are deleted and if any styles are given, then only those styles
are deleted for the pattern.

       zstyle -g name [ pattern [ style ] ]

Retrieve a style definition.
The name is used as the name of an array in which the results are stored.
Without any further arguments, all patterns defined are returned.
With a pattern the styles defined for  that pattern are returned and with both a
pattern and a style, the value strings of that combination is returned.

The other forms can be used to look up or test patterns.

       zstyle -s context style name [ sep ]

The parameter name is set to the value of the style interpreted as a string.
If the value contains several strings they are concatenated with spaces (or with
the sep string if that is given) between them.

       zstyle -b context style name

The value is stored in name as a  boolean, i.e. as the string `yes` if the value
has only one string  and that string is equal to one of  `yes`, `true`, `on`, or
`1`.
If the value is  any other string or has more than one  string, the parameter is
set to `no`.

       zstyle -a context style name

The value is stored in name as an array.
If name is declared as an associative array, the first, third, etc.
strings are used as the keys and the other strings are used as the values.

       zstyle -t context style [ string ... ]
       zstyle -T context style [ string ... ]

Test the value of a style, i.e. the -t option only returns a status (sets $?).
Without any  string the return  status is  zero if the  style is defined  for at
least one matching pattern, has only one  string in its value, and that is equal
to one of `true`, `yes`, `on` or `1`.
If any strings are given  the status is zero if and only if  at least one of the
strings is equal to at least one of the strings in the value.
If the style is defined but doesn't match, the return status is 1.
If the style is not defined, the status is 2.

The -T option tests the values of the  style like -t, but it returns status zero
(rather than 2) if the style is not defined for any matching pattern.

       zstyle -m context style pattern

Match a value.
Returns status zero  if the pattern matches  at least one of the  strings in the
value.

# ?

COMPLETION SYSTEM CONFIGURATION

The fields are always in the order

        :completion:function:completer:command:argument:tag
                                                           ^
                                                           ✘ no colon at the end!

These have the following meaning:

· The command or a special -context-,  just as it appears following the #compdef
tag or the compdef function.
Completion functions  for commands  that have  sub-commands usually  modify this
field  to contain  the name  of the  command followed  by a  minus sign  and the
sub-command.
For example,  the completion  function for  the cvs command  sets this  field to
cvs-add when completing arguments to the add subcommand.

· The  argument; this  indicates which  command-line or  option argument  we are
completing.
For command arguments  this generally takes the form argument-n,  where n is the
number of the argument, and for arguments to options the form option-opt-n where
n is the number of the argument to option opt.
However, this  is only  the case  if the  command-line  is parsed  with standard
UNIX-style options and arguments, so many completions do not set this.

· The tag.
As described  previously, tags  are used  to discriminate  between the  types of
matches a completion function can generate in a certain context.
Any completion function  may use any tag name  it likes, but a list  of the more
common ones is given below.

The context  is gradually put together  as the functions are  executed, starting
with the main  entry point, which adds :completion: and  the function element if
necessary.
The completer then adds the completer element.
The contextual completion adds the command and argument options.
Finally, the tag is added when the types of completion are known.
For example, the context name

        :completion::complete:dvips:option-o-1:files

says that normal completion was attempted as the first argument to the option -o
of the command dvips:

        dvips -o ...

and the completion function will generate filenames.

Usually completion will be tried for all  possible tags in an order given by the
completion function.
However, this can be altered by using the tag-order style.
Completion is then restricted to the list of given tags in the given order.

The `_complete_help` bindable command shows  all the contexts and tags available
for completion at a particular point.
This provides an easy way of finding information for tag-order and other styles.
It is described in the section `Bindable Commands` below.

When looking up styles the completion  system uses full context names, including
the tag.
Looking up the value  of a style therefore consists of  two things: the context,
which is matched to the most specific (best fitting) style pattern, and the name
of the style itself, which must be matched exactly.
The following  examples demonstrate that  style patterns may be  loosely defined
for styles that apply broadly, or as  tightly defined as desired for styles that
apply in narrower circumstances.

For example,  many completion functions can  generate matches in a  simple and a
verbose form and use the verbose style to decide which form should be used.
To make all such functions use the verbose form, put

        zstyle ':completion:*' verbose yes

in a startup file (probably .zshrc).
This  gives  the  verbose style  the  value  yes  in  every context  inside  the
completion system, unless that context has a more specific definition.
It is best to avoid giving the context as `*` in case the style has some meaning
outside the completion system.

A more specific example of the use of the verbose style is by the completion for
the kill builtin.
If the style is set, the builtin lists full job texts and process command-lines;
otherwise it shows the bare job numbers and PIDs.
To turn the style off for this use only:

        zstyle ':completion:*:*:kill:*:*' verbose no

For even more control, the style can use one of the tags `jobs` or `processes`.
To turn off verbose display only for jobs:

        zstyle ':completion:*:*:kill:*:jobs' verbose no

The -e option  to zstyle even allows  completion function code to  appear as the
argument  to a  style;  this requires  some understanding  of  the internals  of
completion functions (see see zshcompwid(1))).
For example,

        zstyle -e ':completion:*' hosts 'reply=($myhosts)'

This forces the  value of the hosts  style to be read from  the variable myhosts
each time  a host name  is needed; this  is useful if  the value of  myhosts can
change dynamically.
For another useful example, see the  example in the description of the file-list
style below.
This form can be slow and should be avoided for commonly examined styles such as
menu and list-rows-first.

Note that  the order  in which  styles are  defined does  not matter;  the style
mechanism  uses the  most  specific possible  match for  a  particular style  to
determine the set of values.
More precisely, strings are preferred over patterns (for
example, `:completion::complete:::foo` is more specific than
`:completion::complete:::*`), and longer patterns are preferred over shorter
patterns.

A good rule of thumb is that  any completion style pattern that needs to include
more than one wildcard (`*`) and that does not end in a tag name, should include
all six colons (:), possibly surrounding additional wildcards.

Style  names like  those of  tags  are arbitrary  and depend  on the  completion
function.
However,  the following  two sections  list  some of  the most  common tags  and
styles.

##
##
##
# 10
## What is a “programmable completion”?

It's  a  definition (often  implemented  by  a  shell function)  that  describes
what the  shell should  do (completing  characters, correcting  typos, expanding
patterns) and how to do it when  the user press a key (typically Tab), depending
on the existing words on the command-line.

##
## How to attempt a completion on the text before the cursor, treating it as a file name?

Press `M-/`.

## As a command name?  Variable name?  Host name?  User name/named directory?

    M-!
    M-$
    M-@
    M-~

## Which kinds of command names does `M-!` consider?  In which order?

   1. aliases
   2. reserved words
   3. shell functions
   4. shell builtins
   5. executable filenames

---

If you wonder what's the difference between reserved words and shell builtins:
<https://unix.stackexchange.com/a/267886/289772>

A shell builtin is a command, but a reserved word (or keyword) is not a command.
A keyword can't be a command, because  it provides a construct which can include
a command, and there can be only one command per “simple command”.

    ┌ keyword
    │  ┌ command
    ├┐ ├─┐
    if \ls >/dev/null; then; echo 'the `ls` command succeeded!'; fi

##
## How to make the shell list command names? variable names? filenames? hostnames? usernames?

        C-x !
        C-x $
        C-x /
        C-x @
        C-x ~ 

---

Note that these widgets don't work by default in zsh:

        M-!    C-x !
        M-$    C-x $
        M-/    C-x /
        M-@    C-x @
        M-~    C-x ~ 

They work  only if you install  some custom key bindings  invoking the functions
`_bash_complete-word` and `_bash_list-choices`.

## What does `C-d` do in zsh?

It inspects the text before the cursor,  and lists matches according to the type
of the text (filename, variable name, hostname, ...).

If there's a  whitespace before the cursor, zsh inspects  the whole command-line
and the cursor position to list relevant matches.

Basically, you can view `C-d` as a way to get smart suggestions, like `Tab` is a
way to get smart completions.

Example:

    % echo C-d
    suggests filenames~

    % aptitude C-d
    suggests subcommands for `aptitude`~

## What's the equivalent in bash?

    Esc =

## What's the difference between `b C-x ~` and `~b C-d` in zsh?

`b C-x ~` lists only usernames beginning with 'b'.
`~b C-d` lists usernames AND named directories beginning with 'b'.

The difference may be due to the fact that, in zsh, `C-x ~` is a
re-implementation of a bash command, and that in bash the concept of named
directory doesn't seem to exist.

##
## How to insert the currently selected match in the completion menu, without closing the menu?

Press `C-o`.

Useful when you need to insert several matches in the menu.

## How to list subscript flags which can be used in (zsh) array indexing?

        % echo $fpath[( Tab

##
## How does readline decide from where to start completing the text before the cursor?

It  splits the  command-line into  chunks whenever  it finds  a whitespace  or a
character in `$COMP_WORDBREAKS`.
The default value of the latter is:

        "'@><=;|&(:

Then, it completes from the beginning of the chunk where the cursor is.

---

        $ COMP_WORDBREAKS='"'\''><=;|&('
        PATH=/bin:/usr/b Tab
        ∅~

Here,   no  match   is  suggested   because   we've  removed   the  colon   from
`COMP_WORDBREAKS`, which makes readline break the line up to the previous `=`.
But there's no file/directory whose path begins with `/bin:/usr/b`.

## How to prevent readline from starting a completion from a colon?

Escape it.

It won't have any  influence on the resulting command once  you press Enter, but
it will prevent readline from considering the colon as a word separator.

        $ PATH=/bin:/usr/b Tab
        /usr/bin~

        $ PATH=/bin\:/usr/b Tab
        ∅~

##
## zstyle
### Which arguments must I pass to the `zstyle` command?

        1. a style pattern
        2. a name
        3. a value

Example:

    zstyle ':completion:*' format '%F{123}%d%f'
           ├─────────────┘ ├────┘ ├───────────┘
           │               │      └ value
           │               └ name
           └ style pattern

### What's the purpose of a style?

It allows you to configure a mechanism, such as the completion.
In particular, a style can configure  how the matches are generated, similarly
to shell options but with much more control.

### Why can't I give a random name to my style?

A style can be seen as  a context-sensitive option, like a buffer-local option
in Vim.
The name you choose controls which aspect of the style you change.

You can't choose the names of your Vim options;
you can't choose the names of your zsh styles.

### Where can I find a list of valid style names?

    % man zshcompsys
      > COMPLETION SYSTEM CONFIGURATION
      > Standard Styles

###
### context
#### What's a context?

Everything that the shell knows about the  meaning of the command-line and the
significance of the cursor position.

#### What's a style pattern?

The first  argument passed to `zstyle`  which is matched against  a context to
determine whether the style should be applied.

#### Into which fields can a context be broken down?

        1. the system used, such as 'completion', 'filter-select', 'zle'
        2. a function
        3. a completer
        4. a command
        5. an argument
        6. a tag

####
#### In case of conflicting styles, which one wins?

The one whose pattern is the most specific.

If 2  styles have similar patterns  (i.e. same level of  specificity), the first
one which was defined wins.

#### When is a style pattern considered more specific than another one?

When it  contains more  fields or  if the  patterns inside  the fields  are more
specific.

#### How would those patterns be ordered, according to their specifity?:  `*foo*`, `*`, `some string`

        1. some string
        2. *foo*
        3. *

A simple string is considered to be  more specific than a pattern, and a complex
pattern is considered to be more specific than a simple one.

###
#### What's the function field in a context?

If the completion is called from a named widget rather than through the normal
completion system, it's the name of the function called by the widget.

Typically this is blank, but it is set by special widgets.
Often, the function name is written in an abbreviated form.

###
#### What's a completer?

It's the  function which  is in  overall control  of how  completion is  to be
performed.
'complete'  is the  simplest completer,  but others  exist to  perform related
tasks such as correction, or to modify the behaviour of a later completer.

#### Which text does the completer field of a context contain?

The name  of the  function which  generates the  matches, without  the leading
underscore and with other underscores converted to hyphens.

#### Where can I find a list of completers?

        % man zshcompsys
          > section `Control Functions`

##
##
##
# 15

completion = definition that describes what the shell should complete depending
             on the existing words on the command-line

matches = list of possibilities generated by the completion system in a given situation

completions in zsh are defined using shell functions.
bash followed  zsh's lead with  a shell  function–based system that  was clearly
inspired by zsh's.
There is quite  a lot you can  achieve without resorting to  writing whole shell
functions, however.
For example, in bash to complete hostnames after the telnet command (which makes
a network connection to another host) you can use:

        $ complete  -A hostname telnet
                    ├─────────┘
                    └ option specifying the 'hostname' action:
                      hostnames should be completed;
                      `-j` is a less readable alternative

In zsh, you would use:

        compdef _hosts telnet
                ├────┘
                └ zsh builtin function

Note If you see  a "command not found" error for compdef, you  will need to make
sure you first enable the new completion system.
See the section "zsh's compinit" in Chapter 10 for details on how to do this.
Also, make sure  that the directories containing zsh's  completion functions are
listed in the fpath variable.
In fact,  zsh also  has a  function named `_telnet`  that does  a better  job of
completing for telnet than merely completing hostnames.
It is common  to want to restrict  completion for a command to  certain types of
files.
In Chapter 10 we demonstrated how  completion after gunzip is restricted to only
those files it can uncompress.
Completions of this  kind are easy to  define and are powerful enough  to make a
difference.
For instance, you might want to restrict  completion to .jpg image files for the
gimp image editor.
In bash  you can specify that  like this:

        complete  -A file -X '!*.jpg'  gimp

In this  example we specify  that we want to  complete filenames using  the file
action and we  also specify a pattern  with the -X option to  indicate that some
matches should be excluded.
The pattern starts with an exclamation mark (!) because we want to exclude those
matches that don't match the pattern rather than those that do.
If you have more than one command  that uses the same completion definition, you
can list all of their names as  arguments to complete (the same applies to zsh's
compdef).
Typically you also want to specify a range of file types so the pattern needs to
be more complicated.
So  you might  use  the  following to  additionally  complete  arguments to  the
gimp-remote  command  and  to  match  .jpeg  and  .png  files:

        complete  -f  -X '!*.@(jp?(e)g|png)' gimp gimp-remote

Note that you will  need to have the extglob option turned on  in your setup for
this to work.
It is an  invaluable option when writing  completions because there is  a lot of
pattern matching.
In  this example,  we use  the -f  option to  specify that  we want  to complete
filenames.
This is the short form of -A file.
One  noteworthy aspect  of the  exclusion  pattern is  that it  also applies  to
directories.
It is, however, quite  common to want to use gimp to edit  an image file that is
in a subdirectory.
Starting with version 3 of bash, if you pass the option -o plusdirs to complete,
it will additionally complete directory names.
Let's now create a similar completion definition for zsh.
To achieve this, you already run into the need to write a shell function.
File completion is handled by a `_files` function.
This supports a -g option that allows  you to specify a glob pattern to restrict
completion to certain types of files.
In zsh 4.0, you can't specify these arguments with compdef.
1 It is still very simple, however:

        _gimp() {
          _files -g  '*.jpg(-.)'
        }
        compdef _gimp gimp

The (-.) at  the end of the pattern  is a glob qualifier (see  the section "Glob
Qualifiers in zsh" in Chapter 9).
This restricts the  files matched to regular files or  symbolic links to regular
files.
We  do this  because gimp  expects its  argument  to be  an image  file and  not
something like a directory.
`_files` can still complete directories, however.
In the section "Ordering with File Completion" later in this chapter we show how
the behavior of `_files` in this regard can be configured.
The functions that make up zsh's completion system are all autoloadable.
This has the advantage that functions are  only loaded into memory when they are
first called.
As  you may  recall from  the section  "Autoloadable Functions"  in Chapter  13,
autoloadable functions are each stored in a separate file and the shell searches
the directories listed in $fpath to find these files.
You don't need to use the autoload command to mark your completion functions for
autoloading;  when  compinit  runs,  it  looks for  functions  with  an  initial
underscore in their name and also at the first line of the file.
If the first line contains a special tag, it autoloads it.
So  for this  function, you  might create  a file  with the  following contents:
create  a   file  with   the  following  contents:

        #compdef  gimp
        _files  -g '*.jpg(-.)'

If this is placed in a directory  in your $fpath when compinit executes, it will
be picked up, marked for autoloading and defined for the gimp command.
Note that the function body doesn't need to be surrounded by `_gimp() { ... }`.

`__________ 1.`

In zsh 4.2, you can use `compdef '_files -g "*.jpg(-.)"' gimp`.
So  far in  this section,  you have  learned how  to replace,  for a  particular
command, the default filename completion.
In our example  for the gimp command,  this meant that the names  of image files
could be completed for each command argument.
However, many commands expect each argument to be something quite different.
A shell function allows programming logic to be used to make decisions.
From a  function, you  can therefore  find out which  command argument  is being
completed and act accordingly.
To demonstrate this ability, we'll write a function to handle completion for the
chown command.

