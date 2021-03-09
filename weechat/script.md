# What's the difference between a plugin and a script?

A plugin is a BINARY file compiled and loaded with the `/plugin` command.

A script is a  TEXT file loaded with a plugin, such as  python via the `/python`
command.

# Where should I put a new python script?

In `~/.config/weechat/python/`.

# How to autoload a python script?

Create a symlink  in the `autoload/` subdirectory pointing to  the script in the
parent directory.

    $ cd ~/.config/weechat/python/autoload/
    $ ln -s ../my_script.py

##
# What are the two commands which I can use to handle my python scripts?

    /python
    /script

# Which one should I prefer and why?

    /script

It will  automatically detect the language  in which the script  is written, and
call the appropriate plugin to load it.

##
# How to manually load a script?   How to reload it?   How to unload it?

    /script load    my_script.py
    /script reload  my_script.py
    /script unload  my_script.py

# How to list all the scripts currently loaded?   Only the python scripts?

    /script list
    /python list

##

# python script
## Which module must I import at the beginning of any script?

    weechat

## How do I call the built-in function `foo()` provided by WeeChat?

    weechat.foo(arg1, arg2, ...)

## What are the three functions whose name is different in python compared to other scripting languages?   Why?

    weechat.prnt()

---

    # Display a message on a buffer, using a custom date and tags.
    # https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_printf_date_tags

    weechat.prnt_date_tags()

---

    # Display a message on a line of a buffer with free content.
    # https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_printf_y

    weechat.prnt_y()

---

They are different because `print` is a reserved keyword in python.

## What's the first function my script must call?

Your script must register itself to WeeChat, by invoking `weechat.register()`.

Prototype:

    weechat.register(
        name,
        author,
        version,
        license,
        description,
        shutdown_function,
        charset
    )

The `shutdown_function`  argument is the  name of  the function called  when the
script is unloaded.

Example:

    weechat.register('test_python', 'nicsig', '1.0', 'GPL3', 'Test script', '', '')

## How do I get the value of a string option?

                                  ┌ return a pointer
                                  │
    weechat.config_string(weechat.config_get('file.section.option'))
            │
            └ you need this function to convert the pointer into a string

## How do I execute a WeeChat command?

    weechat.command('', '/your command')
                    │
                    └ name of the buffer where the command must be executed;
                      an empty string matches the current buffer:

   > name of buffer, if it is NULL  or empty string, the current buffer is returned
   > (buffer displayed by current window)

Source: <https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_buffer_search>

## How do I install a custom command?

    weechat.hook_command(
        'my_cmd',
        '',
        '',
        '',
        '',
        'func',
        '',
    )

    def func(data, buffer, args):
        # ...
        return weechat.WEECHAT_RC_OK

---

For more info:

   - <https://weechat.org/files/doc/stable/weechat_scripting.en.html#hook_command>
   - <https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_hook_command>

