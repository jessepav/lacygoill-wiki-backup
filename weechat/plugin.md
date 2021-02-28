# What's WeeChat “core”?

The part of WeeChat which, contrary to a plugin, is always loaded.
It's only used to display data on screen and interact with the user.

# Does WeeChat support the IRC protocol without any plugin?

No.

The `irc` plugin needs to be loaded.

# How to list the plugins currently loaded?

    /plugin

# What's the list of (21) default plugins loaded by default, if you've compiled WeeChat with a max of options?

    alias:      Alias commands
    aspell:     Spell checker for input (with Aspell)
    buflist:    Buffers list
    charset:    Charset conversions
    exec:       Execution of external commands in WeeChat
    fifo:       FIFO pipe for remote control
    fset:       Fast set of WeeChat and plugins options
    guile:      Support of scheme scripts (with Guile)
    irc:        IRC (Internet Relay Chat) protocol
    javascript: Support of javascript scripts
    logger:     Log buffers to files
    lua:        Support of lua scripts
    perl:       Support of perl scripts
    php:        Support of PHP scripts
    python:     Support of python scripts
    relay:      Relay WeeChat data to remote application (irc/weechat protocols)
    ruby:       Support of ruby scripts
    script:     Script manager
    tcl:        Support of tcl scripts
    trigger:    Text replacement and command execution on events triggered by WeeChat/plugins
    xfer:       DCC file transfer and direct chat

