# How to start WeeChat without my custom config?

    $ weechat -d /tmp/.weechat
               │
               └ --dir

TODO:  document the  new `-t`  command-line  option, which  creates a  temporary
WeeChat home directory and deletes it on exit.

# How to do a binary search in the config files, to find a problematic line, without affecting the current config?

    $ cp -R ~/.config/weechat/ /tmp/.weechat
    $ weechat --dir /tmp/.weechat/

Now, you  can edit the  files in `/tmp/.weechat/` as  you like; it  won't affect
your config in `~/.config/weechat/`.

##
# How to compile WeeChat locally, without installing it?

    $ rm -rf build ; \
      mkdir -p build && cd build ; \
      cmake .. \
        -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
        -DWEECHAT_HOME:STRING="${HOME}/.config/weechat" \
        -DENABLE_PYTHON2:BOOL=ON \
        -DENABLE_MAN:BOOL=ON \
        -DENABLE_TESTS:BOOL=ON ; \
      make

## Then, how to run the local binary?

    $ ./src/gui/curses/normal/weechat -d /tmp/.weechat

### When I'm running it, it complains about some libraries!

    Error: API mismatch for plugin "/usr/local/lib/weechat/plugins/xfer.so" (current API: "20190615-01",~
    plugin API: "20190624-01"), failed to load~
    If plugin "xfer" is old/obsolete, you can delete this file.~

The local binary may use some libraries from the installed WeeChat package.
If that's an  issue, don't just run  the compiled binary; install it  first as a
deb package.

---

TODO: Find a way to make the compiled binary use the compiled libraries.

Here's  how you  can copy  all the  compiled libraries  in the  temporary config
directory:

    $ cd build/src
    $ fd -I '.so$' | xargs -I{} rsync -ahPuzR --stats {} /tmp/.weechat

This should work according to:

> Copy   file    toto.so   into   system   plugins    directory   (for   example
> /usr/local/lib/weechat/plugins)  **or  into  user's plugins  directory**  (for
> example **/home/xxx/.weechat/plugins**).

<https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#load_plugin>

The problem is that WeeChat still first looks at the libraries in `/usr/local/lib`.

This is an issue, for example, if you try to compile WeeChat on this commit:

    $ git checkout f15a24b2ec14e279d15bd509be79176ee3c4d5c9

##
# WeeChat just crashed. What should I do to help the developers fix the bug?

Before going further, try to reproduce the crash with no scripts:

    /script list
    /script unload <script> ...

If you find out that the crash is due to a script, report it here:
<https://github.com/weechat/scripts/issues>

---

Inside  the  shell working  directory,  the  OS has  created  a  file `core`  or
`core.12345` (12345 being the process id).

Execute:

    $ gdb /usr/bin/weechat /path/to/core_file

Then under `$ gdb`, execute the following commands:

    # write the output of the next commands in a file
    (gdb) set logging on

    # display a backtrace
    (gdb) bt full

    (gdb) quit

The output of these commands should look like this:

    (gdb) set logging on
    Copying output to gdb.txt.
    (gdb) bt full
    #0  0x00007f9dfb04a465 in raise () from /lib/libc.so.6
    #1  0x00007f9dfb04b8e6 in abort () from /lib/libc.so.6
    #2  0x0000000000437f66 in weechat_shutdown (return_code=1, crash=1)
        at /some_path/src/core/weechat.c:351
    #3  <signal handler called>
    #4  0x000000000044cb24 in hook_process_timer_cb (arg_hook_process=0x254eb90,
        remaining_calls=<value optimized out>) at /some_path/src/core/wee-hook.c:1364
            hook_process = 0x254eb90
            status = <value optimized out>
    #5  0x000000000044cc7d in hook_timer_exec ()
        at /some_path/src/core/wee-hook.c:1025
            tv_time = {tv_sec = 1272693881, tv_usec = 212665}
            ptr_hook = 0x2811f40
            next_hook = 0x0
    #6  0x000000000041b5b0 in gui_main_loop ()
        at /some_path/src/gui/curses/gui-curses-main.c:319
            hook_fd_keyboard = 0x173b600
            tv_timeout = {tv_sec = 0, tv_usec = 0}
            read_fds = {fds_bits = {0 <repeats 16 times>}}
            write_fds = {fds_bits = {0 <repeats 16 times>}}
            except_fds = {fds_bits = {0 <repeats 16 times>}}
            max_fd = <value optimized out>

You must report the contents of `gdb.txt`  to the developers, and tell them what
action caused the crash.

To write your report, follow the instructions here:
<https://github.com/weechat/weechat/blob/master/Contributing.adoc>

# How to debug a running WeeChat?

    $ gdb /usr/bin/weechat 12345
                           │
                           └ pid of WeeChat

Then like for a crash, use the gdb command `bt full`:

    (gdb) bt full

