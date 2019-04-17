# runtimepath
## Which directories are in Vim's rtp by default (`$ vim -Nu NORC`)?

        ┌────────────────────────┬────────────────────────────────────────────────────────┐
        │ 1. ~/.vim              │ user config                                            │
        ├────────────────────────┼────────────────────────────────────────────────────────┤
        │ 2. $VIM/vimfiles       │ sysadmin config                                        │
        ├────────────────────────┼────────────────────────────────────────────────────────┤
        │ 3. $VIMRUNTIME         │ default config shipped with Vim                        │
        ├────────────────────────┼────────────────────────────────────────────────────────┤
        │ 4. $VIM/vimfiles/after │ allows the sysadmin to override the $VIMRUNTIME config │
        ├────────────────────────┼────────────────────────────────────────────────────────┤
        │ 5. ~/.vim/after        │ same thing for the user                                │
        └────────────────────────┴────────────────────────────────────────────────────────┘

## Which directories are in Neovim's rtp by default (`$ nvim -Nu NORC`)?

TLDR:

Before `$VIMRUNTIME`, Neovim includes:

        $XDG_CONFIG_HOME/nvim (user config)
        $XDG_CONFIG_DIRS/nvim (sysadmin config)
        $XDG_DATA_HOME/nvim/site (user plugins)
        $XDG_DATA_DIRS/nvim/site (sysadmin plugins)

After `$VIMRUNTIME`, Neovim includes:

        $XDG_DATA_DIRS/nvim/site/after
        $XDG_DATA_HOME/nvim/site/after
        $XDG_CONFIG_DIRS/nvim/after
        $XDG_CONFIG_HOME/nvim/after

---

In case you didn't notice:

        - those are the same directories, in reverse order, and with the `after/` suffix
        - `$XDG_CONFIG_DIRS` is a SET of directories; same thing for `$XDG_DATA_DIRS`
                          ^
                          plural

And in case you wonder what those `$XDG_...` variables are:

        https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

---

More details.

There are 9 sets of directories:

        1. $XDG_CONFIG_HOME/nvim

Usually, `$XDG_CONFIG_HOME` is `~/.config`.
If `$XDG_CONFIG_HOME` is not set, Neovim falls back on `$HOME/.config`.


        2. $XDG_CONFIG_DIRS/nvim

`$XDG_CONFIG_DIRS` is an array of directories.
So this second set contains more than one directories.
Example:

        /etc/xdg/xdg-xubuntu/nvim
        /usr/share/upstart/xdg/nvim
        /etc/xdg/nvim


        3. $XDG_DATA_HOME/nvim/site

Usually `$XDG_DATA_HOME` is `~/.local/share`.


        4. $XDG_DATA_DIRS/nvim/site

`$XDG_DATA_DIRS` is an array of directories.
So this fourth set contains more than one directories.
Example:

        /usr/share/xubuntu/nvim/site
        /usr/share/xfce4/nvim/site
        /usr/local/share/nvim/site
        /usr/share/nvim/site
        /var/lib/snapd/desktop/nvim/site


        5. $VIMRUNTIME

        6. $XDG_DATA_DIRS/nvim/site/after

        7. $XDG_DATA_HOME/nvim/site/after

        8. $XDG_CONFIG_DIRS/nvim/after

        9. $XDG_CONFIG_HOME/nvim/after

## Which directories does `vim-plug` add to the rtp?  In which position exactly?

It adds 2 new FAMILIES (one directory per third-party plugin) of directories:

        - ~/.vim/plugged/{plugin}

          just after `~/.vim`

        - ~/.vim/plugged/{plugin}/after

          just before `~/.vim/after`

##
## In which order does Vim add my local plugins (`~/.vim/plugin`, `~/.vim/after/plugin`) to the rtp?

In their alphabetical order.

Same thing for the plugins in `$VIMRUNTIME/plugin`.

## In which order does `vim-plug` add my plugins to the rtp?

In the same order you declared them with your `:Plug` statements.

###
## Why is `~/.vim/plugged/{plugin}` added after `~/.vim` in the rtp?

To give the user a chance to disable it before it's sourced.

They could do so by creating a file such as:

    $ cat ~/.vim/plugin/foo.vim
          let g:loaded_foo = 1

## Why is `~/.vim/plugged/{plugin}/after` added before `~/.vim/after` in the rtp?

To give the user a chance to override some of its settings.

## In Neovim, why is `~/.config/nvim` added after the third-party plugins in the rtp?

I'm not sure, but it seems to be an error.

Anyway, this is due to those lines in `~/.config/nvim/init.vim`:

        set rtp^=~/.vim
        set rtp+=~/.vim/after

If you remove them, `vim-plug` will correctly add:

        - `~/.config/nvim`       before the third-party plugins
        - `~/.config/nvim/after` after  the third-party plugins

##
## Where does Vim look for a color scheme when I execute `:colo {colorscheme}`?

In any `colors/` subdirectory of a directory in the rtp.

## Where does Vim look for a compiler when I execute `:compiler {compiler}`?

In any `compiler/` subdirectory of a directory in the rtp.

## Where does Vim look for documentation files when I execute `:helptags ALL`?

In any `doc/` subdirectory of a directory in the rtp.

## Where does Vim look for a tag when I execute `:help {tag}`?

In any `doc/tags` file inside a directory of the rtp.

## Where does Vim look for spell files?

In any `spell/` subdirectory of a directory in the rtp.

## What's the main difference between `:helptags`, and `:colo` / `:compiler`?

You can pass a name as argument to `:colo` and `:compiler`.
They will  automatically suffix the  name with `.vim`,  and prefix it  with some
subdirectories of the rtp.

OTOH, `:helptags` is not that smart.
It expects as an argument either:

   - a full path to the documentation file
   - a path relative to the cwd

But it does *not* look in the rtp.

## Can I add the same path twice to the rtp?

With `:set`, no.
With `:let`, yes.

MWE:

        $ vim -Nu NONE
        :set rtp+=/tmp
        :set rtp^=/tmp
        :echo &rtp

The last command includes `/tmp` only once.
The second `:set` had no effect, because `/tmp` was already somewhere in the rtp.

        $ vim -Nu NONE
        :set rtp+=/tmp
        :let &rtp = '/tmp,'.&rtp
        :echo &rtp

##
# Filetype detection
## Theory
### How important is it?  What gets broken if it's wrong?

All  buffer-local mechanisms  (filetype, indent,  syntax) rely  on the  filetype
detection.
If the latter fails, all these mechanisms will fail too.

###
### What's the expansion of $VIM?

In Vim:
        /usr/local/share/vim
             │
             └ only if you compile Vim and install it with `checkinstall`

In Neovim:
        /usr/local/share/vim

### What's the expansion of $VIMRUNTIME?

In Vim:
        /usr/local/share/vim/vim81
                                ├┘
                                └ may vary; matches Vim's current version

In Neovim:
        /usr/local/share/nvim/runtime

###
### `$VIMRUNTIME/filetype.vim` installs 4 sets of autocmds, and run 1 command.  What does each of them do?

1. watch the extension of the name of the buffer

2. source all `scripts.vim` files in the rtp

    This  is  a  real  autocmd  listening  to  `BufNewFile`,  `BufReadPost`  and
    `StdinReadPost`.

    It needs to be an autocmd, because the `scripts.vim` files are just scripts,
    they don't contain any autocmd.
    So, every time a buffer fails to  be recognized via its extension, they must
    be sourced.

3. watch another part of the name of the buffer

4. source autocmds from all `ftdetect/` directories in the rtp

    This is NOT a real autocmd, it's just a `:runtime!` command:

            runtime! ftdetect/*.vim

    It doesn't  need to  be an  autocmd, because each  of those  scripts already
    contains an autocmd.

5. set the filetype to `conf` as an ultimate fallback,
   if one of the first 5 lines of the buffer begin with `#`

### When a buffer is loaded and its filetype must be set, what does Vim look at? (5)

        1. its extension
        2. its contents
        3. other parts of its name
        4. its extension (again)
        5. its first few lines

### What's the rationale behind this order?

This order is meant to give the priority to the most reliable mechanisms.

Watching the extension of the name of a buffer is the most reliable way to guess
its filetype.
For example,  if you load the  buffer `file.py`, you  can be sure it's  a python
buffer because that's a widely adopted convention.

OTOH, watching other parts of the name of a buffer is less reliable.
For example, if you load a  buffer whose name matches `crontab.*`, it's probably
a crontab file, but you can't be sure.
It could also be a script written in some language whose goal is to manipulate a
crontab file in some way.

The `scripts.vim` files are positioned in the second place, because guessing the
filetype of  a buffer according to  its contents is less  reliable than watching
its extension, but more reliable than watching other parts of its name.

The  `ftdetect/` files  are positioned  in the  4th place,  to provide  a second
mechanism watching the extensions of the buffers names, with a lesser priority.
This allows plugin authors to use this  mechanism, and in case of conflict, give
the priority to the autocmds in `$VIMRUNTIME/filetype.vim`.

###
### When is the autocmd from `plugged/abc/ftdetect/` sourced compared to the ones from `plugged/def/filetype.vim`?

`def/filetype.vim` is sourced BEFORE `abc/ftdetect/`.

Note that even if your plugin manager has added the plugin `abc` before `def` in
the rtp, it doesn't matter.
ALL the autocmds  in the `filetype.vim` files are sourced  BEFORE ANY autocmd in
`ftdetect/`.

##
## Getting information
### How to list all filetypes recognized by Vim?

        :setf C-d

### How to know which mechanism Vim has enabled, among filetype detection, filetype plugins, and indent plugins?

        :filet[ype]

###
### How to get the list of filetype detection scripts located in a `ftdetect/` directory?

        :Find! ~/.vim -path '*/ftdetect/*'

### How to get the list of filetype detection scripts located in a `filetype.vim` file?

        :Find! ~/.vim -name 'filetype.vim'

###
## Acting
### Which mechanisms are enabled by `:filetype plugin indent on`?

        :filetype plugin indent on
         │        │      │
         │        │      └ enable indent plugins
         │        │
         │        └ enable filetype plugins
         │
         └ enable filetype detection

### How to disable the filetype plugins?  the indent plugins?

        :filetype plugin off
        :filetype indent off

---

Here are all the 8 possible `:filetype` commands:

        ┌─────────────────────────────┬───────────┬───────────┬───────────┐
        │ command                     │ detection │ plugin    │ indent    │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype on                │ on        │ ∅         │ ∅         │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype off               │ off       │ ∅         │ ∅         │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype plugin on         │ on        │ on        │ ∅         │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype plugin off        │ ∅         │ off       │ ∅         │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype indent on         │ on        │ ∅         │ on        │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype indent off        │ ∅         │ ∅         │ off       │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype plugin indent on  │ on        │ on        │ on        │
        ├─────────────────────────────┼───────────┼───────────┼───────────┤
        │ :filetype plugin indent off │ ∅         │ off       │ off       │
        └─────────────────────────────┴───────────┴───────────┴───────────┘
        ∅ = no change

### Which file(s) are sourced when I execute `:filetype on`?  `:filetype plugin on`?  `:filetype indent on`?

        ┌─────────────────────┬───────────────────────────┐
        │ :filetype on        │ $VIMRUNTIME/filetype.vim *│ * = and any `filetype.vim` in the rtp
        ├─────────────────────┼───────────────────────────┤
        │ :filetype plugin on │ $VIMRUNTIME/ftplugin.vim  │
        ├─────────────────────┼───────────────────────────┤
        │ :filetype indent on │ $VIMRUNTIME/indent.vim    │
        └─────────────────────┴───────────────────────────┘

### What do they do?

`$VIMRUNTIME/filetype.vim`  installs some  autocmds  which  set 'filetype'  when
`BufReadPost` is fired.

`$VIMRUNTIME/ftplugin.vim` installs 1 autocmd listening to `FileType *`.
It sources all the files in a directory of the rtp, and whose end of the path matches:

        ftplugin/&ft.vim
        ftplugin/&ft_*.vim
        ftplugin/&ft/*.vim
                 ├─┘
                 └ the autocmd gets the filetype by expanding `<amatch>`

`$VIMRUNTIME/indent.vim` installs 1 autocmd listening to `FileType *`.
It sources all the files in a directory of the rtp, and whose end of the path matches:

        indent/&ft.vim

##
### What are all the locations where I can write my filetype detection files?  What's the difference between them?

Do you want your script to be sourced after `$VIMRUNTIME/filetype.vim`?
If yes, use `ftdetect/&ft.vim`

If no, do you want to set the filetype according to the name of the file or its contents?
If you rely on the name, use `filetype.vim`, otherwise use `scripts.vim`.

Note that these 3 paths must be relative to any directory in the rtp.

For more info, read `:h ftdetect`, and:

        https://vi.stackexchange.com/a/14339/17449

### Why should I use `filetype.vim` instead of `ftdetect/`?

If you set the  filetype detection too late, Vim may set  it wrongly, which will
cause various undesired plugins to be sourced.

You   could  use   `:set`  to   fix  this,   but  you'll   still  source   wrong
filetype/indent/syntax plugins, and you don't know whether their effects will be
correctly undone when the detection will be changed.

### Is there an issue with using `filetype.vim`?  Does it matter?

Yes.

You may use an extension for a new type of special buffer A (freekeys, hydra, ...).
But, what you don't  know, is that it's is already used  to set another filetype
B, for example in `$VIMRUNTIME/filetype.vim`.
In this case, your buffer A will be correctly detected, but not B.

That being said, no matter what you do, you can't avoid this kind of issues.

Note that the issue will NOT go unnoticed forever.
It will go unnoticed as long as you don't load a buffer B.
When you'll load B, you'll obviously see that the filetype is not correctly set.

You have  to choose between  possibly breaking your special  buffers immediately
and/or frequently, or breaking UNused filetypes (types of buffers you never load
atm).
I prefer the risk of breaking UNused filetypes.
Also, I  don't think  it matters  much to know  RIGHT NOW  that I've  broken the
detection of a filetype that I never use.

### Where should I use `:setf`?  What about `:set ft=`?

Use `:setf` everywhere.

It will make sure you don't set the filetype twice.

This is recommended in `:h 43.2`:

> The "setf" command  will set the 'filetype' option to  its argument, unless it
> was set already.
> This will make sure that 'filetype' isn't set twice.

### How to set the filetype of all files, in a directory, which don't have an extension (and only them!) to 'sh'?

Use an `after/` directory:

                               vvvvv
        $ cat <<'EOF' >>~/.vim/after/filetype.vim

        augroup filetypedetect
            au! BufNewFile,BufRead /path/to/dir/* setf sh
        augroup END
        EOF

Now, if  your directory contains files  with some extensions, you  can set their
filetypes in a `filetype.vim` sourced earlier:

        $ cat <<'EOF' >>~/.vim/filetype.vim

        augroup filetypedetect
            au! BufNewFile,BufRead /path/to/dir/*.md setf markdown
        augroup END
        EOF

---

Instead of `after/filetype.vim`, you could also use `ftdetect/*.vim`.

However, it's probably better to use `after/filetype.vim`.
Otherwise, an autocmd from a `ftdetect/` subdirectory of the rtp may wrongly set
the filetype of your files before your autocmd has the chance to do its job.
And if  your autocmd  uses `:setf`  (it should), it  won't be  able to  undo the
detection.

Besides, `after/filetype.vim` is mentioned at `:h 43.2`.

### How to set the filetype of a file, and still allow any later script to reset it (even if it uses `:setf`)?

Pass the optional FALLBACK argument to `:setf`:

        :setf FALLBACK {your filetype}

This will tell  Vim that your filetype should  be used only as a  fallback if no
script sets the filetype later.
Technically, this is achieved by  making `did_filetype()` return false after the
command, instead of true.

From `:h :setf`:

>    When  the  optional FALLBACK  argument  is  present, a  later  :setfiletype
>    command will override the 'filetype'.
>    This is to used for filetype detections that are just a guess.
>    |did_filetype()| will return false after this command.

---

Don't use this unless you *really* have to.
Otherwise, you may set the filetype of a buffer twice.
The last  detection may be  correct, but sourcing  2 filetype plugins,  2 syntax
plugins, ...  is bad  for the performance,  and you have  no guarantee  that the
effects of the first plugins will be correctly undone.

###
### Which guard should I write in a `scripts.vim` file?

	if did_filetype()
	    finish
	endif

#### Why?

If the filetype has already been set, there's no need to run all the commands in
the script.

This improves performance.

###
### How can I set several filetypes consecutively?

Separate the filetype names with dots:

        setf ft1.ft2.ft3...

### How to prevent Vim from assigning a filetype to a file?

Include  a  subpattern   matching  its  extension  in  the   pattern  stored  in
`g:ft_ignore_pat`.
The default value of the latter is:

        '\.\(Z\|gz\|bz2\|zip\|tgz\)$'

### How to ask Vim to look at the new contents I've just inserted, to set the filetype of the current buffer?

        :filetype detect

Useful for  example, when you've  begun writing a shell  script in a  new buffer
which initially didn't have any filetype.

###
### Why shouldn't I use `setf markdown.html` to load the html filetype plugins in addition to the markdown ones?

The markdown filetype plugin sets `b:did_ftplugin`, and the html filetype plugin
has a guard, so it wouldn't be sourced.

Besides, even if it was sourced, you  would also be sourcing the html indent and
syntax plugins which you may not want.
Indeed, `set markdown.html` would fire the `FileType` event with the value html.
This, in turn, would cause SEVERAL kinds of plugins to be sourced.

---

More generally, `setf foo.bar` will not always source the `bar`
filetype/syntax/indent plugins.
It depends on whether they have a guard.

From `:h 'syntax`:

> Note that the second one must be prepared to be loaded as an addition,
> otherwise it will be skipped.

### What should I do instead?  What's the benefit?

Use `:runtime`:

        " ✔ in ftplugin/markdown.vim
        :runtime! ftplugin/html.vim

This approach is more granular than the broad:

        " ✘
        :setf markdown.html

You can choose exactly which kind of markdown plugin you want to load (ftplugin,
indent, syntax).

### When is it ok to use `setf foo.bar` to source the 'bar' filetype plugin?

When it doesn't have a guard and there's no `bar` syntax, indent plugins.
Or you don't mind all of 3 of them being sourced.

###
# Filetype plugins
## Theory
### When is the `FileType` event fired?

When the 'filetype' option of a buffer is set.

### Which three lines of code are equivalent to `:setf sh`?

            ┌ `did_filetype()` evaluates to true when an autocmd is being processed,
            │ and the `FileType` event has been fired at least once for the current buffer
            │
        if !did_filetype()
            setl ft=sh
        endif

###
### Are all autocmds listening to `BufReadPost` executed before the ones listening to `FileType`?

No.

As soon  as an autocmd sets  up `'ft'`, Vim stops  processing `BufReadPost`, and
begins processing the autocmds listening to `FileType`.
It will finish processing `BufReadPost` afterwards.

### Is it possible to inspect the filetype of a buffer from an autocmd listening to `BufReadPost`?

Yes.

### Is there a condition?

Yes.

Let's call (A) and (B) two autocmds listening to `BufReadPost`.
(B)  sets the  filetype, and  (A)  inspects the  filetype to  do some  arbitrary
action.
(A) must be sourced  after (B), to be able to correctly  inspect the filetype of
the buffer.

---

That's one  reason why your custom  autocmds should be sourced  AFTER `:filetype
plugin indent on`.
If they expect to look at the filetype of your buffer, or some setting installed
by a default filetype plugin, they need to be sourced after.

##
## Acting
### Where can I put my C filetype plugin?

        - dir/ftplugin/c.vim
        - dir/ftplugin/c_*.vim
        - dir/ftplugin/c/*.vim

`dir/` must be present in 'rtp'.
`*` can be any sequence of characters.

### Where can I put my C syntax plugin?

   - dir/syntax/c.vim
   - dir/syntax/c/*.vim

---

`syntax/html_*.vim` is *not* a valid file pattern for an html syntax plugin.

Vim doesn't use it when we do `:set syn=foo`:

    :2Verb set syn=foo
    Searching for "syntax/foo.vim syntax/foo/*.vim" in ...~
    not found in 'runtimepath': "syntax/foobar.vim syntax/foobar/*.vim"~

### Where can I put my C indent plugin?

        dir/indent/c.vim

###
### How to load all C filetype plugins from a C++ filetype plugin?

        :runtime! ftplugin/c.vim ftplugin/c_*.vim ftplugin/c/*.vim

Useful to avoid having to repeat some common settings (like the folding ones).

###
### How to prevent a filetype plugin from being sourced if another has already been sourced?

Include this guard at the start of the plugin:

        if exists('b:did_ftplugin')
            finish
        endif

### Why should I NOT write guards in my filetype plugins located in an `after/` directory?

They are  meant to  customize another  plugin, which  necessarily will  have set
`b:did_ftplugin`, `b:did_indent`, `b:current_syntax`.
So, putting a guard in `after/foo.vim` will UNconditionally disable `after/foo.vim`,
which is not the purpose of a guard.
A guard is meant to disable a plugin when some conditions are met.

### Why should I write guards in my other filetype plugins?

To be consistent with how the  other plugins (`$VIMRUNTIME` and third-party) are written.

### My filetype plugin is split across several files.  In which file(s) should I write its guard?

In the one using the simplest naming scheme.

Example:

        ~/.vim/plugged/potion/ftplugin/potion.vim
        ~/.vim/plugged/potion/ftplugin/potion/folding.vim

Write it only in `ftplugin/potion.vim`.

I think the bulk of the customizations should be in one file.
The others, if any, are just minor tweaks, which are not meant to be guarded.
Anyway, you can't write a guard  in `potion/folding.vim`, because it would NEVER
be sourced since either:

        - `ftplugin/potion.vim` WILL have been sourced and set `b:did_ftplugin`

        - `ftplugin/potion.vim` will NOT have been sourced,
          because a previous filetype plugin in the rtp will already have been sourced,
          and the latter will have set `b:did_ftplugin`

---

What makes you think that we're not meant to write a guard in all the files?

Watch [these lines](https://github.com/tpope/vim-haml/blob/ac1cb44d58747ac70a4077da3796a9f696ee46a9/ftplugin/haml.vim#L19-L20):

        runtime! ftplugin/html.vim ftplugin/html_*.vim ftplugin/html/*.vim
        unlet! b:did_ftplugin

Tpope doesn't remove `b:did_ftplugin` after every sourced file, which would have
given:

        runtime! ftplugin/html.vim   | unlet! b:did_ftplugin
        runtime! ftplugin/html_*.vim | unlet! b:did_ftplugin
        runtime! ftplugin/html/*.vim | unlet! b:did_ftplugin

In fact, even if he did, it would still be not enough.
Indeed, `:runtime` is  passed the bang argument, which means  that it can source
several files matching the pattern.

Besides, the last 2 commands contain wildcards.
If you wanted to  be completely safe, you would need to find  a way to unlet the
guard after every file that `:runtime` finds.
That is, you would have to execute `:runtime` verbosely to find these files.
Or use `globpath()` (`globpath(&rtp, 'pat')`).
Then source each file with `:source`, and unlet afterwards.
Too cumbersome to do.

---

If  you really  wanted  to prevent  `potion/folding.vim` to  be  sourced when  a
previous  filetype plugin  has been  sourced  in the  rtp, maybe  you could  set
another variable in `ftplugin/potion.vim`:

        let b:did_my_ftplugin = 1
                 ^^^^

Then, in `potion/folding.vim`, you would check it existence:

        if !exists('b:did_my_ftplugin')
            finish
        endif

This would tie the 2 scripts together.
As a result, if `ftplugin/potion.vim` has not been sourced, `potion/folding.vim`
would do the same.

You also probably would have to remove `b:did_my_ftplugin` after every `:runtime`:

        runtime! ftplugin/potion.vim   | unlet! b:did_ftplugin b:did_my_ftplugin
        runtime! ftplugin/potion_*.vim | unlet! b:did_ftplugin b:did_my_ftplugin
        runtime! ftplugin/potion/*.vim | unlet! b:did_ftplugin b:did_my_ftplugin

###
### How to reload the filetype plugins for the current buffer?  (2)

        :do filetypeplugin filetype

        :let &ft = &ft

You  could use  `:e`, but  it would  cause ALL  “local” plugins  to be  reloaded
including the syntax ones.

### How to reload all filetype/indent/syntax plugins for ALL buffers?

        :doautoall filetypedetect BufReadPost

The augroup `filetypedetect` is defined in `$VIMRUNTIME/filetype.vim`.

### How to reload the filetype plugins for ALL buffers?

        :doautoall filetypeplugin FileType

The augroup `filetypeplugin` is defined in `$VIMRUNTIME/ftplugin.vim`.
It   contains  only   one  autocmd   which  calls   `s:LoadFTPlugin()`  whenever
`'filetype'` is set.
The latter sources all filetype plugins found in the rtp.

---

Don't use `:bufdo`, it would change the current buffer:

        :bufdo let &ft = &ft  ✘
        :bufdo e              ✘

And fuck up the syntax highlighting  of most buffers, because the `Syntax` event
is disabled while `:bufdo` is being executed.

### Does reloading a filetype plugin reset all local options?

No.

It doesn't reset the window-local options  which are set from autocmds listening
to BufWinEnter.
For these, execute:

        :do bufwinenter

###
### How to remove a mapping from `b:undo_ftplugin`?

`:nunmap` interprets the  `|` as a command termination, so  you can include this
command in the variable:

        nunmap <buffer> <lhs>| other_command
                             ^
                             ✔

But make sure to avoid a trailing whitespace:

        nunmap <buffer> <lhs> | other_command
                             ^
                             ✘
                             this trailing whitespace would be included in the lhs

---

Be aware that if another filetype plugin updates `b:undo_ftplugin` and adds sth like:

        let b:undo_ftplugin .= ' | some_command'
                                ^
                                ✘

While you added  an `:nunmap` command at the end  of `b:undo_ftplugin`, it could
result in a trailing whitespace being passed to your `:nunmap`.

---

You could also use `:exe`:

        exe 'nunmap <buffer> <lhs>'

---

Note that  `:exe` is not  useful to prevent `:nunmap`  or `:nno` to  consume the
next commands. These commands work fine:

        if 1 | nno cd :echo 'hello'<cr> | endif
        nunmap cd| echo 'hello'
                 ^
                 again, no trailing whitespace

This is confirmed by the fact that `:nunmap` and `:nno` are absent from `:h :bar`.

And if  your lhs  or rhs  contains a  bar, as  usual, to  prevent it  from being
interpreted as a command  termination you have to escape it,  or use the keycode
`<bar>`.

##
# Indent plugins
## How to prevent Vim from indenting the current line when I insert some character, or open a new line?  (2)

Remove the character you insert (or `o`, `O` for a new line) from 'indk'.

See `:h indk`.

---

Or  look for  a global  variable  used by  the indentation  plugin, which  could
disable the undesired indenting.
Usually,  the help  documents the  default  indent plugins,  so to  find such  a
variable, try something like this:

        :h {filetype}*indent C-d

Example:

        :h html*indent C-d
        html-indent~
        html-indenting~
        ft-html-indent~

## Can I write an indentation setting in a filetype plugin?

No.

It should be inside an indent plugin.

Why?
Because you've probably executed this command (or vim-plug has done it for you):

        filetype plugin indent on

This means that the indent plugins are sourced AFTER the filetype plugins.
So, if you write an indentation setting  in a filetype plugin, even in `after/`,
it can still be undone by ANY indent plugin (default, custom, ...).

## Are the indent plugins sourced after the filetype ones because 'indent' is at the end in `filetype plugin indent on`?

No.

        $ vim -Nu NONE --cmd 'filetype plugin indent on'
        $ vim -Nu NONE --cmd 'filetype indent plugin on'

After starting Vim  with any of these commands, the  output of `:scriptnames` is
always the same:

        ~/.vim/filetype.vim
        $VIMRUNTIME/filetype.vim
        $VIMRUNTIME/ftplugin.vim
        $VIMRUNTIME/indent.vim

##
# Syntax plugins
## How to enable syntax highlighting?  (2)

        :syntax enable
        :syntax on

### Which way is better?

        :syntax enable

`:syntax on` sets default HGs, without checking whether they were already set.

Sources:

From `:h syn_cmd`:
> Only define colors for groups that don't have highlighting yet

From `:h syntax_loading`:
> ":syntax enable" only sets groups that weren't set yet

---

Technically, `:syntax on` and `:syntax enable` both source the file:

        $VIMRUNTIME/syntax/syncolor.vim

The latter execute the custom commands `:SynColor` and `:SynLink`, which,
depending on the argument passed to `:syn` (`enable` or `on`), are defined
differently:

        on:
            command -nargs=* SynColor hi          <args>
            command -nargs=* SynLink  hi link     <args>

        enable:
            command -nargs=* SynColor hi def      <args>
            command -nargs=* SynLink  hi def link <args>

We can see that for `:syntax enable`, the commands use `:hi def` instead of just
`:hi`.
The `def` argument prevents that we override an existing HG (set previously by a
color scheme).

### Why should it be enabled *after* the filetype plugins?

For `setl fdm=syntax` to  work in a given buffer, the syntax  must not have been
already sourced.

<https://stackoverflow.com/a/55692963/9780968>

##
## Besides syntax highlighting, what other fundamental mechanism is enabled by `:syntax on`?

filetype detection

So, there's no need to execute `:filetype on` after `:syntax on`.

## What are the 5 steps into which the execution of `:syntax enable` can be broken?

`:syn enable` sources `$VIMRUNTIME/syntax/syntax.vim`.
The latter does 5 things:

        1. source $VIMRUNTIME/syntax/nosyntax.vim

For  all  buffers,  this  clears  the  existing  syntax  elements,  and  removes
`b:current_syntax`.
If this  variable was not  removed, you wouldn't be  able to reload  your syntax
plugins with `:syn off | syn on`.
Indeed, a syntax plugin is supposed to begin with:

         if exists('b:current_syntax')
             finish
         endif

---

        2. source $VIMRUNTIME/syntax/synload.vim

This does 2 things:

        a) define some basic HGs (Comment, Statement, ...),
           by sourcing $VIMRUNTIME/syntax/syncolor.vim

        b) install an autocmd listening to `Syntax *` which sets the syntax elements of buffers
           by sourcing:

                :so syntax/{&ft}.vim
                :so syntax/{&ft}/*.vim

`a)` answers the question “how do we color?“
`b)` answers the question “what do we color?“

---

        3. :so $VIMRUNTIME/filetype.vim

Installs filetype detection (autocmds setting 'filetype').

---

        4. install an autocmd listening to `FileType *` to set the value
           of 'syntax' whenever 'filetype' is set

---

        5. execute this autocmd for all buffers by executing:

                doautoall syntaxset FileType

For each  buffer, this will set  'syntax', which will fire  `Syntax`, which will
load the appropriate syntax plugins.

##
## Which steps lead to Vim sourcing a syntax plugin when (re)loading a buffer?  (5)

        1. `BufRead`  is fired
        2. 'filetype' is set
        3. `FileType` is fired
        4. 'syntax'   is set
        5. `Syntax`   is fired

When  the last  step occurs,  Vim  sources the  relevant syntax  plugins in  all
`syntax/` directories of the rtp.

##
# Compiler plugins
## What's the main difference between a compiler plugin and a filetype/indent/syntax plugin?

Its settings are NOT applied automatically.
You need to execute the `:compiler` command.

##
## Where should I execute `:compiler foo`?

From a filetype plugin.

A  compiler sets  buffer-local options,  so  it makes  sense  to use  it from  a
filetype plugin.
Besides, this way, you can be sure  that its effect will persist after reloading
the buffer.

## What should I do in addition to `:compiler foo`?

Since the  compiler assigns  values to  `'efm'` and  `'mp'`, you  should include
those in `b:undo_ftplugin`.

##
# Guards
## What's the purpose of a guard?

It lets the user have a chance to disable the plugin.

The user can do  so by sourcing a statement such as `let  b:did_ftplugin = 1` or
`let b:current_syntax = 'tex'` before the plugin.

Example:

        " user script containing `let b:did_ftplugin = 1`
        ~/.vim/ftplugin/foo.vim

        " this third-party plugin containing a guard `if exists('b:did_ftplugin') ...`
        " won't be sourced entirely
        ~/.vim/plugged/vim-foo/ftplugin/foo.vim

It  can also  prevent  2  plugins, with  the  same  purpose (filetype  settings,
indentation, syntax highlighting), from being sourced for the same buffer.

## What does a guard look like in a filetype plugin?  In an indent plugin?  In a syntax plugin?

        ┌─────────────────────────────┬───────────────────────────┬───────────────────────────────┐
        │       filetype plugin       │       indent plugin       │         syntax plugin         │
        ├─────────────────────────────┼───────────────────────────┼───────────────────────────────┤
        │ if exists('b:did_ftplugin') │ if exists('b:did_indent') │ if exists('b:current_syntax') │
        │     finish                  │     finish                │     finish                    │
        │ endif                       │ endif                     │ endif                         │
        │ ...                         │ ...                       │ ...                           │
        │ let b:did_ftplugin = 1      │ let b:did_indent = 1      │ let b:current_syntax = '...'  │
        └─────────────────────────────┴───────────────────────────┴───────────────────────────────┘

##
## When should I include a guard in a filetype/indent/syntax plugin?

All the time, except in `after/`.

## Where should I write `let b:did_ftplugin = 1` in a filetype plugin?

At the end, before `b:undo_ftplugin`.

In particular, it should be before the last `:runtime` statement (if any).
Otherwise, you could face this issue:

        ...
        let b:did_ftplugin
        runtime! ftplugin/markdown.vim
        ...

Here `:runtime` will fail to source the markdown plugin if the latter contains a guard.

## When should I unlet `b:did_ftplugin`?

And after every `:runtime` command, otherwise you could face this issue:

        runtime! ftplugin/markdown.vim
        runtime! ftplugin/python.vim

The last `:runtime` may fail, because the previous one may have set `b:did_ftplugin`.

Example of code you could write:

        if exists('b:did_ftplugin')
            finish
        endif
        runtime! ftplugin/markdown.vim | unlet! b:did_ftplugin
        runtime! ftplugin/python.vim | unlet! b:did_ftplugin
        let b:did_ftplugin = 1

## Should I do the same for `let b:current_syntax = '...'` and `let b:did_indent = 1`?

Yes.

##
# Issues
## I've changed the name of file with `:file`, but the syntax highlighting is still wrong!

For the filetype detection  to work, the name of your buffer  must be set BEFORE
the `BufReadPost` or `BufNew` event:

        " ✘
        :new
        :file some_file

        " ✔
        :new some_file

## I have an `:echom` in one of my filetype plugin.  No message is printed nor logged!

That's because of `shortmess+=F`.

Use `:unsilent`:

        :unsilent echom 'your message'

## The default filetype plugin 'foo' sources the filetype plugin 'bar' (with `:ru`).  I don't want that!

Inside:

        ~/.vim/ftplugin/bar.vim

write:

        if &ft is# 'foo'
            let b:did_ftplugin = 1
        endif

---

If we didn't use  our own custom markdown filetype plugin,  this would be useful
to prevent  `$VIMRUNTIME/ftplugin/markdown.vim` from sourcing the  html filetype
plugin.

