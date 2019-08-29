# `VT_ACTIVATE`

Switching  virtual   terminals  is  usually   done  by  the  user   by  pressing
[Ctrl+]Alt+Fn, but it can also be  triggered in software using either chvt(1) or
the Linux-specific system call `ioctl(ttyfd, VT_ACTIVATE, num)`.

Here, `num` is the number of the virtual terminal you wish to switch to, and the
`ttyfd` argument must be a valid file descriptor to a terminal.

Now, you might ask, what terminal device does `ttyfd` have to refer to?
Shouldn't this system  call only care about  one terminal, that is,  the one you
want to switch to?
Well, based on tests I've run, the  terminal device to which `ttyfd` refers must
be either  one of the numbered  virtual terminals (such as  the currently active
one, or the one you want to switch to) or the system console, `/dev/console`.
It will  not work if  you use  a pseudoterminal or  one of the  serial consoles,
`/dev/ttyS*`.

