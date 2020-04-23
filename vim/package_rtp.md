# Packages
## What is a Vim package?

A directory containing one or more plugins.

## What are the advantages of a package over normal plugins?

   - A package can be downloaded as:

       * an archive
       * a git repository

     An archive can be unpacked in a single directory.
     A git repo can easily be cloned (for installation) or pulled (for updating).

     In both cases, the package files are not mixed with files of other plugins.
     As a result, a package is easier to update and remove.

   - A package can contain multiple plugins that depend on each other.

   - A package can be loaded on-demand with `:packadd`.
     A plugin is always loaded.

## How to install a package from an archive in `/tmp/archive.zip`?

    $ mkdir -p ~/.vim/pack/my_package
    $ unzip /tmp/archive.zip ~/.vim/pack/my_package

The directory name `my_package/` is arbitrary, you can pick anything you like.

## Where should I put the documentation of a package I'm writing?

At its root:

    my_package/README.txt
    my_package/start/foo/plugin/foo.vim
    my_package/opt/bar/plugin/bar.vim
    ...

## Must there be a relationship between the name of the package, one of its plugins, one its files?

No.

You can choose three different names:

    my_package/start/my_plugin/plugin/my_file.vim
    ├────────┘       ├───────┘        ├─────┘
    │                │                └ Interface
    │                └ plugin
    └ package

## What's the default value of 'pp'?

The same as `'rtp'`.

## How does Vim use the value of 'pp'?

During startup, after  processing the `vimrc`, Vim iterates  over each directory
in `'pp'`.
In each of them, Vim looks for a subdirectory matching `pack/*/start/*`.
Every time one is found, Vim assumes it contains a plugin, and adds it to `'rtp'`.

You can check this like so:

    $ mkdir -p ~/.vim/pack/my_pack/start/foo
    $ vim
    :echo &rtp
    " should contain `~/.vim/pack/my_pack/start/foo`, because:
    "   - `~/.vim` is in 'pp'
    "   - `pack/mypack/start/foo` matches `pack/*/start/*`

Then, it loads all the plugins in `'rtp'`.

## When does Vim load `~/.vim/pack/my_pack/start/foo`?   `~/.vim/pack/my_pack/opt/bar`?

`foo` is loaded automatically.
`bar` is loaded only when the user executes `:packadd`.

## Why does Vim first finish updating 'rtp' with plugins in 'pp' before loading any plugin from any package?

Why not loading it immediately, as soon as it's found?

Suppose you have a  package `foo` which includes two plugins.
They need to call the same function, and you decide to move the latter in a library.

`foo` would include these files (and these statements):

    ┌─────────────────────────────────────┬─────────────────┐
    │ file                                │ statement       │
    ├─────────────────────────────────────┼─────────────────┤
    │ pack/foo/start/one/plugin/one.vim   │ call lib#func() │
    ├─────────────────────────────────────┼─────────────────┤
    │ pack/foo/start/two/plugin/two.vim   │ call lib#func() │
    ├─────────────────────────────────────┼─────────────────┤
    │ pack/foo/start/lib/autoload/lib.vim │ fu lib#func()   │
    │                                     │     ...         │
    │                                     │ endfu           │
    └─────────────────────────────────────┴─────────────────┘

Now suppose that when Vim finds a plugin in `pack/*/start/`, it loads it immediately.
Here's what would happen:

   - Vim finds `pack/foo/start/one/plugin/one.vim`, and sources it immediately

   - Vim executes `call lib#func()`

This would  cause an  error, because the  library would NOT  have been  added to
`'rtp'` and Vim would NOT find the definition of `lib#func()`.

IOW,  Vim must  have  a  complete knowledge  of  all  plugins' locations  before
sourcing any of them.

For more info, see `:h packload-two-steps`.

#
# Plugins
## How to prevent plugins and packages from being loaded?

Reset `'loadplugins'` in the vimrc.

Or, start Vim with any of these command-line arguments:

   * `-u NONE`
   * `--clean`
   * `--noplugin`

## Which command does Vim execute to load plugins at startup?

    :runtime! plugin/**/*.vim

## How to make `:runtime` print a message when it doesn't find any file?

    :1verb runtime path/to/file

## How to make `:runtime` print a message for every file it sourced?

    :2verb runtime path/to/file

Look for the pattern `sourcing`.

## How to make `:runtime` print a message for each location where it tried to find the file?

    :3verb runtime path/to/file

##
##
##
##
## In which order are the plugins loaded (inside/outside packages, inside/outside `after/`)?

   1. plugins outside `after/` and outside packages
   2. plugins outside `after/` and inside  packages

   3. plugins inside  `after/` and outside packages
   4. plugins inside  `after/` and inside  packages

All directories in `'rtp'` (except the ones ending in `after/`) are searched for
a `plugin/`  subdirectory. Inside, all  files ending in  `.vim` are  sourced (in
alphabetical order per directory), also in subdirectories.

Directories in  `'rtp'` ending  in `after/`  are skipped  here, and  only loaded
after packages.

Packages are loaded.  These are plugins  found in the `start/` directory of each
entry in `'pp'`.  Every plugin directory found  is added in `'rtp'` and then the
plugins are sourced.

Plugins in directories ending in `after/` are loaded.

For more info, see `:h load-plugins`.

## ?

To load packages earlier, so that `'rtp'` gets updated:

    :packloadall

This also works when loading plugins is disabled.  The automatic loading will
only happen once.

If the package has an `after/` directory,  that directory is added to the end of
`'rtp'`, so that anything there will be loaded later.



    :packl[oadall][!]

            Load  all packages  in the  `start/` directory  under each  entry in
            'pp'.

            First all the directories found are added to 'rtp', then the plugins
            found  in the  directories are  sourced.  This  allows for  a plugin
            to  depend  on something  of  another  plugin, e.g.  an  `autoload/`
            directory.

            This is  normally done  automatically during startup,  after loading
            your .vimrc file.  With this command it can be done earlier.

            Packages  will be  loaded only  once.  After  this command  it won't
            happen again.  When  the optional ! is added this  command will load
            packages even when done before.

            An error  only causes  sourcing the  script where  it happens  to be
            aborted, further plugins will be loaded.



                    Charger automatiquement un seul plugin.

If you don't have a package but a single plugin, you need to create the extra
directory level:

    $ mkdir -p ~/.vim/pack/foo/start/foobar
    $ cd ~/.vim/pack/foo/start/foobar
    $ unzip /tmp/someplugin.zip

You would now have these files:

    pack/foo/start/foobar/plugin/foo.vim
    pack/foo/start/foobar/syntax/some.vim

From here it works like above.


                               Plugins optionnels

To load an optional plugin from a pack use the `:packadd` command:

    :packadd foodebug

This searches for `pack/*/opt/foodebug` in `'pp'`, will find
`~/.vim/pack/foo/opt/foodebug/plugin/debugger.vim`, and source it.

This could be done if some conditions are met.  For example, depending on
whether Vim supports a feature or a dependency is missing.

You can also load an optional plugin at startup, by putting this command in
your `.vimrc`:

    :packadd! foodebug

The extra `!` is so that the plugin isn't loaded if Vim was started with
`--noplugin`.

It is perfectly normal for a package to only have files in `opt/`.
You then need to load each plugin when you want to use it.


                                Où mettre quoi ?

Since color schemes, loaded with  `:colorscheme`, are found below `pack/*/start`
and `pack/*/opt`, you could put them  anywhere.  We recommend you put them below
`pack/*/opt`, for example `.vim/pack/mycolors/opt/dark/colors/very_dark.vim`.

Filetype plugins should go under `pack/*/start`, so that they are always
found.  Unless you have more than one plugin for a file type and want to
select which one to load with `:packadd`.  E.g. depending on the compiler
version:

    if foo_compiler_version > 34
        packadd foo_new
    else
        packadd foo_old
    endif

`after/` is most likely not useful in a package.  It's not disallowed though.

==============================================================================
6. Creating Vim packages                *package-create*

This assumes you write one or more plugins that you distribute as a package.

If you have two unrelated plugins you would use two packages, so that Vim
users can chose what they include or not.  Or you can decide to use one
package with optional plugins, and tell the user to add the ones he wants with
`:packadd`.

Decide how you want to distribute the package.  You can create an archive or
you could use a repository.  An archive can be used by more users, but is a
bit harder to update to a new version.  A repository can usually be kept
up-to-date easily, but it requires a program like "git" to be available.
You can do both, github can automatically create an archive for a release.

Your directory layout would be like this:

        start/foobar/plugin/foo.vim        " always loaded, defines commands
        start/foobar/plugin/bar.vim        " always loaded, defines commands
        start/foobar/autoload/foo.vim      " loaded when foo command used
        start/foobar/doc/foo.txt           " help for foo.vim
        start/foobar/doc/tags              " help tags

        opt/fooextra/plugin/extra.vim      " optional plugin, defines commands
        opt/fooextra/autoload/extra.vim    " loaded when extra command used
        opt/fooextra/doc/extra.txt         " help for extra.vim
        opt/fooextra/doc/tags              " help tags

This allows for the user to do:

    mkdir ~/.vim/pack/myfoobar
    cd ~/.vim/pack/myfoobar
    git clone https://github.com/you/foobar.git

Here `myfoobar` is a name that the user can choose, the only condition is that
it differs from other packages.

In your documentation you explain what the plugins do, and tell the user how
to load the optional plugin:

    :packadd! fooextra

You could add this packadd command in one of your plugins, to be executed when
the optional plugin is needed.

Run the `:helptags` command to generate the doc/tags file.  Including this
generated file in the package means that the user can drop the package in his
pack directory and the help command works right away.  Don't forget to re-run
the command after changing the plugin help:

    :helptags path/start/foobar/doc
    :helptags path/opt/fooextra/doc

==============================================================================

    :runtime syntax/c.vim

Sources the first file `syntax/c.vim`  found in a directory of `'rtp'`.
No error is raised if the file is not found.

When [!] is included, all found files are sourced.
When it is not included only the first found file is sourced.

When [where] is omitted only `'rtp'` is used.

When {file} contains wildcards it is expanded to all matching files.  Example:

    :runtime! plugin/*.vim

## Which values can be used in place of `[where]` in:   `:runtime [where] file ...`?

    ┌───────┬───────────────────────────────────────────────┐
    │ START │ search under `start/` in 'pp'                 │
    ├───────┼───────────────────────────────────────────────┤
    │ OPT   │ search under `opt/` in 'pp'                   │
    ├───────┼───────────────────────────────────────────────┤
    │ PACK  │ search under `start/` and `opt/` in 'pp'      │
    ├───────┼───────────────────────────────────────────────┤
    │ ALL   │ first use 'rtp',                              │
    │       │ then search under `start/` and `opt/` in 'pp' │
    └───────┴───────────────────────────────────────────────┘

##
##
##
# Todo
## Read this

    :h :runtime
    :h :packadd
    :h :packloadall

It seems that you can use all metacharacters documented in `:h file-pattern`.
Document this.

## ?

> One annoyance with packages is `:helptags ALL` does not consider `opt` directories. Personally, I like having help documentation tags built for all packages, even optional ones.

> Here is an "enhanced" command, `:Helptags`:

>      command! -nargs=0 -bar Helptags for p in glob('~/.vim/pack/*/opt/*', 1, 1) | exe 'packadd '.fnamemodify(p, ':t') | endfor | silent! helptags ALL

<https://www.reddit.com/r/vim/comments/g68bf6/pathogen_is_dead_or_should_be_long_live_vim_8/fo861i8/>

## ?

Could  we use  Vim packages  to eliminate  the separation  of plugins'  config
between `~/.vim/plugin` and `~/.vim/after/plugin/`?

> What  I like  about packadd  is  that **you  can actually  put the  before**
> **and  after  config**  and  the  loading of  the  plugin  **in  a  single**
> **file**.  That's because packadd loads the plugin right when it's called as
> apposed to most plugin managers that collect the list of all plugins to load
> before loading  them.  (For  that to  work plugins need  to be  installed in
> a  pack/**/opt  directory  i.e.  when  using  the  minpac  package  manager:
> minpac#add(url, {'type': 'opt'}))

> Oh that's  a neat idea. I  think at  the moment though  I prefer to  see all
> external plugins that will be loaded  in the one place. I use :packadd! (the
> ! version) which adds the plugins to  the runtime path but doesn't load them
> immediately. Also, that  way the plugins are  loaded when they expect  to be
> loaded (ie. in the usual place in the startup order).

Source:

- <https://www.reddit.com/r/vim/comments/a5ngap/debugging_your_vim_config_vimways_1224/eboufag/>
- <https://www.reddit.com/r/vim/comments/a5ngap/debugging_your_vim_config_vimways_1224/ebow7d5/>

