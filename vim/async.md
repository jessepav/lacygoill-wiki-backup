# async

            Normalize async job control api for vim and neovim.

            https://github.com/prabirshrestha/async.vim

                                    204 sloc

# asyncmake

            Plugin for asynchronously running make

            https://github.com/yegappan/asyncmake



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

The output from  the make command is  added to a quickfix list. You  can use the
quickfix commands to browse the output. If  the make command exits with an error
code, then the quickfix window is automatically opened.

# autoread

            Use `tail -f` on a buffer and append new content.

            This plugin uses Vim 8 async jobs to append new buffer content.

            Internally, it works by running tail -f on a file and the output will be
            appended to the buffer, which displays this buffer.

            https://github.com/chrisbra/vim-autoread

                                        141 sloc

# makejob

            This is a plugin for folks  who think that Vim's quickfix feature is
            great, but  who don't like how  calls to :make and  :grep freeze the
            editor. MakeJob  implements  asynchronous  versions of  the  builtin
            commands in just over 150 lines of Vimscript.

            https://github.com/djmoch/vim-makejob

                                    208 sloc

