# Priority

matchup
outlaw
swapit
sandwich
ultisnips
tbone
dispatch
easy-align
fzf.vim
codi
apathy
projectionist
vimtex
autoformat

##
# Interesting plugins
## AdvancedSorters

The built-in `:sort` command is powerful, but it still is line-based.
It doesn't take  into account folded lines,  nor can it sort  entire blocks like
function definitions, paragraphs, etc.  But often, one needs to sort exactly such
areas as single entities, i.e. without changing the line order within them.
A workaround in Vim is condensing each  block into a single line, performing the
sorting, and then expanding again.
External, more powerful sort commands could be used, too.

This plugin implements this workaround and encapsulates the three separate steps
in one handy command.

While  `:sort`  has  several  flags  for  sorting  on  various  numbers,  and  a
/{pattern}/ can  be specified  to skip  or sort on,  it doesn't  allow arbitrary
(Vimscript) expressions.

This plugin offers extension commands that  evaluate an expression per line, put
that number  in front  of the  line, do a  numerical sort,  and then  remove the
temporary number again.
Specializations handle the common sort by number of characters and by the line's
display width.

<http://www.vim.org/scripts/script.php?script_id=4958> 260sloc

---

Simpler alternative (previous script has dependencies...):

<https://gist.github.com/PeterRincker/582ea9be24a69e6dd8e237eb877b8978>

## ALE    syntastic    neomake

ALE (Asynchronous Lint  Engine) is a plugin for providing  linting in NeoVim and
Vim 8 while you edit your text files.

ALE  makes use  of NeoVim  and Vim  8 job  control functions  and timers  to run
linters on the contents of text buffers  and return errors as text is changed in
Vim.
This allows  for displaying  warnings and  errors in files  being edited  in Vim
before files have been saved back to a filesystem.

In other words, this plugin lets you lint while you type.

<https://github.com/w0rp/ale> 8614 sloc

---

Alternatives:

- <https://github.com/scrooloose/syntastic>
- <https://github.com/neomake/neomake>

## alias

This  plugin lets  you define  command-line abbreviations  by :Alias  which only
expand at the beginning of the command prompt.

You can  pass the optional parameters  `-buffer` or `-range` to  create a buffer
local alias or one that accepts a range preceding the alias.

These command-line  abbreviations work  like the bash  aliases, except  that the
alias is substituted in-place.

<https://github.com/Konfekt/vim-alias> 156 sloc

## altscreen

Alternate screen setup for terminal Vim.

<https://github.com/fcpg/vim-altscreen> 28 sloc

The code can be boiled down to:

    augroup NoAltScreen
        au!
        au VimEnter * call s:altscreen(v:true)
        au VimLeave * call s:altscreen(v:false)
    augroup END

    fu s:altscreen(disable) abort
        if a:disable
            let [s:t_ti_save, s:t_te_save] = [&t_ti, &t_te]
            let &t_ti = substitute(&t_ti, '\e\[?1049h', '', '')
            let &t_te = substitute(&t_te, '\e\[?1049l', '', '')
        else
            if exists('s:t_te_save')
                let &t_te = s:t_te_save
                let &t_ti = s:t_ti_save
            endif
        endif
    endfu

## AnkiVim

Use vim (or your favorite editor) to write anki cards quickly in plain text or latex.

<https://github.com/MFreidank/AnkiVim>

## any-jump

IDE madness without overhead for 40+ languages

Vim code inspection plugin for finding defitinitions and references/usages.

Any-jump can  be used with any  language, but definitions search  only available
for supported languages.
This is not a problem in general, so use any-jump freely on any code project.

Based on syntax rules for 40 languages and fast regexp engines like ripgrep and ag.

<https://github.com/pechorin/any-jump.vim> 6074 sloc

## anywhere

Sometimes, you edit text outside of Vim.
These are sad times.
Enter vim-anywhere!

Once invoked, vim-anywhere will open a buffer.
Close  it and  its  contents are  copied  to your  clipboard  and your  previous
application is refocused.

<https://github.com/cknadler/vim-anywhere> 167 sloc

Alternative:

<https://github.com/hrantzsch/vimclip> 12 sloc

## apathy

Apathy sets the five path  searching options — 'path', 'suffixesadd', 'include',
'includeexpr', and 'define' — for file types I don't care about enough to bother
with creating a proper plugin.

<https://github.com/tpope/vim-apathy> 234 sloc

## argumentative

Argumentative aids with manipulating and moving between function arguments.

<https://github.com/PeterRincker/vim-argumentative> 312 sloc

Alternative:

<https://github.com/machakann/vim-swap> 2943 sloc

## async

Normalize async job control api for vim and neovim.

<https://github.com/prabirshrestha/async.vim> 243 sloc

## asyncrun

This plugin takes the  advantage of new apis in Vim 8 (and  NeoVim) to enable you to
run shell commands in background and read output in the quickfix window in realtime:

   - Easy to use, just start your background command by :AsyncRun
     Just like old '!' cmd.

   - Command is done in the background, no need to wait for the entire process to finish.

   - Output are displayed in the quickfix window, errors are matched with errorformat.

   - You can explore the error output immediately or keep working in vim while executing.

   - Ring the bell or play a sound to notify you job finished while you're focusing
     on editing.

   - Fast and lightweight, just a single self-contained asyncrun.vim source file.

   - Provide corresponding user experience in Vim, neovim, gvim and macvim.

<https://github.com/skywind3000/asyncrun.vim/> 1302 sloc

## asyncomplete

Provide async autocompletion for vim8 and neovim with timers.
This repository  is fork of  <https://github.com/roxma/nvim-complete-manager> in
pure vim script with python dependency removed.

asyncomplete.vim deliberately does not contain any sources.
Please use one of the following sources or create your own.

   - Buffer     via asyncomplete-buffer.vim
   - Vim Syntax via asyncomplete-necosyntax.vim
   - Vim        via asyncomplete-necovim.vim
   - UltiSnips  via asyncomplete-ultisnips.vim

<https://github.com/prabirshrestha/asyncomplete.vim> 353 sloc

## autoformat

Format code with one button press.

This  plugin makes  use  of external  formatting programs  to  achieve the  best
results.

Check the list  of formatprograms below to see which  languages are supported by
default.

You can easily customize these or add your own formatprogram.

When no  formatprogram exists (or no  formatprogram is installed) for  a certain
filetype, vim-autoformat falls  back by default to indenting,  (using vim's auto
indent functionality), retabbing and removing trailing whitespace.

<https://github.com/Chiel92/vim-autoformat> 538 sloc

## autoread

Use `tail -f` on a buffer and append new content.

This plugin uses Vim 8 async jobs to append new buffer content.

Internally, it works by running tail -f on a file and the output will be
appended to the buffer, which displays this buffer.

<https://github.com/chrisbra/vim-autoread> 145 sloc

---

Alternative relying on `inotifywait(1)` (provided by `inotify-tools` package):
```vim
vim9script
&autoread = true
command -bar AutoRead AutoRead()
def AutoRead()
  if !executable('inotifywait')
    echomsg 'missing dependency: inotifywait(1); https://man7.org/linux/man-pages/man1/inotifywait.1.html'
    return
  endif
  var cmd: string = 'inotifywait --monitor --event modify ' .. expand('%:p')
  job_start(cmd, {out_cb: function(AutoreadOutCb, [bufnr('%')])})
enddef
def AutoreadOutCb(buf: number, ..._)
  execute 'checktime ' .. buf
  win_execute(bufwinid(buf), 'normal! G')
enddef
```
## braceless

Text objects, folding, and more for Python and other indented languages.

<https://github.com/tweekmonster/braceless.vim> 2183 sloc

## browserlink

Live browser editing for Vim.

Browserlink lets  you live  edit CSS  files, which  are sent  to the  browser on
change, without reloading or changing the state of the page.

Browserlink lets you  evaluate buffers or selections of  JavaScript directly, or
even call  individual functions within the  buffer, for instant feedback  in the
browser.

<https://github.com/jaxbot/browserlink.vim/issues> 2904 sloc

## CamelCaseMotion

<https://github.com/bkad/CamelCaseMotion> 107 sloc

Ideas of mappings (make motion repeatable with ; ,):

   - `\w`    next       beginning of Word
   - `\b`    previous   "
   - `\e`    next       end of Word
   - `\ge`   previous   "

Adapt the plugin to support snake case also.
That  is  `\w`  should move  the  cursor  to  the  next uppercase  character  OR
underscore; same things for other mappings.

Alternative:
<https://github.com/chaoren/vim-wordmotion>

## clam

A lightweight Vim plugin for working with shell commands.

<https://github.com/sjl/clam.vim> 97 sloc

## codelf

(Neo)Vim plugin for searching useful variable names

<https://github.com/voldikss/vim-codelf> 252 sloc

## codi

The interactive scratchpad for hackers.

Codi is an interactive scratchpad for  hackers, with a similar interface to Numi
(<https://numi.io>).
It opens  a pane  synchronized to  your main buffer  which displays  the results
of  evaluating  each   line  as  you  type  (if  Vim   has  +job  and  +channel,
asynchronously!).
It's  extensible  to nearly  any  language  that  provides a  REPL  (interactive
interpreter)!

Note: without async support, evaluation  will trigger on cursor hold
rather than text change.

<https://github.com/metakirby5/codi.vim> 747 sloc

---

See also:

simple REPL inside vim

supports:  python,  php,  coffee,  mysql, mongodb,  redis,  sh,  go,
javascript, ruby, elixir ...

<https://github.com/zweifisch/pipe2eval> 407 sloc

And:
<https://github.com/krisajenkins/vim-pipe> 73 sloc

And:
<https://github.com/jalvesaq/vimcmdline> 799 sloc

## colorizer

A Vim plugin to colorize all text in the form #rrggbb or #rgb.

<https://github.com/lilydjwg/colorizer>:407 sloc

Alternative:
<https://github.com/RRethy/vim-hexokinase>:263 sloc

This plugin is interesting to study how to use signs in Vim.

## committia

A Vim plugin for more pleasant editing on commit messages

<https://github.com/rhysd/committia.vim> 336 sloc

## CompleteParameter

Complete parameter after select the completion.
Integration with YouCompleteMe(ycm), deoplete, neocomplete.

<https://github.com/tenfyzhong/CompleteParameter.vim> 1202 sloc

## complimentary

Complimentary  improves  the  completion   of  VimL  builtin  functions,
commands, variables and options.

<https://github.com/fcpg/vim-complimentary> 464 sloc (265 VimL + 199 awk)

## context

A Vim plugin that shows the context of the currently visible buffer contents.
It's supposed to work on a wide range of file types, but is probably most useful
when looking at source code files.
In most programming  languages this context will show you  which function you're
looking at, and  within that function which loops or  conditions are surrounding
the visible code.

<https://github.com/wellle/context.vim> 1068 sloc

## cosco

VIM colon and semicolon insertion bliss

<https://github.com/lfilho/cosco.vim> 450 sloc

## csv

- <https://github.com/chrisbra/csv.vim>
- <https://github.com/andmarti1424/sc-im>
- <https://csvkit.readthedocs.io/en/0.9.1/tutorial/1_getting_started.html>

## ctags    GNU global

Ctags is a programming tool that generates an index (or tag) file of names found
in source and header files of various programming languages.

2 flavors exist: exuberant ctags and universal ctags

Universal Ctags is a fork of  Exuberant Ctags, Universal-ctags has the objective
of continuing the development from Exuberant Ctags.

The goal of the project is  preparing and maintaining common/unified space where
people interested in making Ctags better can work together.

Universal will replace exuberant:

<https://github.com/universal-ctags/ctags/issues/446>

It's probably more actively maintained.

Blog post about exuberant:

<https://andrew.stwrt.ca/posts/vim-ctags/>

---

Linux source  code GNU GLOBAL is  a source code tagging  system that
works  the  same way  across  diverse  environments, such  as  Emacs
editor, Vi  editor, Less viewer,  Bash shell, various  web browsers,
etc.

<https://www.gnu.org/software/global/>

Is this a more powerful alternative to cscope ?

<https://github.com/OpenGrok/OpenGrok/wiki/Comparison-with-Similar-Tools>

Also, read `:h cscope`.

## ctrlsf

An ack.vim alternative mimics Ctrl-Shift-F on Sublime Text 2

Features

   - Search and display result in a user-friendly view with adjustable context.

   - Edit mode which is incredible useful when you are doing refactoring. (Inspired by vim-ags)

   - Preview mode for fast exploring.

   - View location results in a quickfix window.

   - Various options for customized search, view and edit.

<https://github.com/dyng/ctrlsf.vim> 1899 sloc

## dadbod

DB is a Vim plugin for interacting with databases.
It's a more modern take on dbext.vim, improving on it on the following ways:

   - Connections are specified with a single URL, rather than prompting you for
     14 separate variables

   - All interaction is through invoking :DB, not 53 different commands and 35
     different maps (omitting many of the more esoteric features, of course)

   - Supports a modern array of backends, including NoSQL databases:

       * MongoDB
       * MySQL
       * PostgreSQL
       * Redis
       * Sqlite
       * Your own easily implemented adapter

   - Easily configurable based on a project  directory (as seen in rails.vim,
     for example), rather than just globally or in a per-file modeline

<https://github.com/tpope/vim-dadbod> 1018 sloc

---

See also `vim-dadbod-ui`:

Simple UI for vim-dadbod.
It  allows simple  navigation through  databases and  allows saving  queries for
later use.

<https://github.com/kristijanhusak/vim-dadbod-ui> 311 sloc

## dasht

(Neo)Vim plugin for dasht integration

<https://github.com/sunaku/vim-dasht> 88 sloc

Alternative:

<https://github.com/kabbamine/zeavim.vim> 228 sloc

## debugger

- <https://github.com/idanarye/vim-vebugger>
- <https://github.com/joonty/vdebug>

## diffconflicts

<https://github.com/whiteinge/diffconflicts> 133 sloc

Read also: <https://medium.com/prodopsio/solving-git-merge-conflicts-with-vim-c8a8617e3633>

## diminactive

Vim plugin to dim inactive windows.

<https://github.com/blueyed/vim-diminactive> 419 sloc

## dirdiff

Vim plugin to diff all the files in two directories.

<https://github.com/will133/vim-dirdiff>:655 sloc

## dirvish-git

Git support for dirvish.vim

<https://github.com/kristijanhusak/vim-dirvish-git> 161 sloc

## doge

(Do)cumentation (Ge)nerator  (10+ languages) Generate proper  code documentation
skeletons with a single keypress.

<https://github.com/kkoomen/vim-doge> 2977 sloc

---

Even if we don't use this plugin,  it could be useful to implement some mappings
to ease the process of writing good documentation at the start of our functions.
We  should also  agree on  some convention;  e.g. always  write a  `Synopsis` or
`Signature` line, an `Input` and `Output` section, ...

---

Alternative:

<https://github.com/mg979/docgen.vim> 733 sloc

## echodoc

Displays function signatures from completions in the command-line.

<https://github.com/Shougo/echodoc.vim> 488 sloc

## editorconfig

EditorConfig  helps  developers define  and  maintain  consistent coding  styles
between different editors and IDEs.
The EditorConfig  project consists of a  file format for defining  coding styles
and a  collection of text  editor plugins that enable  editors to read  the file
format and adhere to defined styles.

- <https://github.com/editorconfig/editorconfig-vim> 446 sloc
- <http://editorconfig.org/>

---

Greg Hurrell doesn't like EditorConfig, because it requires you to put a file in
the project,  and you may not  be able to do  so if it's not  your project (e.g.
you're collaborating with others).

Instead, he uses a bit of Vimscript:
<https://www.youtube.com/watch?v=ifA8iw42vwI>

## editvar

Edits vim variable in buffer.

<https://github.com/thinca/vim-editvar> 209 cloc

## errormarker

Highlights and sets error markers for lines with compile errors.

<https://github.com/mh21/errormarker.vim> 118 sloc

## expand-region

vim-expand-region is  a Vim  plugin that lets  you visually  select increasingly
larger regions of text using the same key combination.

- <https://github.com/terryma/vim-expand-region> 226 sloc
- <https://github.com/landock/vim-expand-region> 231 sloc

## ferret

Enhanced multi-file search for Vim

Ferret improves Vim's multi-file search in four ways:

   1. Powerful multi-file search
   2. Streamlined multi-file replace
   3. Quickfix listing enhancements
   4. Easy operations on files in the quickfix listing

<https://github.com/wincent/ferret> 880 sloc

## fetch

<https://github.com/kopischke/vim-fetch> 218 sloc

vim-fetch enables  Vim to process  line and  column jump specifications  in file
paths as found in stack traces and similar output.
When  asked to  open such  a file,  in- or  outside Vim  or via  `gF`, Vim  with
vim-fetch will  jump to  the specified  line (and column,  if given)  instead of
displaying an empty, new file.

See also: <https://github.com/lervag/file-line> 41 sloc

## flattery

Flattery provides  targets for f/t searches,  either as a conveniency  [eg. fb searching
for ), as for text-objects] or creating new target types.

Ce plugin pourrait être utile pour se déplacer dans un mot utilisant la forme camelcase,
ou snakecase:

        fu:  jump to the next uppercase letter

        fw:  jump to the next alnum-word.
             Useful to move around in, for instance, snake-case identifiers
             like 'did_load_filetypes'

Il faudrait toutefois changer les raccourcis.
Peut-être  utiliser `C-g  f`  comme préfixe  au  lieu de  `f`.   Puis rendre  le
mouvement répétable.  Ou créer un sous-mode.

<https://github.com/fcpg/vim-flattery> 570 sloc

## floobits

Real-time collaborative editing.  Think Etherpad, but with native editors.

- <https://github.com/Floobits/floobits-vim> 113 sloc
- <https://floobits.com/>

## foldscript

Simple way to show some text ('transcript') in terminal recordings (eg. asciinema).

<https://github.com/fcpg/vim-foldscript> 83 sloc

## flygrep

Grep on the fly (and asynchronously).

<https://github.com/wsdjeg/FlyGrep.vim> 1056 sloc

## fzf    skim    picker

fuzzy-finder:

- <https://github.com/junegunn/fzf>
- <https://github.com/junegunn/fzf.vim>
- <https://github.com/lotabout/skim>
- <https://github.com/lotabout/skim.vim> 1141 sloc (readme is identical, but not the code)
- <https://github.com/srstevenson/vim-picker> 201 sloc

## git-diff

`auto-git-diff` is a vim plugin which shows git diff between each commit and its
parent commit below the commit list window of git rebase interactive.

When you  move a text-cursor  in `git-rebase-todo` file, `auto-git-diff`  gets a
commit hash of the line where the cursor exists and update the diff window.

<https://github.com/hotwatermorning/auto-git-diff> 103 sloc

## git-messenger.vim

Vim and Neovim plugin to reveal the commit messages under the cursor

<https://github.com/rhysd/git-messenger.vim> 1013 sloc

This plugin  would be  really useful  when you  are studying  the codebase  of a
foreign project.
Instead of relying on `$ git log` to  search when did a line of code appear, and
why, you could stay in Vim and  make the commit message – introducing the change
– be printed in a popup window.

---

Alternatively, use `:Gblame` and press O.

Or try one of these `:GB` commands:

    com -range GB echo systemlist(
        \ 'git -C ' .. expand('%:p:h')->shellescape() .. ' blame -L <line1>,<line2> ' .. expand('%')
        \ )->join("\n")

    com -range GB echo systemlist(
       \ 'git -C ' .. expand('%:p:h')->shellescape()
       \ .. ' blame -L <line1>,<line2> '
       \ .. expand('%')
       \ )->join("\n")
       \ ->substitute('^\([a-z0-9]\+\)[^)]\+\zs) .*$',
       \ '\=") " .. system("git log -1 --pretty=%s " .. submatch(1))',
       \ '')

Source: <https://www.reddit.com/r/vim/comments/dmi2qo/display_commit_message_for_line_in_file/f5168y8/>

## gitgutter    signify

A Vim plugin which shows a git diff in the 'gutter' (sign column).
It shows whether each  line has been added, modified, and  where lines have been
removed.

<https://github.com/airblade/vim-gitgutter>:1466 sloc

This article is interesting:
<https://jakobgm.com/posts/vim/git-integration/>

It  explains that  the plugin  installs key  bindings to  move between  modified
chunks in a file, which have changed the author workflow for the better.
In particular,  they claim that  their git history is  much more atomic,  and so
more useful, because each commit has a clearer purpose:

   > Almost all of my commits are now partial commits.
   > My git  history ends  up being  much more  atomic, each  commit having  a clear,
   > singular purpose.

   > I keep track of remaining work by navigating over remaining code chunks.
   > If I consider a chunk to be completed, I stage it and forget about it.
   > This lets me easily ignore finished code.

   > Staging occurs when my cursor is placed on top of the code to be staged.
   > That  way I  know  exactly what  code  goes into  the  staging area,  implicitly
   > enforcing a last-time quality check of the code.
   > No more git add -a or similar blunders  which result in bad code being pushed to
   > a remote repository.

   > All my  written content  must now  be version controlled  since this  plugin has
   > become such a crucial part of my mental model of editing text.
   > My work is therefore  mostly backed up to GitHub, while  giving me the necessary
   > tools to revert changes, and so on.

   > It is much easier to do “non-linear” experimentation.
   > What  I mean  with this  is that  it enables  you to  safely edit  some code  at
   > location A, then  make some permanent changes over at  B, and finally completely
   > reverse the first change at A without altering location B.
   > This detaches  your changes from  the concept of  time and rather  associates it
   > with source code location instead, which I think is much more useful as a mental
   > model for source code changes.

Although, beware, it could make Vim slow:
<https://www.reddit.com/r/vim/comments/bqtvk8/tightly_integrating_git_into_vim/eo88srq/>
In that case, try vim-signifiy instead.

Note that I think it shows how important it is to get better at git.
Are you sometimes concerned by the amount of comments in our code files?
Those comments should be inside commit messages.
And when you wonder why a line is  written like it is, you should use `:Gblame`,
then press `O` to read the commit message.

---

Signify (or just Sy) is a quite unobtrusive plugin.
It uses signs to indicate added, modified  and removed lines based on data of an
underlying version control system.

<https://github.com/mhinz/vim-signify>:1078 sloc

## gitv

Using  this plugin  you can  view a  repository's history  including
branching and merging, you can see which commits refs point to.
You can  quickly and  easily view  what changed  to which  files and
when.
You  can  perform  arbitrary  diffs   (using  Vim's  built  in  diff
functionality)  and  you can  easily  check  out whole  commits  and
branches or just individual files if need be.
Start the plugin  by running :Gitv in  Vim when viewing a  file in a
git repository.

<https://github.com/gregsexton/gitv> 1435 sloc

---

Alternative:

gitv is  nice.  But I needed  a faster, and possibly  simpler alternative that I  can use
with a project with thousands of commits.

<https://github.com/junegunn/gv.vim> 298 sloc


A lightweight and powerful git branch viewer for vim.

<https://github.com/rbong/vim-flog> 1787 sloc

## golden-ratio

When working  with many windows  at the same  time, each window has  a size that  is not
convenient for editing.

golden-ratio  helps  on this  issue  by  resizing automatically  the
windows you  are working  on to  the size  specified in  the "Golden
Ratio".
The window  that has the main  focus will have the  perfect size for
editing, while the  ones that are not being actively  edited will be
re-sized to a smaller  size that doesn't get in the  way, but at the
same time will be readable enough to know it's content.

<https://github.com/roman/golden-ratio> 135 sloc

## goyo    limelight

Distraction-free writing in Vim.
<https://github.com/junegunn/goyo.vim> 355 sloc

Hyperfocus-writing in Vim.
<https://github.com/junegunn/limelight.vim> 238 sloc

## gnupg

This script implements transparent editing of gpg encrypted files.
The filename must have a ".gpg", ".pgp" or ".asc" suffix.
When opening such a  file the content is decrypted, when opening  a new file the
script will ask for the recipients of the encrypted file.
The file content will be encrypted to all recipients before it is written.

- <https://github.com/jamessan/vim-gnupg> 793 sloc
- <http://www.vim.org/scripts/script.php?script_id=3645> (For a rudimentary documentation)

## grepper

This plugin makes searching in files easier than ever!

It supports many common grep tools (ag, ack, git grep, sift, pt, findstr and our
beloved BSD/GNU grep) out-of-the-box and it is easy to add new ones.
Grepper focuses on flexbility - there are many ways to use it

Using the prompt:  just insert the search query or  switch through the available
grep tools

Using the operator: search for the current visual selection or motion right away
or pre-fill the prompt with it

Using the pre-defined commands: all supported  tools come with their own command
for convenience; `:Ag 'foo bar' test/` does just what you would expect.

Build  your own  mappings commands:  for  maximum customization  simply use  the
:Grepper command.
It is fully configurable using flags  that take priority over options defined in
your vimrc.
Actually, all the default commands like :Ag etc. a built atop of :Grepper.

<https://github.com/mhinz/vim-grepper> 971 sloc

See also: <https://github.com/yegappan/grep/> 706 sloc

## gutentags

Gutentags is  a plugin  that takes care  of the much  needed management  of tags
files in Vim.

It will (re)generate tag files as you  work while staying completely out of your
way.

It will even do its best to keep those tag files out of your way too.

It has no dependencies and just works.

<https://github.com/ludovicchabant/vim-gutentags> 1081 sloc

See also:
<https://github.com/skywind3000/gutentags_plus>

Alternative:
<https://github.com/jsfaint/gen_tags.vim> 615 sloc

## haskellConcealPlus

This bundle provides extended Haskell Conceal feature for Vim.
The  feature is  used  to  display unicode  operators  in  Haskell code  without
changing the underlying file.

This package offers more (and, more importantly, configurable) features than the
baseline vim-haskellConceal bundle.
The  baseline bundle  has  numerous  forks, which  is  possible  to combine,  so
everyone  is welcome  to  share, improve  or contribute  new  notations to  this
Conceal Plus package.

<https://github.com/enomsg/vim-haskellConcealPlus>

S'inspirer de ce syntax plugin pour conceal davantage de bruit.
Il y a 2 fichiers pour 2 types de fichiers différents.
Chacun utilise environ 300 sloc.

## hier

Highlight quickfix errors and location list entries in buffer.

<https://github.com/jceb/vim-hier> 90 sloc

## indent-object

Vim plugin that defines a new text object representing lines of code at the same indent level.
Useful for python/vim scripts, etc.

<https://github.com/michaeljsmith/vim-indent-object> 141 sloc

## indentLine

A vim plugin to display the indention levels with thin vertical lines. (may be slow)

<https://github.com/Yggdroot/indentLine> 294 sloc


A Vim plugin for visually displaying indent levels in code. (may be faster)

<https://github.com/nathanaelkane/vim-indent-guides> 1034 sloc

## jdaddy

Check out these must have mappings for working with JSON in Vim:

   - aj provides a text  object for the outermost JSON object,
     array, string, number, or keyword.
   - gqaj "pretty  prints" (wraps/indents/sorts  keys/otherwise
     cleans  up) the JSON construct  under the cursor.
   - gwaj takes the JSON  object on the  clipboard and extends it
     into the JSON object under the cursor.

There  are  also  ij  variants that  target  innermost  rather  than
outermost JSON construct.

<https://github.com/tpope/vim-jdaddy> 246 sloc

## join

a better (hopefully) :Join command in vim

<https://github.com/sk1418/Join> 140 sloc

## kronos

A simple task and time manager for vim.

<https://github.com/soywod/kronos.vim/> 789 sloc

## live-latex-preview

A clone of Kevin Klement's vim-live-latex-preview

- <https://github.com/ying17zi/vim-live-latex-preview>
- <https://jlebl.wordpress.com/2011/01/13/vim-evince-and-forward-and-backward-latex-synctex-search/> 312 sloc

## lister

lister.vim is a collection of commands for manipulating and moving between lists.


                      Quickfix list and Location list

:Qgrep {pattern} will narrow  down the quickfix list to results  with a message matching
the given pattern. :Qgrep! {pattern} will narrow down the results to those whose message
does not match the given pattern.

Similarly, :Qfilter {pattern}  will narrow the quickfix list to  results with a filename
matching the given pattern (and :Qfilter! for the inverse).

For the location list, there are :Lgrep and :Lfilter commands.

The {pattern} argument is always a Vim-flavoured regex.


                               Argument list

:Agrep  [arguments]  runs :grep  [arguments]  on  the files  in  the  argument list.  If
provided, ! is passed directly to :grep.  This causes the quickfix list to be populated,
but Vim does not move to the first item.

:Afilter  {pattern}  narrows  the  argument  list to  those  with  a  filename  matching
{pattern}. :Afilter! does the same, but where filenames do not match a pattern.


                       Moving between types of lists

:Qargs populates the  argument list with a  unique set of files from  the quickfix list.
Similar for :Largs, but with the location list.

:Sargs will convert all of the windows in the current tab page into a local argument list.

<https://github.com/tommcdo/vim-lister> 89 sloc

## lookup

This plugin is meant for VimL programmers.
It knows how  to jump to the definitions of  script-local and autoload variables
or functions:

   - s:var
   - s:func()
   - <sid>func()
   - autoload#foo#var
   - autoload#foo#func()
   - 'autoload#foo#func'

<https://github.com/mhinz/vim-lookup> 114 sloc

## lsp

async language server protocol plugin for vim and neovim

- <https://github.com/prabirshrestha/vim-lsp> 1353 sloc
- <https://github.com/prabirshrestha/vim-lsp/wiki>

---

<https://github.com/iamcco/vim-language-server> 42998 sloc

---

<https://github.com/prabirshrestha/vim-lsp/wiki/Servers-Python>

A Python 2.7 and 3.4+ implementation of the Language Server Protocol.

---

<https://github.com/prabirshrestha/asyncomplete-lsp.vim>

LSP source for asyncomplete.vim and vim-lsp

Provide Language Server Protocol autocompletion source for asyncomplete.vim and vim-lsp.

Résumé (pas sûr; juste mon intuition):

- `asyncomplete.vim` et `vim-lsp` fournissent des frameworks pour compléter du code
- `asyncomplete-lsp.vim` fournit des candidats utilisables par ces frameworks
- `async.vim` est une dépendance à installer pour `vim-lsp`

---

<https://www.reddit.com/r/vim/comments/71nj1a/code_completion/dnc661o/>

Commentaire de l'auteur des précédents plugins:

   > asyncomplete.vim paired with vim-lsp.
   > Language Server Protocol  (LSP) provides more than  just autocompletion features
   > like go to definition, rename find symbols, format and so on.
   > Since it runs in a separate process using jobs, it doesn’t slow down vim.

---

Liens intéressants:

- <https://blog.logrocket.com/how-to-use-the-language-server-protocol-to-extending-a-client-764da0e7863c>
- <https://microsoft.github.io/language-server-protocol/overview>

## makejob

This is a plugin for folks  who think that Vim's quickfix feature is
great, but  who don't like how  calls to :make and  :grep freeze the
editor.  MakeJob  implements  asynchronous  versions of  the  builtin
commands in just over 150 lines of Vimscript.

<https://github.com/foxik/vim-makejob> 197 sloc

---

This plugin could be useful to learn how to implement our own custom
async solutions, because it's short.

See also:
<https://github.com/yegappan/asyncmake> 125 sloc

## makery

Do  you know  about Vim's  own :make  system? It's  great! You  can set  makeprg to  any
executable program, so you can use :make not  just to run make with a Makefile, but also
to run linters, build scripts, task runners, etc.

Vim will then  catch the results of :make into  a quickfix list, so you can  jump to any
errors, down to the correct filename, line, and column!

This plugin is designed to be a companion to :make.

<https://github.com/igemnace/vim-makery> 152 sloc

## mark

This plugin adds  mappings and a :Mark command  to highlight several
words in  different colors  simultaneously, similar to  the built-in
'hlsearch' highlighting of search results and the * star command.

For example,  when you are  browsing a  big program file,  you could
highlight multiple identifiers in parallel.

This will make it easier to trace the source code.

<https://github.com/inkarkat/vim-mark> 1263 sloc

---

Alternative:

Highlight on the fly.

`quickhl.vim` support highlight for:

   - manual keywords
   - tag in ctags generated file
   - automatically higlight word under cursor(<cword>)

<https://github.com/t9md/vim-quickhl> 518 sloc

## mathpix

Vim commands to use mathpix from your screen

This is useful if you work with  LaTeX; it lets you convert a picture containing
a diagram or an equation into LaTeX source code, and paste it in Vim.

<https://github.com/ekiim/vim-mathpix> 37 sloc

## markology  markbar

Vim mark visualization, navigation and management

<https://github.com/jeetsukumaran/vim-markology> 658 sloc

Alternative:

<https://github.com/Yilin-Yang/vim-markbar> 2679 sloc

## miniyank

killring-alike plugin for neovim with no default mappings

<https://github.com/bfredl/nvim-miniyank> 141 sloc

This is a neovim plugin, but we could implement it in Vim because `TextYankPost`
has been added in Vim:

<https://github.com/vim/vim/pull/2333#issuecomment-344177706>

The neovim plugin uses `msgpackparse()` and `msgpackdump()` which don't exist in Vim.
Maybe try `json_encode()` and `json_decode()`, or `js_encode()` and `js_decode()`.

## minisnip

Snippets plugin based on snipmate.vim.

<https://github.com/habamax/vim-minisnip/> 631 sloc

## neoformat

A (Neo)vim plugin for formatting code.

Neoformat uses a variety  of formatters for many filetypes.  Currently,  Neoformat will run a
formatter using the  current buffer data, and  on success it will update  the current buffer
with the  formatted text.  On a  formatter failure,  Neoformat will  try the  next formatter
defined for the filetype.

By using getbufline() to read from the current  buffer instead of file, Neoformat is able to
format your  buffer without  you having  to :w your  file first.  Also, by  using setline(),
marks, jumps, etc. are all maintained after formatting.

Neoformat supports both sending buffer data to formatters via stdin, and also writing buffer
data to /tmp/ for formatters to read that do not support input via stdin.

<https://github.com/sbdchd/neoformat> 1098 sloc

---

Alternative:

<https://github.com/prettier/vim-prettier> 418 sloc

## ninja-feet

While Vim has a  great number of wonderful text objects, and plugins  can add even more,
there is no general way to operate from the cursor to the beginning or end of those text
objects.

Well, now there is. ninja-feet.vim lets you do so by putting [ or ] between the operator
and the text object.  For example, d]i) deletes from the cursor to the end of the current
parenthetical term. c[ip changes from the cursor to the beginning of the paragraph.

You  can  also  jump into  Insert  mode  at  the  beginning  or  end of  a  text  object
(technically, any motion) with z[ and z].

<https://github.com/tommcdo/vim-ninja-feet/> 57 sloc

## one

Inspired by Derek Wyatt’s “One Vim ... just one” video, this rewrite of the mvim
script builds on  Vim’s +clientserver capability to better  manage remote server
sessions.

<https://github.com/reedes/vim-one> 259 sloc

Alternative:
<https://github.com/susam/vimer>

## opex

Opex  is a  simple plugin  that  defines two  custom  operators to  execute motions  (:h
motion.txt) with  builtin interpreters.  Execution  operator (opex-execute)  executes the
code  and displays  any output  in  the message  line.  Appending operator  (opex-append)
executes the code and appends any output as a comment below the code.

<https://github.com/gokcehan/vim-opex> 345 sloc

## outlaw

The wanted outliner!

<https://github.com/lifepillar/vim-outlaw> 219 sloc

---

Alternative:
<https://github.com/msuperdock/vim-foldout> 730 sloc

---

Also, study this:
<https://github.com/rlue/vim-getting-things-down/> 258 sloc

---

Also, read this:
<https://github.com/vim-voom/VOoM/blob/master/doc/voom.txt>

You can't study this code, it's written in python.
However, the features it provide could give us inspiration.

## pandoc

vim-pandoc  provides  facilities  to  integrate Vim  with  the  pandoc  document
converter  and work  with documents  written in  its markdown  variant (although
textile documents are also supported).

vim-pandoc's goals are:

   - to provide advanced integration with pandoc
   - a comfortable document writing environment
   - great configurability

<https://github.com/vim-pandoc/vim-pandoc> 3519 sloc

---

pandoc-syntax

Pandoc syntax module, to be used alongside vim-pandoc (or as standalone).

If you want to use vim-pandoc-syntax without vim-pandoc, you'll need to tell Vim
to load it for certain files.
Just add something like this to your vimrc:

    augroup pandoc_syntax
        au! BufNewFile,BufFilePre,BufRead *.md set filetype=markdown.pandoc
    augroup END

<https://github.com/vim-pandoc/vim-pandoc-syntax> 516 sloc

<http://pandoc.org/MANUAL.html#pandocs-markdown>

---

rmarkdown

<https://github.com/vim-pandoc/vim-rmarkdown> 221 sloc

## pear-tree

A  Vim  auto-pair  plugin   that  supports  multi-character  pairs,  intelligent
matching, and more.

Pear Tree  automatically pairs  parentheses, quotes, HTML  tags, and  many other
text items based on a simple-to-define set of rules.
It  also  provides pair-wise  deletion,  newline  expansion, and  other  typical
auto-pair   features  without   interfering  with   Vim's  undo   or  dot-repeat
functionality.

<https://github.com/tmsvg/pear-tree> 1307 sloc

## phonetics

A vim plugin for checking and listening to English phonetics.

<https://github.com/soywod/vim-phonetics> 84 sloc

## pythonsense

A Vim plugin that provides text objects and motions for Python classes, methods,
functions, and doc strings.

<https://github.com/jeetsukumaran/vim-pythonsense> 486 sloc

## preview

This plugin solves a series of  user experience problems in vim's preview window
and provide a handy way to preview tags, files and function signatures.

<https://github.com/skywind3000/vim-preview> 869 sloc

## qf

vim-qf—short for  vim-quickfix—is a small  collection of settings,  commands and
mappings put  together to  make working  with the  location/quickfix list/window
smoother.

<https://github.com/romainl/vim-qf> 556 sloc

Global features (available from any window)

   - quickfix buffers are hidden from :ls and buffer navigation

   - optional mappings for :cnext, :cprevious, :lnext, :lprevious that wrap around
     the beginning and end of the list

   - optional mapping for jumping to and from the location/quickfix window,
   - optional mappings for toggling location/quickfix windows

   - open the location/quickfix window automatically after :make, :grep, :lvimgrep and
     friends if there are valid locations/errors

   - quit Vim if the last window is a location/quickfix window
   - close the location window automatically when quitting parent window

Local features (available only in location/quickfix windows)

   - disable soft-wrapping
   - disable relative numbers
   - optional Ack.vim-inspired mappings
   - filter and restore the current list
   - perform commands on each line in the current list
   - perform commands on each file in the current list
   - jump to next group of entries belonging to same file (“file grouping“)
   - save and load named lists

## qf-layout

<https://github.com/MarcWeber/vim-addon-qf-layout> 108 sloc

## qf-resize

Automatically resize quickfix and location list windows.

It will resize location/quickfix windows based on the number of lines therein; e.g. with
a single list entry, why waste 10 lines (the default height)?!

With vim-test/dispatch-neovim etc., and on VimResized it will process all existing qf windows.

<https://github.com/blueyed/vim-qf_resize> 251 sloc

## `quickfixsigns_vim`

Mark quickfix & location list items with signs

<https://github.com/tomtom/quickfixsigns_vim> 1488sloc

## quickmenu

A nice customizable popup menu for vim

<https://github.com/skywind3000/quickmenu.vim> 510 sloc

## quick-scope

A Vim plugin that highlights which characters to target for f, F and family.
No mappings are needed.

<https://github.com/unblevable/quick-scope> 269 sloc

Met en surbrillance le  bon caractère à choisir pour se  déplacer sur chaque mot
de la ligne via `f{char}`.

## rainbow_parentheses.vim

- <https://github.com/kien/rainbow_parentheses.vim> 90 sloc
- <https://github.com/junegunn/rainbow_parentheses.vim> 189 sloc
- <https://github.com/bounceme/poppy.vim> 40 sloc

## rhubarb   merginal

If fugitive.vim is the Git, rhubarb.vim is the Hub.  Here's the full list of features:

Enables :Gbrowse from fugitive.vim to open GitHub URLs.

Sets up :Git to use hub if installed rather than git.

In  commit  messages,  GitHub  issues,  issue URLs,  and  collaborators  can  be
omni-completed (<C-X><C-O>, see :help compl-omni).
This makes  inserting those `Closes  #123` remarks slightly easier  than copying
and pasting from the browser.

<https://github.com/tpope/vim-rhubarb>:247 sloc

---

Fugitive extension to manage and merge Git branches

<https://github.com/idanarye/vim-merginal>:1201 sloc

## scratch

Unobtrusive scratch window

<https://github.com/mtth/scratch.vim> 181 sloc

## sideways

A Vim plugin to move function arguments (and other delimited-by-something items)
left and right.

<https://github.com/AndrewRadev/sideways.vim> 2108 sloc

## signature

vim-signature is a plugin to place, toggle and display marks.

Le plugin permet aussi de poser 10 types de marqueurs visuels en utilisant les symboles:

    ! @ # $ % ^ & * ( )

Contrairement aux marques, il semble qu'on puisse poser un même marqueur sur plusieurs
lignes différentes.

Par défaut, le plugin installe un certain nb de mappings.  Parmi eux,
4 posent pb, car ils changent des mappings par défaut:

    `]           se rend à la prochaine marque dans l'ordre alphabétique
                 par défaut, se rend sur le dernière caractère du dernier texte changé

    `[           se rend à la précédente marque dans l'ordre alphabétique
                 par défaut, se rend sur le 1er caractère du dernier texte changé

    ']           mappings similaires mais se rend sur le 1er caractère non whitespace
    '[           "

Heureusement, on peut modifier les  mappings installés par le plugin
via la variable g:SignatureMap qui contient le dico suivant:

    let g:SignatureMap = {
    \ 'Leader'             :  "m",
    \ 'PlaceNextMark'      :  "m,",
    \ 'ToggleMarkAtLine'   :  "m.",
    \ 'PurgeMarksAtLine'   :  "m-",
    \ 'DeleteMark'         :  "dm",
    \ 'PurgeMarks'         :  "m<Space>",
    \ 'PurgeMarkers'       :  "m<BS>",
    \ 'GotoNextLineAlpha'  :  "']",
    \ 'GotoPrevLineAlpha'  :  "'[",
    \ 'GotoNextSpotAlpha'  :  "`]",
    \ 'GotoPrevSpotAlpha'  :  "`[",
    \ 'GotoNextLineByPos'  :  "]'",
    \ 'GotoPrevLineByPos'  :  "['",
    \ 'GotoNextSpotByPos'  :  "]`",
    \ 'GotoPrevSpotByPos'  :  "[`",
    \ 'GotoNextMarker'     :  "]-",
    \ 'GotoPrevMarker'     :  "[-",
    \ 'GotoNextMarkerAny'  :  "]=",
    \ 'GotoPrevMarkerAny'  :  "[=",
    \ 'ListBufferMarks'    :  "m/",
    \ 'ListBufferMarkers'  :  "m?"
    \ }

<https://github.com/kshenoy/vim-signature> 766 sloc

## signjump

Jump to signs just like other object motions.
A feature that is oddly absent from Vim.

<https://github.com/ZeroKnight/vim-signjump> 153 sloc

## shortcut

L'avantage de ce  plugin par rapport à fzf.vim, semble  être de pouvoir chercher
dans une description de ce que fait le mapping.

Avec fzf.vim, on peut juste chercher dans le lhs et le rhs du mapping.

This plugin provides a discoverable shortcut  system for Vim that is inspired by
Spacemacs and powered by fzf.vim.

It displays a searchable menu of shortcuts when you pause partway while typing a
shortcut, say, because you forgot the rest of it or because you just want to see
the shortcut menu again to discover what else is available.

You can interactively filter  the menu by typing more shortcut  keys or parts of
shortcut descriptions shown in the menu.

<https://github.com/sunaku/vim-shortcut> 258 sloc

Alternatives:

- <https://github.com/hecal3/vim-leader-guide> 509 sloc
- <https://github.com/urbainvaes/vim-remembrall> 226 sloc
- <https://github.com/skywind3000/vim-quickui> 4273 sloc

## smartword

<https://github.com/kana/vim-smartword> 108 sloc

## smoothie

This (neo)vim plugin makes scrolling nice and smooth.
Find yourself completely lost every time you press Ctrl-D or Ctrl-F?
You might want to give vim-smoothie a try!

<https://github.com/psliwka/vim-smoothie> 121 sloc

## spellcheck

This plugin  populates the  quickfix-list with  all spelling  errors found  in a
buffer to give you that overview.
You can use  the built-in quickfix features to navigate  to the first occurrence
of a particular spell error.
You can  also manage  the spelling  errors (mark  as good  / bad  word, globally
replace with suggestion) directly from the quickfix window via the usual zg, zw,
z= etc. mappings.

<https://github.com/vim-scripts/SpellCheck> 378 sloc

## splitjoin

Switching between a single-line statement and a multi-line one.
Offers the following default keybindings, which can be customized:

   - `gS` to split a one-liner into multiple lines

   - `gJ` (with the cursor on the first line of a block) to join a block into
     a single-line statement

<https://github.com/AndrewRadev/splitjoin.vim> 5165 sloc

---

Alternative limited to function arguments, lists and dictionaries:
<https://github.com/FooSoft/vim-argwrap> 405 sloc

ArgWrap is an industrial strength argument wrapping and unwrapping extension for
the Vim text editor.
It can  be used for collapsing  and expanding everything from  function calls to
array and dictionary definitions.
All operations are  easily reversible and correctly preserve  the indentation of
the surrounding code.

## stable-windows

Keeps vim windows stable when layout changes.

It  really annoys  me when  opening  new windows  in vim  (especially using  the
quickfix or  location list) and  vim automatically adjusts  the text in  all the
windows so the cursor line is centered.

<https://github.com/gillyb/stable-windows> 114 sloc

## startify

This plugin provides a start screen for Vim and Neovim.

It provides  dynamically created  headers or  footers and  uses configurable
lists to show recently used or bookmarked files and persistent sessions.

All of this can be accessed in a simple to use menu that even allows to open
multiple entries at once.

Startify doesn't get in your way and works out-of-the-box, but provides many
options for fine-grained customization.

<https://github.com/mhinz/vim-startify> 1029 sloc

See also:
<http://vi.stackexchange.com/a/715/6960>

<https://github.com/hardcoreplayers/dashboard-nvim> 1080 sloc

## startuptime

Everybody knows  that 1ms could  mean the difference  between life and  death in
Vim.
This plugin breaks  down the output of  --startuptime so you can zero  in on the
scripts that are stealing dozens of your milliseconds each time Vim is started.
You won't even need to leave the comfort of Vim.

<https://github.com/tweekmonster/startuptime.vim> 303 sloc

## stay

vim-stay adds automated view session creation and restoration whenever editing a
buffer, across Vim sessions and window life cycles.

It  also alleviates  Vim's  tendency to  lose view  state  when cycling  through
buffers (via argdo, bufdo et al.).

It is smart about which buffers should be persisted and which should not, making
the procedure painless and invisible.

<https://github.com/kopischke/vim-stay> 283 sloc

## subversive

Subversive provides  two new operator  motions to make  it very easy  to perform
quick substitutions.
It contains no default  mappings and will have no effect until  you add your own
maps to it.

<https://github.com/svermeulen/vim-subversive> 234 sloc

## swapit

Permet d'alterner entre 2 à 10 mots-clés via C-a/C-x.
On peut définir sa  propre liste (sans doute locale à un buffer  ou à un type de
fichiers).

Exemple d'utilisation:  définir la  liste ['true',  'false'] et  positionner son
curseur sur la ligne:

    setting=tr|ue

... le pipe représentant le curseur, appuyer sur C-a produira la ligne:

    setting=false

Exemples de listes de mots-clés installées par défaut:

    ['yes','no']
    ['Yes','No']
    ['True','False']
    ['true','false']
    ['AND','OR']
    ['Hello World!','GoodBye Cruel World!' , 'See You Next Tuesday!']
    ['On','Off']
    ['on','off']
    ['ON','OFF']
    ['<','<=','==', '>=', '>' , '=~', '!=']
    ['bool', 'char','int','unsigned int', 'float','long', 'double']
    ['Sunday','Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday']

<https://github.com/mjbrownie/swapit> 310 sloc

Ideas for mappings:

   - `<s`, `>s` to cycle in a chain
   - `=s` to get a default value no matter where we are in the chain

---

Alternatives:

- <https://github.com/AndrewRadev/switch.vim> 1208 sloc
- <https://github.com/zef/vim-cycle> 159 sloc
- <https://github.com/bootleq/vim-cycle> 627 sloc

---

switch semble  + puissant mais nécessite  de bien connaître les  regex pour être
customisé.

Screencast consacré à switch:
<https://www.youtube.com/watch?v=zIOOLZJb87U>

---

Une alternative naïve consiste à utiliser `C-x C-t` et un fichier spécial de synonymes.

## swoop

Lets  you find  and  replace occurrences  in  many buffers  being  aware of  the
context.

You can edit  the swoopBuffer and the  changes you applied will be  save for all
corresponding files by saving the buffer.

Especially useful to refactor a name in multiple files and keep control on it...

<https://github.com/pelodelfuego/vim-swoop> 416 sloc

Alternative:

<https://github.com/Olical/vim-enmasse> 171 sloc

## SyntaxRange

Define a different filetype syntax on regions of a buffer.

<https://github.com/inkarkat/vim-SyntaxRange> 78 sloc

See also:
<https://www.reddit.com/r/vim/comments/2x5yav/markdown_with_fenced_code_blocks_is_great/>

## tagbar

Tagbar is  a Vim  plugin that provides  an easy  way to browse  the tags  of the
current file and get an overview of its structure.

It does this by creating a sidebar that displays the ctags-generated tags of the
current file, ordered by their scope.

This means that  for example methods in  C++ are displayed under  the class they
are defined in.

Tagbar is not a general-purpose tool for managing tags files.

It only  creates the  tags it  needs on-the-fly  in-memory without  creating any
files.

tags file management is provided by other plugins, like for example easytags.

<https://github.com/majutsushi/tagbar> 4788 sloc

## targets

Targets.vim is  a Vim  plugin that adds  various text objects  to give  you more
targets to operate on.

It expands  on the idea  of simple commands like  di' (delete inside  the single
quotes  around the  cursor) to  give you  more opportunities  to craft  powerful
commands that can be repeated reliably.

One major goal is to handle all corner cases correctly.

- <https://github.com/wellle/targets.vim> 1459 sloc
- <https://github.com/wellle/line-targets.vim> 34 sloc

## test    entr

A Vim wrapper for running tests on different granularities.

- <https://github.com/janko-m/vim-test> 2694 sloc
- <https://www.youtube.com/watch?v=ODzMN91AhXc>

---

<http://entrproject.org/>

## textobj-user

vim-textobj-user is a Vim plugin to create your own text objects without pain.

It is hard to create text objects, because there are many pitfalls to deal with.

This plugin  hides such details  and provides a  declarative way to  define text
objects.

You can use regular expressions to  define simple text objects, or use functions
to define complex ones.

<https://github.com/kana/vim-textobj-user> 558 sloc

---

A  vim plugin  providing  a single  text  object  (on iv  and  av) for  variable
segments.

A variable  segment is  defined to  be a substring  in any  identifier character
followed by  an underscore  ("snake case") or  a lowercase  identifier character
followed by an uppercase character ("camel case").

<https://github.com/Julian/vim-textobj-variable-segment> 62 sloc (après avoir viré t/ et bin/)

---

Defines text objects to target text after the designated characters.

<https://github.com/junegunn/vim-after-object> 93 sloc

## tig-explorer.vim

Vim plugin to use Tig as a git client.
Seamless switching between vim and Tig with opening in the same buffer.

<https://github.com/iberianpig/tig-explorer.vim> 248 sloc

## tiler

Tiling window manger for Vim

Features

   - multiple layouts
   - can increase or decrease master window count on the fly
   - support for popups e.g. nerdtree, tagbar, quickfix, etc
   - each tab has its own settings

<https://github.com/zhamlin/tiler.vim> 401 sloc

Alternatives:

- <https://github.com/mattboehm/vim-accordion> 335 sloc
- <https://github.com/paroxayte/vwm.vim> 538 sloc

## tmuxify    tbone    tmux-runner    vimux    slimux

From best to worst:

- <https://github.com/jebaum/vim-tmuxify  (seems very good for handling panes)> 252 sloc
- <https://github.com/tpope/vim-tbone> 338 sloc
- <https://github.com/christoomey/vim-tmux-runner> 437 sloc
- <https://github.com/benmills/vimux> 169 sloc

---

Celui-là je sais pas où le ranger:

<https://github.com/epeli/slimux> 487 sloc

---

See also:
<https://github.com/roxma/vim-tmux-clipboard>

I began a refactoring of this last one here:

    ~/Dropbox/vim_plugins/tmux_clipboard.vim

## tmux-complete

Vim plugin for insert mode completion of words in adjacent tmux panes

If you're using  Vim in tandem with  tmux you might be familiar  with this pesky
situation:

You're happily  editing your lovely  files in Vim, when  you notice you  need to
type a word that you can see in a different tmux pane right next to Vim.

This might be some secret key found in your REPL or the name of a failing test.

Usually the interesting text is too short to warrant switching panes
and going into tmux' copy mode, so you end typing it out again.

But fear no longer!

This plugin adds a completion function that  puts all words visible in your tmux
panes right under your fingertips.

Just enter insert  mode, start typing any  word you see and  press <C-X><c-u> to
the trigger user defined insert mode completion.

It also completes words that are scrolled off, hidden in background tmux windows
and even different tmux sessions.

And it even works from gvim or MacVim!

<https://github.com/wellle/tmux-complete.vim> 410 sloc

---

- <https://gist.github.com/blueyed/6856354>
- <https://github.com/Osse/dotfiles/blob/master/.zfunctions/tmux_complete>

         local -A panes
         panes=($(tmux list-panes -F '#{pane_index} #{pane_active}'))

         local -a words
         words=(${(f)"$(
             for pane active in ${(kv)panes}; do
                 if (( active )); then
                     tmux capture-pane -J -p -t $pane | sed '/^$/d' | head -n -1
                 else
                     tmux capture-pane -J -p -t $pane
                 fi
             done | grep -o '\<\w\+\>'
         )"})

         _wanted values expl 'words from visible tmux panes' compadd -a words
         bindkey -M menuselect '^T' menu-complete

<https://github.com/Osse/dotfiles/blob/master/.zfunctions/tmux_complete_path>

    local -A panes
    panes=($(tmux list-panes -F '#{pane_index} #{pane_active}'))

    local -a words
    words=(${(f)"$(
        for pane active in ${(kv)panes}; do
            tmux capture-pane -J -p -t $pane
        done | grep -o '~\?[[:alnum:]/._]\+'
    )"})

    local -a paths
    for w in $words; do
        w=${w#[ab]/}
        w=${w%/}
        if [[ -e $w ]] || [[ $w = '~/'* && -e "$HOME${w#\~}" ]]; then
                paths+=($w)
        fi
    done

    _wanted values expl 'paths from visible tmux panes' compadd -Q -a paths
    bindkey -M menuselect '^P' menu-complete

<https://github.com/Osse/dotfiles/blob/master/.zshrc>

    zstyle ':completion:tmux-complete:*' completer tmux_complete
    zstyle ':completion:tmux-complete:*' ignore-line current
    zstyle ':completion:tmux-complete:*' menu yes select
    zstyle ':completion:tmux-complete-path:*' completer tmux_complete_path
    zstyle ':completion:tmux-complete-path:*' ignore-line current
    zstyle ':completion:tmux-complete-path:*' menu yes select
    zle -C tmux-complete complete-word _generic
    zle -C tmux-complete-path complete-word _generic
    bindkey '^X^T' tmux-complete
    bindkey '^X^P' tmux-complete-path

## traces

This plugin will highlight patterns and ranges for Ex-commands.

<https://github.com/xtal8/traces.vim> 1018 sloc

## translate-shell.vim

Translate-shell.vim is a plugin for translating text without leaving Vim.
It provides a window that displays  the translate of word under cursor, selected
text or you can use "on fly" translation and translate inserted text.
Also, you can save your translate story to file and import it to Anki.

<https://github.com/echuraev/translate-shell.vim> 906 sloc

## twiggy

Git branch management for Vim

<https://github.com/sodapopcan/vim-twiggy> 1082 sloc

## vim-stream

vims - use vim commands for pipeline filtering in terminal

<https://github.com/MilesCranmer/vim-stream> 33 sloc

## vimdade

An  eye friendly  plugin that  fades your  inactive buffers  and preserves  your
syntax highlighting!

<https://github.com/TaDaa/vimade> 510 sloc

## vimagit    gita    tig    gina

Ease your git worflow within vim.

From a very  single vim buffer, you  can perform main git operations  in few key
press; to name a few:

   - Visualize all diffs in your git repository.
   - Stage file, hunks or even just parts of a hunk using a single key press.
   - Write or amend your commit message and commit in the same buffer.

<https://github.com/jreybert/vimagit> 2089 sloc

---

gita  is a  git  manipulation plugin  which  allow users  to  perform daily  git
operation within Vim's live session.

<https://github.com/lambdalisue/vim-gita> 15463 sloc (!!!)

---

Asynchronously control git repositories in Neovim/Vim 8

<https://github.com/lambdalisue/gina.vim> 14016 sloc (!!!)

---

Alternatively, we could open a terminal  buffer, and from there launch the `tig`
program:

<https://github.com/jonas/tig>

This idea comes from:

<https://medium.com/usevim/what-is-modern-vim-2591f6b1ec04>

   > Any command-line tool that you enjoy using alongside Vim can be used in Neovim’s
   > split terminal.
   > For example, if  you like using tig,  the text-mode Git interface,  then you can
   > open a panel that runs tig!
   > This instantly gives you the power of integrated Git, without waiting for Neovim
   > or a plugin author to add this functionality.
   > Again,  this  usage  is  similar  to   the  benefits  of  using  tmux  alongside
   > command-line Vim, but you might prefer the integrated approach because it adds a
   > modal layer for movement and yank/paste over tig.

Youtube video demo for tig:

<https://www.youtube.com/watch?v=udCXubFr5Yo>

Read also the man pages:
tig(1), tigrc(5), tigmanual(7)

Update:
You could also integrate tig in Vim:

<https://github.com/iberianpig/tig-explorer.vim> 229 sloc

## vimdoc

Helpfile generation for vim

<https://github.com/google/vimdoc> 1606 sloc

## vimspector

vimspector - A multi-language debugging system for Vim

- <https://github.com/puremourning/vimspector> 5016 sloc
- <https://puremourning.github.io/vimspector-web/>

## vint

Fast and Highly Extensible Vim script Language Lint implemented by Python.

<https://github.com/Kuniwak/vint/> 11349 sloc

## vis

Extended Visual Mode Commands, Substitutes, and Searches

- <http://vim.sourceforge.net/scripts/script.php?script_id=1195>
- <https://github.com/RobertAudi/vis.vim (mirror)> 475 sloc

## visual-split

Vim plugin to control splits with visual selections or text objects

- <https://github.com/wellle/visual-split.vim> 102 sloc
- <https://www.reddit.com/r/vim/comments/3x2fcu/visualsplitvim_plugin_to_control_splits_with/>

## vpager

Pipe input from Vims terminal directly back into Vim

- <https://github.com/chrisbra/vpager>
- <https://www.reddit.com/r/vim/comments/8hqang/github_chrisbravpager_pipe_input_from_vims/dympxc2/> 182 sloc

## which-key

vim-which-key is vim port of emacs-which-key that displays available keybindings
in popup.

<https://github.com/liuchengxu/vim-which-key> 606 sloc

## wildfire

Smart selection of the closest text object

<https://github.com/gcmt/wildfire.vim> 346 sloc

## wiki

A wiki plugin for Vim

- <https://github.com/lervag/wiki>
- <https://www.reddit.com/r/vim/comments/8hz8bd/some_questions_regarding_note_taking_with_vim/dyow7db/>
- <https://www.youtube.com/watch?v=wh_WGWii7UE> 1995 sloc

## win

vim-win is a Vim plugin for managing windows.
Built-in functionality  includes window  selection, window buffer  swapping, and
window resizing.
The plugin  is extensible,  allowing additional functionality  to be  added (see
Configuration below).

<https://github.com/dstein64/vim-win> 362 sloc

---

It may be interesting to study this plugin because:

   - it's recent
   - it uses features such as popup / floating windows

## winresizer

very simple vim plugin for easy resizing of your vim windows

<https://github.com/simeji/winresizer/> 239 sloc

---

It could be useful and easier than what  we do currently, to create a submode in
which we can resize/move windows with `hjkl`, and move them.

## xrange

X-range is  a plugin allowing to  execute source code within  text documents. It
can run  part of  a buffer,  process it  through an  external shell  command and
inject the result somewhere else in the buffer. It attempts to be an alternative
to Emacs org-babel.

The main use cases are:

   - to store local macros in a buffer. Such macros can for example, launch
     tests, and modify the buffer itself, to generate and keep up to date
     a table of content

   - to use a vim buffer as a REPL by evaluting code in different languages and
     collecting the results in the same buffer. This is sometimes called
     reproductible research' as is in Emacs org-babel or Jupyter Notebook

<https://github.com/maxigit/vim-xrange> 789 sloc

## yadi

Yet Another Detect Indent.

<https://github.com/timakro/vim-yadi> 63 sloc

##
# Abolish

    ┌─────────────────────┬──────────────────────────────────────────────────┐
    │ FooBar   →  fooBar  │ crc         coerce to camelCase                  │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ foo_bar  →  FooBar  │ crm         "         MixedCase                  │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ fooBar   →  foo_bar │ crs         "         snake_case                 │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ FooBar   →  FOO_BAR │ cru         "         UPPER_CASE                 │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ FooBar   →  foo bar │ cr space    "         space case    irréversible │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ FooBar   →  foo-bar │ crk         "         kebab-case    "            │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ FooBar   →  foo.bar │ cr.         "         dot.case      "            │
    ├─────────────────────┼──────────────────────────────────────────────────┤
    │ xv       →  ✔       │ crg         "         glyph         "            │
    └─────────────────────┴──────────────────────────────────────────────────┘

Les coercitions  space case, kebab-case  et dot.case sont irréversibles  à moins
d'ajouter temporairement  l'espace, le tiret et  le point à la  valeur locale de
'isk'.

La coercition  `crg` est également irréversible,  et elle n'est pas  fournie par
Abolish mais indirectement par Unicode.vim.
Ce dernier fournit un opérateur que j'ai remap à `crg`.
On peut  aussi l'utiliser  sur une  ligne pour y  convertir tous  les digraphes:
`crgg`.

See also:

<https://github.com/arthurxavierx/vim-caser>

Could be useful for this reason:

<https://www.reddit.com/r/vim/comments/9dyu5w/vimcaser_easily_change_word_casing_with_motions/e5l6s0m/>

   > Yes, that  was the inspiration,  and some  part of the  code is based  on that
   > plugin.
   > The problem with it is that it  doesn't allow for coercion of text with motions,
   > text objects or visual mode.
   > That makes it impossible  to, for instance, press crc in  front of a kebab-cased
   > word and have it become camelCased.

Idea:

use `crs` to coerce  the current word in snake case, and  `crS` for the operator
coercing a text-object in snake case.
Do the same with `crc` and `crC`, `crm` and `crM`, ...

##
# Dirvish

    g?

            Affiche l'aide des mappings.


    -                            :Dirvish %
    <Plug>(dirvish_up)
    <Plug>(dirvish_split_up)
    <Plug>(dirvish_vsplit_up)

            Ouvre le dossier parent du fichier courant dans:

                    - la fenêtre courante
                    - un split horizontal
                    - un "     vertical

            Fonctionnent peu importe le type du buffer, Dirvish ou non.
            Ce sont les seuls mapping globaux.
            Les autres sont exclusivement locaux aux buffers Dirvish.

            Par défaut, `-` tape `<Plug>(dirvish_up)`.
            Ils acceptent un count.  Pex:

                    3-    ouvre le dossier arrière-grand parent du fichier courant


    q
    <Plug>(dirvish_quit)

            Quitter Dirvish et revenir au fichier d'origine (celui depuis lequel on a ouvert Dirvish).

            Par défaut, `q` tape `<Plug>(dirvish_quit)`.
            On peut utiliser ce dernier pour customiser la fermeture d'un buffer Dirvish.


    R    :Dirvish %

            Recharger le buffer Dirvish.

            Pratique si on a modifié le buffer (écriture, suppression…) et qu'on veut restaurer
            son contenu.
            Peut aussi servir à mettre à jour son contenu, si un fichier / dossier a été créé
            par un pgm externe, depuis son chargement initial.


    l (custom)    i    CR    double-clic gauche

            charge le fichier sous le curseur dans la fenêtre courante


    o    C-w f
    a    C-w f C-w L     résultats similaires mais pas identiques
    t    C-w gf
    p

            Charge le fichier sous le curseur dans:

                    - un split horizontal
                    - "        vertical
                    - un onglet
                    - la fenêtre précédente (la dernière ayant eu le focus)

            Avec `o`, `a`, et `t` le focus reste dans la fenêtre Dirvish.
            Avec tous les autres, le focus passe dans la nouvelle fenêtre ouverte.

            Mnémotechnique:

            On peut faire un parallèle entre la direction vers laquelle s'ouvre un split horizontal
            créé via `C-w s`, et celle vers laquelle s'ouvre une nouvelle ligne via `o`.
            Toujours vers le bas.

            Idem entre la direction vers laquelle s'ouvre un split vertical créé via `C-w v`, et celle
            vers laquelle se déplace le curseur qd on passe en mode insertion via `a`.
            Toujours vers la droite.


    {Visual} I    {Visual} CR
    {Visual} O
    {Visual} A

            Charge les fichiers sélectionnés visuellement:

                    - en tache de fond; seul le dernier est affiché dans la fenêtre courante
                    - dans des splits horizontaux
                    - dans des "        verticaux


    :cd %

            configure le dossier de travail comme étant le dossier affiché par Dirvish

            Fonctionne car `%` est développé automatiquement par Vim en le nom du buffer courant,
            et le nom d'un buffer Dirvish est le chemin littéral vers le dossier affiché.


    :edit %foo.txt

            crée le fichier `foo.txt` dans le dossier affiché par Dirvish


    :5,10call dirvish#open('tabedit', 0)

            ouvre les fichiers présents entre les lignes 5 et 10, chacun dans un onglet

            dirvish#open() est une fonction publique de Dirvish.

            Elle attend 2 arguments, dont les valeurs peuvent être:

                    - cmd    'edit', 'split', 'vsplit', 'tabedit'
                    - bg     0, 1                                Mnémotechnique = background

            Si:
                    bg = 0           les buffers sont toujours chargés et affichés dans une fenêtre
                                     le focus passe dans la fenêtre du dernier buffer affiché

                    bg  = 1          les buffers sont chargés mais pas affichés
                    cmd = 'edit'

                    bg   = 1         les buffers sont chargés et affichés            malgré  `bg = 1`
                    cmd != 'edit'    MAIS le focus reste dans la fenêtre courante    grâce à `bg = 1`


                                               FIXME:

            Passage à revoir, il semble que `bg` contrôle le focus et rien d'autre.
            Il n'y a pas (ou plus ?) de buffers chargés sans être affichés.


    :Dirvish
    :Dirvish %
    :Dirvish {path}

            Ouvre Dirvish au niveau du:

                    - dossier de travail

                    - dossier parent du fichier courant

                    - dossier parent de {path}, si {path} est un fichier
                      ou
                      {path} lui même,          si {path} est un dossier


    x

            Peuple la ligne de commande avec:

                    :Shdo  {}

            Fonctionne en mode normal et visuel.


    :12,34Shdo {cmd}

            Génère un script shell où {cmd} est appliquée à chaque fichier dont le chemin
            est écrit sur une ligne dont l'adresse est comprise entre 12 et 34.

            À chaque fois que {cmd} doit se référer à un fichier, il faut utiliser le placeholder {}.


    :'<,'>Shdo cp {} {}.bak
    :!%    OU    Z!

            Crée un script shell ayant pour but de faire backup de tous les fichiers sélectionnés
            visuellement, puis, sauvegarde et exécute le script shell.

            Après que la commande shell ait été exécutée:

                    - avec `:!%`, on reste dans le buffer shell.

                    - avec `Z!`, on retourne dans le buffer Dirvish.

            Si on pense qu'on aura besoin d'exécuter une commande shell similaire à celle qu'on va exécuter,
            on utilisera plutôt `:!%`, autrement `Z!`.


    ┌───────────┬──────────────────────────────────────────────────────────────────────┐
    │ dax       │ supprime le contenu de l'arglist locale à la fenêtre courante        │
    ├───────────┼──────────────────────────────────────────────────────────────────────┤
    │ x         │ ajoute le fichier sous le curseur ou la sélection visuelle           │
    │           │ à l'arglist locale                                                   │
    ├───────────┼──────────────────────────────────────────────────────────────────────┤
    │ Shdo! cmd │ exécute la commande shell `cmd` sur les fichiers de l'arglist locale │
    └───────────┴──────────────────────────────────────────────────────────────────────┘

            On remarque que le bang après `Shdo` détermine sur quels fichiers elle agit.

            Sang bang: ceux dont les chemins sont écrits dans le buffer dirvish, sur des lignes dont
                       l'adresse est au sein de la rangée passée à `Shdo`

            Avec bang: l'arglist


     X
    !X
    !.

            TODO:
            à documenter


    git ls-files | vim +'setf dirvish' -

            Depuis le shell, liste les fichiers du repo git où on se trouve, et charge cette liste
            dans un buffer Vim en lui donnant le type de fichier `dirvish`.

            Permet ensuite d'utiliser `Shdo` pour exécuter une transformation shell arbitraire sur
            un sous-ensemble des fichiers.

##
# Fzf.vim

    let g:fzf_action = {
    \                    'ctrl-t': 'tab split',
    \                    'ctrl-s': 'split',
    \                    'ctrl-v': 'vsplit',
    \                  }

            Définit ’C-s’, ’C-v’ et ’C-t’ comme raccourcis permettant d'ouvrir le résultat sélectionné
            dans resp. un split horizontal, vertical, ou onglet.

            Par défaut, `fzf.vim` utilise ’C-x’ à la place de ’C-s’ sans doute pour éviter de geler
            le terminal.

            On peut ajouter au dico n'importe quel couple 'key': 'Ex command'.
            Pex:    'ctrl-a': 'argedit'
            Bien que ’C-a’ soit déjà utilisé par readline.


    let g:fzf_buffers_jump = 1

            Qd on utilise `:[Fzf]Buffers`, et qu'on sélectionne et valide un buffer qui est déjà
            affiché dans une fenêtre, donner le focus à cette dernière, plutôt que de charger
            le buffer dans la fenêtre courante.


    let g:fzf_command_prefix = 'Fzf'

            Ajoute le préfixe `Fzf` devant tous les noms de commandes fournies par le plugin.

            Permet d'éviter qu'une commande du plugin n'en écrase une préexistante.
            Pex, par défaut, les plugins `fzf.vim` et `pathogen.vim` installent la même commande:

                    :Helptags

            En ajoutant `:Fzf` à la commande de `fzf.vim`, on obtient:

                    :FzfHelptags

            … et on préserve la commande de pathogen.vim.


    let g:fzf_files_options =
        \ '--preview "(coderay {} || cat {}) 2> /dev/null | head -'.&lines.'"'

            `g:fzf_files_options` permet d'ajouter automatiquement une option arbitraire à `:Files`.

            Ici, l'option ajoutée permet de prévisualiser le contenu du résultat sélectionné via
            le pgm `coderay`:

                    https://github.com/rubychan/coderay

            Ce dernier peut être installé via la commande:

                    $ gem install coderay


    let g:fzf_layout = { 'down': '~40%' }

            Position et dimension du pane tmux où s'affiche fzf.

            Si Vim tourne en dehors de tmux, fzf s'affichera dans le terminal entier.
            S'il tourne à l'intérieur d'une session tmux, alors il n'occupera qu'un pane,
            dont on peut contrôler la position et la taille via `g:fzf_layout`.

            La dimension s'exprime selon un pourcentage de la hauteur ou largeur du terminal.
            La position peut être:

                    - down
                    - up
                    - left
                    - right


    :Ag          [PATTERN]
    :BLines      [QUERY]
    :Lines       [QUERY]

            Cherche resp. dans:

                    - le contenu des fichiers du working directory
                    - les lignes du buffer courant
                    - les lignes des buffers de la buffer list

                                               NOTE:

            Quelle différence entre `:Ag` et `:Grep` ?

                    :Ag      installée par fzf.vim
                    :Grep    "             vimrc

            `:Ag` traite le pattern qu'on lui passe différemment.
            Pex:

                    :Grep foobarbaz    :    cherche ’foobarbaz’ exactement
                    :Ag   foobarbaz    :    cherche toute ligne contenant qch ressemblant vaguement
                                            à ’foobarbaz’ (fuzzy search)

            De plus, par défaut, `:Grep` peuple la qfl avec les résultats.
            Mais `:Ag` ne peuple la qfl qu'avec les résultats qu'on a marqué (via Tab ou M-a).


    :Buffers
    :Files       [PATH]
    :Locate      PATTERN

            Cherche resp. dans:

                    - les noms des buffers
                    - "            fichiers du working directory
                    - "            "        de la bdd de `locate(1)`


    :BCommits
    :Commits
    :GFiles      [OPTS]
    :GFiles?

            Cherche resp. dans:

                    - les commits ayant modifié le fichier courant (1)
                    - les commits du working directory (2)
                    - les noms des fichiers du repo (2)
                    - les noms des fichiers du repo ayant été changés depuis le dernier commit (2)

            (1) Ne fonctionne que si le fichier est versionné
            (2) "                    le working directory est à l'intérieur d'un repo Git

                                               NOTE:

            `:GFiles` équivaut à:

                    $ cd repo_root; git ls-files
                        OU
                    $ git ls-files $(git rev-parse --show-toplevel)

            `:GFiles?` équivaut à:

                    $ git status

            Les flags ’A’ et ’M’ devant les noms de fichiers signifient que ces derniers
            contiennent des changements resp. à commit, ou non indexés:

                    - changes to be committed
                    - changes not staged for commit

                                               NOTE:

            Pour les commits, fzf cherche spécifiquement dans 3 choses:

                    - la fin du sha1
                    - le message
                    - la date


            GFiles [OPTS]   | Git files (git ls-files)
            GFiles?         | Git files (git status)


    :History
    :History:
    :History/

            Cherche resp. dans:

                    - l'historique des fichiers récemment ouverts (v:oldfiles) + les buffers
                    - "                commandes Ex
                    - "                recherches

            J'ai remap les 2 dernières à C-R C-R, et la 1ère à SPC fr.


    :BTags       [QUERY]
    :Helptags
    :Tags        [QUERY]

            Cherche resp. dans:

                    - les tags du buffer courant
                    - "        de l'aide
                    - "        du projet

            Le fichier de tags du projet correspond à la 1e entrée de `tagfiles()`.
            Cette dernière correspond au développement de &tags.


    :Colors
    :Commands
    :Filetypes
    :Marks
    :Maps
    :Snippets
    :Windows

            Cherche resp. dans:

                    - les color schemes
                    - les commandes Vim
                    - les types de fichiers
                    - les marques (globales + locales)
                    - les mappings en mode normal
                    - les tab triggers des snippets contenant le texte devant le curseur
                    - les fenêtres


    :FzfFiles!

            Identique à `:FzfFiles`, à ceci près que le bang ouvre fzf en plein écran,
            au lieu d'un simple pane tmux.
            Le bang a le même effet pour toutes les commandes fzf.vim.


    :fbl
    :fc
    :fl
    :fs

            Abréviations en mode ligne de commande, développées en:

                    :FzfBLines
                    :FzfCommands
                    :FzfLines
                    :FzfLocate

            J'ai préféré associer ces commandes à des abréviations plutôt qu'à des mappings.

            Le but de `:FzfCommands` est d'insérer le nom d'une commande sur la ligne de commandes.
            Dans ce contexte, un mapping normal aurait peu de sens.

            `:FzfLocate` attend un argument obligatoire (PATTERN).
            `:FzfBLines` et `:FzfLines` attendent un argument optionnel (QUERY).
            Des mappings ne permettraient pas de les fournir.  Une abréviation est + flexible.


    Tab    S-Tab

            Marque le résultat sélectionné et sélectionne le résultat suivant / précédent.
            Répéter ces raccourcis sur une même résultat a pour effet de toggle la marque.

    C-s    C-v    C-t

            Afficher le résultat sélectionné dans un split horizontal, split vertical, ou un onglet.

            Ces raccourcis ne fonctionnent que pour les commandes qui ouvrent / chargent un fichier.

    M-a    M-d

            (Dé)Marque tous les résultats.


    <Plug>(fzf-maps-i)
    <Plug>(fzf-maps-x)
    <Plug>(fzf-maps-o)

            Plug mappings fonctionnant resp. en mode insertion, visuel et operator-pending.
            Ils permettent de chercher un mapping depuis les modes concernés.

            Ex d'utilisation:

                    imap <C-G>fm <Plug>(fzf-maps-i)
                    xmap <C-G>fm <Plug>(fzf-maps-x)
                    omap <C-G>fm <Plug>(fzf-maps-o)


    Custom mappings: | Mnemonics         |  Commands:
    ――――――――――――――――――――――――――――――――――――――――――――――――――
    SPC fa           |                   |  Ag
    "        bc      |                   |  BCommits
    "        bt      |                   |  BTags
    "        c       |                   |  Commits
    "        f       |                   |  Files
    "        gf      | Git Files         |  GFiles
    "        gc      | Git Changed files |  GFiles?
    "        ht      |                   |  Helptags
    "        l       | Buffer List       |  Buffers
    "        m       |                   |  Maps
    "        M       |                   |  Marks
    "        r       | Recently used     |  History
    "        s       |                   |  Snippets
    "        t       |                   |  Tags
    "        w       |                   |  Windows

##
# UltiSnips

## Configuration

    :echo has('python3')

            Tester si Vim a été compilé avec 3.x


    :py3 import sys; print(sys.version)

            Déterminer la version de l'interpréteur python 3.x contre laquelle Vim a été compilé.


UltiSnips permet de développer un tab trigger en snippet.


Qd UltiSnips doit développer un tab trigger et qu'il cherche le fichier dans lequel il est défini,
il regarde dans un certain nb de dossiers.

Ces derniers sont définis par les variables `g:UltiSnipsSnippetDir` et `g:UltiSnipsSnippetDirectories`.
Quelle différence entre les 2 ?

La 1e variable:

        - N'est pas définie par défaut

        - Attend comme valeur une chaîne contenant un chemin absolu vers un dossier.
          Le dernier composant du chemin ne doit pas être 'snippets'.
          En effet, qd UltiSnips entre dans un dossier portant le nom 'snippets', il considère
          que les fichiers qui s'y trouvent utilisent le format SnipMate (différent du format UltiSnips).

        - Est utile pour configurer le chemin vers notre dossier de snippets privé.
          Ex:

                let g:UltiSnipsSnippetDir = '~/.vim/UltiSnips/'

        - Est le 1er dossier dans lequel UltiSnips cherche le fichier de snippets à éditer
          qd on tape :USE


La 2e variable:

        - Vaut ['UltiSnips'] par défaut.

        - Attend comme valeur une liste de chemins relatifs ou absolus.
          Si le chemin est relatif, UltiSnips cherchera à compléter le chemin via tous les dossiers
          du &rtp.

        - Est utile pour pouvoir utiliser immédiatement des snippets tiers, tq:

                https://github.com/honza/vim-snippets

        - Si on lui affecte un seul élément correspondant à un chemin absolu, alors UltiSnips ne
          cherchera pas de snippets dans `&rtp` ce qui peut améliorer les performances.


À l'intérieur de  ces dossiers, le nom  d'un fichier de snippets  doit suivre un
certain schéma  parmi plusieurs possibles.   Tous dépendent du type  de fichiers
courant.  Pex, si le buffer courant est de type vim, UltiSnips cherchera dans un
fichier nommé:

        - vim.snippets

        - vim_foo.snippets
        - vim/foo
        - vim/foo.snippets

        - all.snippets
        - all/foo.snippets

UltiSnips considère `all` comme une sorte de type de fichiers universel.
`all.snippets` est utile pour définir des snippets indépendant du type de fichiers,
comme pex l'insertion d'une date.


    :UltiSnipsEdit
    :USE (custom)

            Édite le fichier de snippets correspondant au type de fichier du buffer courant.

            Dans un 1er temps, UltiSnips cherche dans le dossier `g:UltiSnipsSnippetDir`, puis
            s'il ne trouve rien, il cherche dans les dossiers `g:UltiSnipsSnippetDirectories`.


   :UltiSnipsAddFiletypes rails.ruby
                          │     │
                          │     └── … doit provoquer l'activation des snippets ruby
                          └── l'activation des snippets rails …

            Demande à ce que les snippets ruby soient chargés qd on édite un buffer rails.

            À taper dans un buffer rails, ou à écrire dans un filetype plugin rails.
            On pourrait également taper/écrire:

                    :UltiSnipsAddFiletypes ruby.programming

            L'ordre de priorité des snippets (en cas de conflit) serait alors:

                    rails > ruby > programming > all


    ┌────────────────────────────────┬───────────────────┬─────────────────┬─────────────────────────────────┐
    │ variable                       │ valeur par défaut │ valeur actuelle │ effet                           │
    ├────────────────────────────────┼───────────────────┼─────────────────┼─────────────────────────────────┤
    │ g:UltiSnipsExpandTrigger       │ Tab               │                 │ développer un tab trigger       │
    │                                │                   │                 │                                 │
    │ g:UltiSnipsListSnippets        │ C-Tab             │ C-g Tab         │ lister les snippets disponibles │
    │                                │                   │                 │                                 │
    │ g:UltiSnipsJumpForwardTrigger  │ C-j               │ S-F18           │ sauter vers le prochain tabstop │
    │                                │                   │                 │                                 │
    │ g:UltiSnipsJumpBackwardTrigger │ C-k               │ S-F19           │ "              précédent "      │
    └────────────────────────────────┴───────────────────┴─────────────────┴─────────────────────────────────┘


                                               NOTE:

            Il faut configurer ces variables avant l'appel de fin à une fonction du plugin manager.
            Pour vim-plug, il s'agit de la ligne:

                    call plug#end()


                                               NOTE:

            Les mappings de saut (C-j et C-k par défaut) ne sont installés que pendant le développement
            d'un snippet, et détruits immédiatement après pour ne pas interférer avec des mappings utilisateurs.


    UltiSnips#JumpForwards()
    UltiSnips#JumpBackwards()

    UltiSnips#ExpandSnippet()
    UltiSnips#ExpandSnippetOrJump()

            Il s'agit de 4 fonctions publics dont on peut se servir pour des configurations avancées.

            Les 2 premières fonctions servent à sauter vers le prochain / précédent tabstop.
            Les 2 dernières demandent le développement d'un tab trigger.


                                               NOTE:

            Quelle différence entre les 2 fonctions de développement ?

            ┌───────────────────────┬──────────────────────────────────────────────────────────┐
            │ ExpandSnippetOrJump() │ à utiliser si on a choisi la même touche pour développer │
            │                       │ et sauver vers l'avant:                                  │
            │                       │                                                          │
            │                       │ g:UltiSnipsExpandTrigger = g:UltiSnipsJumpForwardTrigger │
            ├───────────────────────┼──────────────────────────────────────────────────────────┤
            │ ExpandSnippet()       │ à utiliser si on a choisi des touches différentes        │
            └───────────────────────┴──────────────────────────────────────────────────────────┘


                                               NOTE:

            Si on a choisi la même touche pour développer et sauter vers l'avant, pex Tab,
            UltiSnips installe 2 mappings globaux:

                    i  <Tab>       * <C-R>=UltiSnips#ExpandSnippetOrJump()<cr>
                    s  <Tab>       * <Esc>:call UltiSnips#ExpandSnippetOrJump()<cr>

            … et 2 mappings locaux au buffer:

                    i  <S-Tab>     *@<C-R>=UltiSnips#JumpBackwards()<cr>
                    s  <S-Tab>     *@<Esc>:call UltiSnips#JumpBackwards()<cr>

            Les locaux sont installés dès qu'un tab trigger est développé, et supprimés dès que
            le développement est terminé (:h UltiSnips-triggers):

                    UltiSnips will only map the jump triggers while a snippet is
                    active to interfere as little as possible with other mappings.


                                               NOTE:

            Ces 4 fonctions produisent un code de retour chacun stocké dans une variable globale,
            dont la valeur code un succès ou un échec:

                    g:ulti_expand_res            0: fail, 1: success
                    g:ulti_expand_or_jump_res    0: fail, 1: expand, 2: jump
                    g:ulti_jump_forwards_res     0: fail, 1: success
                    g:ulti_jump_backwards_res    0: fail, 1: success

## Syntaxe basique

Dans un fichier où des snippets sont  définis, on peut faire commencer une ligne
par un mot-clé pour exécuter une directive.  Parmi ces mots-clés, on trouve:

            - extends
            - priority
            - clearsnippets
            - snippet
            - endsnippet

            - context
            - pre_expand
            - post_expand
            - post_jump


    extends perl, ruby

            UltiSnips active tous les snippets liés aux types de fichiers dont le nom suit.
            Pex ici:    perl, ruby

            On peut utiliser autant de directives `extends` qu'on veut, et les placer où on veut.


    priority 42

            Les snippets définis après cette ligne ont une priorité de 42.
            Sans cette directive, par défaut, les snippets ont une priorité de 0.

            En cas de conflit, càd si un tab trigger est utilisé dans 2 snippets différents,
            celui ayant la plus haute priorité gagne.


    snippet tab trigger "description" options

            Syntaxe de base pour déclarer un snippet.
            La description et les options sont optionnelles.


                                               NOTE:

            Si le tab trigger contient un espace, il faut l'encadrer avec un caractère qui n'apparaît
            pas en son sein, comme des guillemets.  Ex:

                    snippet "tab trigger"

            Si on veut en plus qu'il contienne des guillemets, on peut utiliser le point d'exclamation:

                    snippet !"tab trigger"!

            Qd plusieurs snippets ont le même tab trigger et la même priorité, UltiSnips affiche
            la liste des snippets possibles, chacun avec leur description.
            C'est à ce moment-là que la description est utile.  Elle permet à l'utilisateur de choisir
            le bon.

            Exception:
            En cas de conflit entre 2 snippets, l'un d'eux utilisant l'option `e` mais pas l'autre,
            celui qui utilise `e` a automatiquement la priorité.
            Ça permet de définir un snippet “fallback” qd la condition testée par l'expression
            du snippet utilisant `e` échoue.


                                               NOTE:

            Pour augmenter le niveau d'indentation d'une ligne au sein du snippet, il faut la préfixer
            avec un caractère littéral.  Qd le snippet sera développé, le caractère tab sera inséra
            littéralement ou remplacé par des espaces suivant la valeur de 'expandtab'.

            Dans un snippet, on peut voir le caractère tab comme l'appui sur la touche tab.


                                               NOTE:

            ┌────────┬──────────────────────────────────────────────────────────────────────┐
            │ option │ signification                                                        │
            ├────────┼──────────────────────────────────────────────────────────────────────┤
            │ b      │ beginning of line                                                    │
            │        │                                                                      │
            │        │ ne développer le tab trigger que s'il se trouve au début d'une ligne │
            ├────────┼──────────────────────────────────────────────────────────────────────┤
            │ e      │ expression                                                           │
            │        │                                                                      │
            │        │ le snippet n'est développé que si l'expression est vraie             │
            ├────────┼──────────────────────────────────────────────────────────────────────┤
            │ i      │ in-word                                                              │
            │        │                                                                      │
            │        │ autoriser le développement du snippet, même si le tab trigger        │
            │        │ est au milieu d'un mot                                               │
            │        │                                                                      │
            │        │ par défaut, un snippet n'est développé que si le tab trigger         │
            │        │ est en début de ligne ou précédé de whitespace                       │
            ├────────┼──────────────────────────────────────────────────────────────────────┤
            │ m      │ trim                                                                 │
            │        │                                                                      │
            │        │ les trailing whitespace de toutes les lignes du snippet              │
            ├────────┼──────────────────────────────────────────────────────────────────────┤
            │ r      │ regex                                                                │
            │        │                                                                      │
            │        │ interpréter le tab trigger comme une regex python                    │
            └────────┴──────────────────────────────────────────────────────────────────────┘

            Pour des infos concernant les options dispo:

                    :h UltiSnips-snippet-options


    snippet tab trigger
    \`texte entouré de backticks\`
    endsnippet

            Le caractère backtick ayant un sens spécial  pour UltiSnips, si on veut en insérer un
            littéralement dans un snippet, il faut l'échapper.


    snippet fmatter
    ---
    title: $1
    date: $2
    tags: $3
    ---
    $0
    endsnippet

            $1, $2, $3 et $0 correspondent à des tabstops.

            On peut naviguer entre les tabstops via les raccourcis définis par:

                    g:UltiSnipsJumpForwardTrigger
            et
                    g:UltiSnipsJumpBackwardTrigger

            Le tabstop $0 est spécial, car qd on arrive sur lui, UltiSnips considère que le développement
            du tab trigger et l'édition du snippet sont terminés.
            Déplacer le curseur en-dehors du snippet termine également son développement.

            Dès lors, on ne peut plus naviguer entre les autres tabstops.

            Tant qu'on reste au-sein du snippet, les raccourcis fonctionnent en mode insertion et sélection.


    title: ${1:my placeholder}

            On définit un placeholder pour le tabstop:

                    $1    →    ${1:my placeholder}

            Ici il s'agit d'une simple chaîne de caractères, mais on pourrait aussi utiliser:

                    - une interpolation d'une commande shell/VimL/python… entre des backticks.  Ex:

                            ${1:`date`}

                    - autre tabstop

            Qd notre curseur est positionné sur un tabstop doté d'un placeholder, ce dernier
            est sélectionné visuellement, et on se trouve en mode 'select'.
            Ainsi, n'importe quel caractère tapé remplace automatiquement le placeholder,
            et on peut continuer à insérer des caractères ensuite, car on est alors en mode 'insertion'.


    snippet a
    <a href="$1"${2: class="${3:link}"}>
        $0
    </a>
    endsnippet

            Le 2e placeholder:

                    class="…"

            … contient lui-même un tabstop:

                    ${3:link}

            Imbriquer 2 tabstops permet d'exprimer une relation de dépendance entre eux:
            l'un est une partie de l'autre.

            Ici, si  on supprime l'attribut,  la valeur est  automatiquement supprimée.  Ce  qui est
            souhaitable, car  on ne pourrait  pas avoir un attribut  (`class`) HTML sans  valeur, ni
            l'inverse, une valeur sans attribut.


                                               NOTE:

            Le placeholder `link` du 3e tabstop est important.
            Sans lui, si on supprime le 2e tabstop, le 3e n'est pas automatiquement supprimé.
            Plus généralement, un tabstop est automatiquement supprimé ssi:

                - il est inclus dans le placeholder d'un autre tabstop
                - il est suivi d'un texte qcq à l'intérieur du placeholder

                    snippet a
                    foo ${1:bar $2}($3)
                    endsnippet

                        a Tab
                        foo bar()˜
                            ├─┘˜
                            └ sélectionné˜

                        C-h
                        foo |()˜
                            ^
                            curseur˜

                        Tab
                        foo |()˜
                            ✘ le 2e tabstop n'a pas été automatiquement supprimé˜
                              raison pour laquelle le curseur reste sur place˜

                    snippet a
                    foo ${1:bar $2 baz}($3)
                    endsnippet

                        a Tab
                        foo bar()˜
                        foo bar  baz()˜
                            ├──────┘˜
                            └ sélectionné˜

                        C-h
                        foo |()˜
                            ^
                            curseur˜

                        Tab
                        foo (|)˜
                             ✔


    snippet date
    ${2:${1:`date +%d`}.`date +%m`}.`date +%Y`
    endsnippet

            Autre exemple, où un placeholder contient lui-même un tabstop.

            Décomposition de l'imbrication:

                    ${2:${1:`date +%d`}.`date +%m`}
                        │   │          │
                        │   │          └ ce n'est pas un opérateur de concaténation (juste un point)
                        │   └ début du placeholder du 1er tabstop:    `date +%d`
                        └ début du placeholder du 2e tabstop:         ${1:…}.`date +%m`

            Cette déclaration exprime que le jour dépend du mois.
            Ainsi, si on supprime le mois, le jour sera lui-aussi automatiquement supprimé.

            On aurait pu aussi écrire:

                    ${1:`date +%d`}.${2:`date +%m`}

            … mais dans ce cas, il n'y a plus de relations de dépendance.


    snippet "chap?t?e?r?" "Latex chapter" r
    chapter
    \section{chapter}
       $0
    \end{chapter}
    endsnippet

            Dans cet exemple, le tab trigger prend la forme d'une expression régulière python:

                    "chap?t?e?r?"

            Une  expression régulière  doit être  encadrée avec  des quotes,  ou n'importe  quel
            caractère absent de l'expression.

            Ici, elle équivaut à `\vcha%[pter]>`.
            On peut donc développer plusieurs tab triggers ayant un même préfixe en un même snippet.

            Si le snippet contient du code python, celui-ci peut accéder au texte matché par la regex
            via la variable locale `python`.


    snippet if "test" bm
    if ${1:condition}
        ${0:${VISUAL:MyCmd}}
    endif
    endsnippet

            Ce snippet permet d'entourer une commande Ex, avec un bloc `if`.

            Pour ce faire, il faut:

                    1. sélectionner la commande Ex

                    2. appuyer sur Tab pour qu'UltiSnips capture la sélection
                       et nous fasse passer en mode insertion

                    3. insérer `if` et ré-appuyer sur Tab pour développer ce snippet

            Le snippet utilise le placeholder spécial `${VISUAL}`.
            Ce dernier est donné en valeur par défaut au tabstop final 0.

            Il reçoit lui-même en valeur par défaut `MyCmd`.
            Ainsi qd on appuiera sur Tab, `${VISUAL}` sera développé en:

                    - `MyCmd` depuis le mode insertion
                    - la dernière sélection visuelle depuis le mode visuel


                                               NOTE:

            Sans valeur par défaut,  le placeholder fonctionne toujours même qd  on appuie sur Tab
            en mode insertion: il est alors développé en une chaîne vide.

            Les  accolades au  sein du  placeholder  sont obligatoires.  En  leur absence,  UltiSnips
            interpréterait `$VISUAL` comme une simple chaîne littérale.


                                               NOTE:

            Si on veut apporter une modification à la dernière sélection visuelle, il faut passer
            par une interpolation python, et utiliser `snip.v.text` au lieu de `${VISUAL}`.
            Par exemple, pour supprimer le 1er caractère `x` qu'elle contient, on écrira:

                    `!p snip.rv = snip.v.text.strip('x')`

## Substitution

On peut réinsérer automatiquement un tabstop où l'on veut, on parle de “mirroring“.
On peut également effectuer une substitution au sein du tabstop miroir.


    snippet fmatter
    ---
    title: ${1:my placeholder}
    ---
    # $1
    $0
    endsnippet

            Le 1er tabstop ($1) est répété 2 fois.
            Cela implique que lorsqu'on lui donne une valeur, le même texte est inséré automatiquement
            une 2e fois, là où se trouve sa 2e occurrence (ici:    `# $1`).

            On dit que le tabstop est “mirrored“ (reflété).


    snippet t "A simple HTML tag" bm
    <${1:div}>
    </${1/(\w+).*/$1/}>
    endsnippet

            On applique une transformation sur le miroir.
            Il s'agit de la substitution:    :s/(\w+).*/$1/

            Le  $1 au  sein de  la substitution  ne correspond  pas au  1er tabstop,  mais à  la 1e
            sous-expression capturée  dans le pattern  (\w+).  L'expression régulière  est gérée
            par python et non par Vim.


                                               NOTE:

            La chaîne  de remplacement peut  contenir des variables  `$i`, qui font  référence au
            sous-expressions  capturées dans  le pattern.  Ici, `$1`  fait référence  au 1er  mot
            capturé dans le 1er tabstop.

            `$0` est spéciale: elle fait référence à l'ensemble du match (équivaut à `&` ou `\0` dans Vim).


    snippet cond
    ${1:some_text}
    ${1/(a)|.*/(?1:foo:bar)/}
    endsnippet

            Le miroir subit une substitution conditionnelle, qui:

                    1. cherche et capture le pattern `a`:

                    2. pour le remplacer par:    (?1:foo:bar)

            Ça signifie que si le texte inséré dans  le tabstop d'origine commence par un `a`, il
            sera  remplacé  par `foo`  dans  le  miroir,  autrement  il sera  totalement  (`|.*`)
            remplacé par `bar`.


            Section de l'aide pertinente:  :h Ultisnips-replacement-string


                                               NOTE:

            Le token `?1` permet de tester si le groupe 1 a capturé qch ou pas.
            Le token `()` permet de demander à Ultisnips de traiter le remplacement comme
            une expression à évaluer.  Similaire à `\=` pour la commande `:s` dans Vim.


    ${1/(a)|(b)|.*/(?1:foo)(?2:bar)/}

            Ici, la substitution:

                    1. cherche le pattern:       (a)|(b)|.*
                       en capturant `a` ou `b` si le caractère est trouvé

                    2. pour le remplacer par:    (?1:foo)(?2:bar)

            Ce qui signifie que si le texte inséré dans le tabstop d'origine commence par un:

                    - `a`, le miroir commencera par `foo`
                    - `b`, "                        `bar`
                    - ni `a`, ni `b`, le miroir sera vide


                                               NOTE:

            On remarque au passage qu'il semble que python ajoute automatiquement l'ancre `^` au début
            du pattern.

                                               NOTE:

            On pourrait omettre  la dernière branche `|.*`; le code  fonctionnerait pratiquement à
            l'identique. À ceci près que le texte inséré dans le tabstop d'origine ne serait pas
            supprimé dans le miroir lorsqu'il ne commence pas par `a` ou `b`.


    ${1/(a)|(b)|.*/(?1:foo:bar)(?2:baz:qux)/}

            Si le texte inséré dans le tabstop d'origine commence par un:

                    - `a`, le miroir commencera par `fooqux`
                    - `b`, "                        `barbaz`
                    - ni `a`, ni `b`, le miroir commencera par `barqux`

            Illustre  qu'un miroir  peut  être aussi  intelligent qu'on  veut;  i.e. être  capable
            d'effectuer autant de substitutions que nécessaire, et choisir la bonne en fonction
            d'une caractéristique du tabstop d'origine.

## Interpolation

    `date`
    `!v strftime('%c')`
    `!p python code`

            Interpolation d'une commande shell ou d'une expression Vim.

            Les backticks encadrent la commande / expression interpolée.
            `!v` indique que ce qui suit est une expression Vim.
            `!p` "                           du code python.


    snippet wpm "average speed" b
    I typed ${1:750} words in ${2:30} minutes; my speed is `!p
    snip.rv = float(t[1]) / float(t[2])
    ` words per minute
    endsnippet

            Si on écrit un bloc de code python, après le `!p`, on peut chaque écrire chaque instruction
            sur une ligne dédiée, pour + de lisibilité.

            De plus, UltiSnips configure automatiquement certains objets et variables python, valables
            au sein du bloc de code:

                    - snip.rv    = variable 'return value'; sa valeur sera interpolée au sein du document

                    - t          = liste dont les éléments contiennent le texte inséré dans les
                                   différents tabstops; ex:    t[1] = $1, t[2] = $2

            Ici, `float()` est une fonction python, et non Vim.


                                               NOTE:

            Quelle différence entre `!p` et `#!/usr/bin/python`?
            Qd une interpolation débute par un shebang, la sortie du script est insérée dans le buffer.
            Mais `!p` est différent.  Avec `!p`, UltiSnips ignore la sortie de l'expression python qu'on
            écrit.  Il ne fait que l'évaluer.  Pour insérer sa sortie dans le buffer, il faut l'affecter
            à `snip.rv`.


                                               NOTE:

            Si on modifie la valeur d'un tabstop en mode normal via la commande `r`, l'interpolation
            est mise à jour. Ça peut donner l'impression de travailler avec un tableur (pgm manipulant
            des feuilles de calcul).

## Post-expand actions

                                               FIXME:

Lire:    :h UltiSnips-post-expand-actions

Comment écrire en VimL une action à exécuter juste après le développement d'un snippet?
La documentation ne semble parler que de code python.

Ce serait intéressant par exemple pour le snippet `op` dans un fichier Vim.
On pourrait alors s'assurer que les {rhs} des 3 mappings soient bien alignés au niveau du `:`.
On exécuterait qch comme `gaip:`

Lire:
How can I use several triggers for the same snippet?
<http://vi.stackexchange.com/a/10536/6960>

##
# Unicode.vim

Qd on parle de digraphe, on fait référence aux caractères à taper après C-k pour
produire un caractère spécial.  Par exemple, le digraphe de `✔` est `xv`.


    :UnicodeName
    :UnicodeName {register} {digraph|name|html|regex|value}

            Affiche les informations du caractère sous le curseur.
            Idem, mais en plus stocke une information le concernant dans le registre {register}.

            Par exemple si le curseur est placé sur le caractère `✔`, exécuter la commande:

                    :UnicodeName d digraph

            … stockera `xv` dans le registre `d`.

            De même:

                    - :UnicodeName n name   →  HEAVY CHECK MARK
                    - "            h html      &#x2714;
                    - "            r regex     \%u2714
                    - "            v value     10004


    :verb Digraphs!

            Affiche toutes les informations concernant les digraphes actuellement définis.

            Le bang est optionnel, il demande à afficher les info d'un digraphe sur une ligne dédiée.
            Autrement, une ligne contient les infos de plusieurs digraphes.
            Plus lisible.
            En outre, ça permet d'afficher le nom du digraphe.
            Chaque ligne suit la syntaxe suivante:

                    {glyph} {digraph}… {decimal code} ({name})

            Il peut y avoir plusieurs digraphes pour un même glyphe (d'où le …).

            Le modificateur `:verbose` n'est pas nécessaire, mais `:Digraphs` est lente, ça permet
            de voir où elle en est dans son traitement des digraphes.
            `:verb` remplit la même fonction qu'une barre de progression.

            Quel intérêt à `:Digraphs` par rapport à `:digraphs`?
            `:digraphs` est certes plus rapide, mais sa sortie est moins lisible.
            Les glyphes ne sont pas colorisés, on a donc plus de mal à les distinguer des digraphes.


    :Digraphs! copy

            Affiche tous les digraphes dont le nom unicode contient le mot 'copy'.
            La recherche est insensible à la casse.


    :UnicodeSearch pattern
    :UnicodeSearch 42
    :UnicodeSearch U+42

            Affiche tous les caractères dont:

                    - la valeur décimale est 42
                    - "         hexa     est 42
                    - le nom match pattern

            La recherche est insensible à la casse.

            Qd ils existent, les digraphes sont affichés entre parenthèses, séparés par des virgules.
            Les entités html sont également affichées.


    :UnicodeTable

            Ouvre une nouvelle fenêtre affichant la table des caractères unicodes.


    :UnicodeDownload


            Dl les données Unicode.  Utile si on veut mettre à jour la bdd locale.
            Elles sont téléchargées à partir d'une url, qu'on peut changer via une option:

                    :let g:Unicode_URL='http:....'


    C-x C-g

            Propose un caractère dont le digraphe contient les caractères devant le curseur.
            S'il n'y a qu'un seul match, le menu ne contiendra qu'une seule entrée.
            Appuyer sur Enter remplacera les caractères devant le curseur par l'entrée sélectionnée.


    C-x C-z

            En mode insertion, remplace les caractères devant le curseur par un caractère unicode
            dont le nom ou le code point contient ces derniers.
            Exemple d'utilisation:

                    math C-x C-z (pour insérer un symbole mathématique)

            On peut afficher toutes les infos le concernant (codepoint, nom, digraphe, glyphe)
            dans la fenêtre preview.  Pour ce faire, il faut activer une option:

                    let g:Unicode_ShowPreviewWindow = 1


    crg
    <Plug>(MakeDigraph)

            Mapping associé à un opérateur remplaçant tous les digraphes au sein d'un text-object
            par les caractères qu'ils génèrent.

            Mnémotechnique:    coerce to glyph

            Exemple d'utilisation:

                    foo => bar xv

                       crgg

                    foo ⇒ bar ✔


    let g:Unicode_ConvertDigraphSubset = [
                                         \ char2nr("€"),
                                         \ char2nr("ä"),
                                         \ char2nr("Ä"),
                                         \ char2nr("ö"),
                                         \ char2nr("Ö"),
                                         \ char2nr("ü"),
                                         \ char2nr("Ü"),
                                         \ char2nr("ß"),
                                         \ ]

            Limite la génération de digraphes à certains digraphes seulement.

            `g:Unicode_ConvertDigraphSubset` est une liste pouvant contenir des nbs décimaux.
            Seuls les digraphes des caractères dont la valeur décimale est à l'intérieur seront
            remplacés par l'opérateur `<Plug>(MakeDigraph)`.


    unicode#FindUnicodeBy({match})
    unicode#FindDigraphBy({match})

            À l'intérieur des données unicode téléchargées, cherche les caractères dont
            le nom / digraphe matche {match}.

            Retourne une liste de dico.
            Chaque dico contient un ensemble d'infos concernant {match}:

                    - 'name'    nom

                    - 'glyph'   glyphe

                    - 'dec'     valeur décimale du codepoint

                    - 'hex'     valeur hexa du codepoint

                    - 'dig'     digraphe;
                                s'ils en existent plusieurs pour un même caractère, ils seront
                                séparés par des espaces; cette clé est optionnelle

                    - 'html'    entité HTML

            {match} peut être:

                    - une regex                               comparée au nom du caractère
                                                              sans tenir compte de la casse

                    - un nb décimal                           comparé au code du caractère

                    - un nb hexa préfixé par '0x', ou 'U+'    "


    unicode#Digraph({string})

            Retourne le glyphe généré par le digraphe {string}.

            {string} doit contenir exactement 2 caractères.


    unicode#UnicodeName({val})

            Retourne le nom du caractère dont le code décimal est {val}.

##
# Vim-easy-align

TODO:
revoir nos notes sur vim-lion, les adapter à vim-easy-align

Une règle d'alignement est un ensemble prédéfini d'options pour une tâche d'alignement habituelle.
Elle est associée à une touche délimitrice, tq:

        space | alignement général autour de whitespaces                                   |
        =     | opérateurs contenant le symbole = ( = ,  ==,  != ,  += ,  &&= , …)         |
        :     | dico                                                                       |
        .     | concaténation multilignes                                                  |
        bar   | tableau markdown                                                           |
        #     | lignes de commentaires bash/python/… avec différents niveaux d'indentation |
        ,     | arguments multilignes                                                      |
        "     | commentaires Vim                                                           |

Ces 8 touches sont associées à des règles d'alignements prédéfinies par le plugin lui-même.
On peut les modifier, ou ajouter nos propres règles associées à d'autres touches.
En mode interactif, pour appliquer une règle d'alignement, il faudra frapper la touche délimitrice.


            Lorem=ipsum
            dolor  =sit
            amet+=  consectetur==  adipiscing
            elit-= sed != do
            eiusmod= tempor= incididunt
            ut &&= labore

            Lorem,ipsum
            dolor  ,sit
            amet,  consectetur,  adipiscing
            elit, sed , do
            eiusmod, tempor, incididunt
            ut ,, labore

            Lorem<-ipsum
            dolor  <--sit
            amet<=  consectetur <- adipiscing
            elit<~~ sed <~ do
            eiusmod<-= tempor<=- incididunt
            ut <== labore


    <Plug>(EasyAlign)        :EasyAlign
    <Plug>(LiveEasyAlign)    :LiveEasyAlign

            Démarre le mode interactif.
            Démarre le mode interactif avec prévisualisation.

            En mode interactif, il faut taper un délimiteur.

            Le mode avec prévisualisation permet de modifier le délimiteur et les options
            à la volée, en voyant le résultat immédiatement, sans pour autant que les changements
            soient validés.

            On peut alterner entre:

                    - les modes interactifs avec/sans prévisualisation via C-P
                    - différents type d'alignements (gauche, droite, centré) via Enter

            Par défaut, le plugin aligne autour de la 1e occurrence du délimiteur sur chaque ligne.
            On peut choisir une/d'autre(s) occurrence(s) en préfixant le délimiteur:

                    | préfixe  | résultat                                                                |
                    | 2, 3, …  | 2e, 3e, … occurrence                                                    |
                    | -, -2, … | dernière, avant-dernière … occurrence                                   |
                    | *        | toutes les occurrences                                                  |
                    | **       | toutes les occurrences en alignant alternativement à gauche et à droite |


