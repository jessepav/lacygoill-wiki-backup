# How to
## Get the list of processes opening
### the shared library `/lib/x86_64-linux-gnu/libcrypto.so.1.0.0`?

    $ lsof /lib/x86_64-linux-gnu/libcrypto.so.1.0.0

Useful if you've updated a library and you want all running processes to use the new one.
To do so, you need to know which running processes are still opening the old one.

### files in `~/.vim`

    $ lsof ~/.vim/**/*

Note that the expansion of `**/*` is done by the shell prior to invoking `lsof`.
Also, `**`, which here is understood as a recursive wildcard, is not interpreted
as such by all shells.
It depends on the shell and its configuration.
For example, bash needs this setting:

    shopt -s globstar

##
## Get the list of
### files opened by the Vim process?

    $ lsof -p $(pidof vim)

### files opened by all the firefox processes?

    $ lsof -p $(pidof firefox | tr ' ' ',')

### file descriptors created for the Vim process?

    $ ls [-l] /proc/$(pidof vim)/fd
           │
           └ to see what file they point to

### files opened for the root user?

    $ lsof -u root

##
### opened sockets?

    $ lsof -i

### opened Unix domain sockets?

    $ lsof -i -U

### sockets listening on port 6667?

    $ lsof -i :6667
              │
              └ port specification leader

### sockets connected to the ipv4 1.2.3.4?  to the ipv6 2001:41d0:...?

              ┌ host specification leader
              │
    $ lsof -i @1.2.3.4
    $ lsof -i '@[2001:41d0:...]'
              │
              └ to prevent zsh from interpreting the brackets as a collection:

                  % echo [1]
                   zsh: no matches found: [1]~
                   (zsh tried to find a file named 1)~

### sockets using the tcp protocol?  the udp protocol?

    $ lsof -i tcp
    $ lsof -i udp

### ipv4 sockets opened by the process whose pid is `1234`?

                ┌ AND the list selection options
                ├┐
    $ lsof -i 4 -a -p 1234
           ├──┘    ├─────┘
           │       └ list selection 2
           │
           └ list selection 1

###
## Get the path to the binary from which the Vim process was started?

    $ lsof -p $(pidof vim) | grep txt
                                  │
                                  └ program text (code and data)

Or simpler:

    $ type vim

## Get the paths to the shared libraries used by the Vim process?

    $ lsof -p $(pidof vim) | grep -E '\.so'

## Get the paths to the logfiles used by the WeeChat process?

    $ lsof -p $(pidof weechat) | grep log

##
## Get the pid, and only the pid, of the process opening `some_file`?

    $ lsof -t some_file
            │
            └ terse output with pid only and no header/warning

Useful when you need to unmount a  partition, but you can't because some process
is still accessing a file in it.

##
# Understanding the output
## Where is the line matching the binary file opened to start the Vim process?

Look for the line where the `FD` column has the `txt` value.

## Where are the names of the opened files in the output?

In the last column.

##
## What's the meaning of
### the numbers `0`, `1`, `2` which sometimes are printed in the FD column?

    0 = stdin
    1 = stdout
    2 = stderr

### the letter right afterwards?

It's the mode in which the file is opened.

### 'r', 'w' and 'u'?

    r = read
    w = write
    u = read + write

### `DIR`, `REG`, `CHR`, `unix` in the `TYPE` column?

It represents the type of the opened file:

    ┌──────┬────────────────────────┐
    │ DIR  │ directory              │
    ├──────┼────────────────────────┤
    │ REG  │ regular file           │
    ├──────┼────────────────────────┤
    │ CHR  │ character special file │
    ├──────┼────────────────────────┤
    │ unix │ UNIX domain socket     │
    └──────┴────────────────────────┘

For more info, see:

    man lsof /OUTPUT

##
## What's a socket?

A pseudo-file that represents a network connection.

Writes to a socket  are turned into network packets that get  sent out, and data
received from the network can be read from the socket.

Analogy:

    machine/host = house
    data         = mail
    socket       = mailbox
                   attached to the house,
                   and where you can put your outgoing mail as well as receive mail

Sources:
<https://unix.stackexchange.com/a/193665/289772>
<https://unix.stackexchange.com/a/16323/289772>
<https://unix.stackexchange.com/a/193824/289772>

## What's a Unix domain socket?

It's  common for  programs on  a single  machine to  communicate using  standard
network protocols, such as TCP.
It  would be  wasteful to  go all  the way  to the  network hardware  (if any!),
computing checksums, etc., just to go back to the same host.

That's where a Unix domain socket comes in.
It works like  a regular socket, except  it connects processes on  the same host
rather than remote  processes, and doesn't attempt to use  any network resources
at all.

From this point of view, it's a medium of inter-process communication.

## What does a pipe and a socket have in common?

They both are means of communication.

They both look  like a file to the  programs using it, but they  don't result in
read or writes to a disk.
Rather, they  allow communicating  with another  program (local  in the  case of
pipes, and possibly remote in the case of sockets).

## What's the main difference between a pipe and a socket?

The pipe is a means of **one way** communication.
The socket is a means of **two way** communication.

##
# Misc
## What's the meaning of the characters in the name of the command 'lsof'?

LiSt Open Files.

##
## Why doesn't `lsof ~/.vim/vimrc` output anything?

Vim isn't actually holding the `vimrc` open.
It's reading it into a swapfile and then holding that file open.

Source: <https://unix.stackexchange.com/a/65504/289772>

Although, if  `'swf'` is unset,  it doesn't hold  any file open,  which probably
means that Vim only cares about the  buffer, and opens the file only temporarily
when you write it with `:w` or read it with `:r`.

