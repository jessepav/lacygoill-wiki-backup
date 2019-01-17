# How to start WeeChat without my custom config?

        $ weechat -d /tmp/.weechat
                   │
                   └ --dir

# WeeChat just crashed. What should I do to help the developers fix the bug?

Before going further, try to reproduce the crash with no scripts:

        /script list
        /script unload <script> ...

If you find out that the crash is due to a script, report it here:

        https://github.com/weechat/scripts/issues

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

        https://github.com/weechat/weechat/blob/master/Contributing.adoc

# How to debug a running WeeChat?

        $ gdb /usr/bin/weechat 12345
                               │
                               └ pid of WeeChat

Then like for a crash, use the gdb command `bt full`:

        (gdb) bt full

# How to do a binary search in the config files, to find a problematic line, without affecting the current config?

        $ cp -R ~/.config/weechat/ /tmp/.weechat
        $ weechat --dir /tmp/.weechat/

Now, you  can edit the  files in `/tmp/.weechat/` as  you like; it  won't affect
your config in `~/.config/weechat/`.

