# Updating a quickfix/location list asynchronously without interfering with another plugin

<https://gist.github.com/yegappan/3b50ec9ea86ad4511d3a213ee39f1ee0>

Updating a  quickfix or  location list asynchronously  opens up  the possibility
that two or more plugins may try to update the same quickfix list with different
output.
Also when a plugin  is updating a quickfix list in the  background, the user may
issue a command that creates or updates a quickfix list.
The plugin may then incorrectly use this new list to add the entries.

The various Vim commands that create or modify a qfl (like `:make`, `:grep`, and
`:cfile`) operate only on the current one.
A  plugin using  these commands  to update  the qfl  can interfere  with another
plugin.

To avoid these issues, `getqflist()` and `setqflist()` can be used to operate on
a specific list in the stack, using its unique id which can be obtained with:

    let qfid = getqflist({'id' : 0}).id

When adding new entries, the plugin can use `setqflist()` with this id:

    call setqflist([], 'a', {'id' : qfid, 'items' : newitems})

To parse the output of a command and add the quickfix entries, the plugin can use:

    call setqflist([], 'a', {'id' : qfid, 'lines' : cmdoutput})

Note that in the  previous command, the current `'efm'` option  is used to parse
the command output.
This setting might have been changed either  by the user or by some other plugin
to some other value.
To parse the command output using a specific `'efm'`, the plugin can use:

    call setqflist([], 'a', {'id' : qfid, 'lines' : cmdoutput, 'efm' : myefm})

If more than  10 quickfix lists are added  to the stack, then the  oldest qfl is
removed.
When a plugin  is using a qfl, if another  plugin or user adds a new  qfl to the
stack, then there is  a possibility that the qfl that is in  use is removed from
the stack.
So the plugin should check whether the qfl it is using is still valid:

    if getqflist({'id' : qfid}).id == qfid
        " List is still valid
    endif

In summary,  a plugin can  use the following  steps to asynchronously  process a
command output and update a qfl:

   1. Create an empty quickfix list:

        call setqflist([], ' ', {'title' : 'Output from command abc'})

   2. Save the newly created quickfix list identifier:

        let qfid = getqflist({'id' : 0}).id

   3. Start a command in the background using `job_start()`

   4. In the job callback function, check if the quickfix list is still present:

        if getqflist({'id' : qfid}).id == qfid
            " Still present
            " Update the list
        else
            " List is removed. Stop the background job.
            call job_stop(....)
        endif

   5. Process the command output and update the quickfix list using one of the
      following calls:

        call setqflist([], 'a', {'id' : qfid, 'lines' : cmdoutput, 'efm' : myefm})

      or

        call setqflist([], 'a', {'id' : qfid, 'items' : newitems})

##
# async

Normalize async job control api for vim and neovim.

<https://github.com/prabirshrestha/async.vim>

204 sloc

# asyncmake

Plugin for asynchronously running make

<https://github.com/yegappan/asyncmake>

To start make in the background, run the following command:

    :AsyncMake

This invokes the program set in the 'makeprg' option in the background.
The results are processed and added to a quickfix list.
Only one instance of the make command can be run in the background at a time.
Arguments passed to  the ":AsyncMake" command will be passed  on to the external
make command:

    :AsyncMake -f SomeMake.mak

To display the  status of the currently running make  command, use the following
command:

    :AsyncMakeShow

To cancel the currently running make command, use the following command:

    :AsyncMakeStop

When a make is running in the background, if you quit Vim, then the make process
will be terminated.

The output from the make command is added to a quickfix list.
You can use the quickfix commands to browse the output.
If  the make  command exits  with an  error code,  then the  quickfix window  is
automatically opened.

# autoread

Use `$ tail -f` on a buffer and append new content.

This plugin uses Vim 8 async jobs to append new buffer content.

Internally, it  works by running `$  tail -f` on a  file and the output  will be
appended to the buffer, which displays this buffer.

<https://github.com/chrisbra/vim-autoread>

141 sloc

# makejob

This is a plugin  for folks who think that Vim's quickfix  feature is great, but
who don't like how calls to :make and :grep freeze the editor.
MakeJob implements  asynchronous versions of  the builtin commands in  just over
150 lines of Vimscript.

<https://github.com/djmoch/vim-makejob>

208 sloc

