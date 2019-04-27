We should progressively switch to a more simple DE.
There would be several benefits:

   - fewer bugs
   - less memory/cpu consumption
   - more responsive applications
   - better latency in the terminal (?)
   - easier to fix bugs; easier to understand how the OS/shell/systemd/... works (because fewer processes)

---

First, you need to get rid of lightdm.
It's not that lightweight.

Ok, but replace it with what?
Nothing. We don't need a display manager.

Read this:
<https://wiki.gentoo.org/wiki/X_without_Display_Manager>

We should be able to:

   - start our custom DE from a console
   - autologin
   - “attach” different DEs to different consoles
     (e.g. `exec startx` from console1 → custom DE;
     from console2 → lxde;
     from console3 → xfce)

To begin with, we should learn how to disable lightdm.
It may  not be useful later,  if we re-install a  linux distro with a  custom DE
right from  the start; but  who knows, it  may still be  useful if we  install a
common DE as a fallback in case of an issue.
And anyway, right now, we definitely need to disable lightdm before building our DE.

See:
<https://askubuntu.com/questions/882422/how-can-i-disable-all-display-managers>
<https://askubuntu.com/questions/16371/how-do-i-disable-x-at-boot-time-so-that-the-system-boots-in-text-mode/79682#79682>
<https://superuser.com/questions/974797/how-to-boot-a-linux-system-without-graphical-server>

---

Next, we need  to find a replacement for  every basic component of a  DE, like a
screen locker, an app to access system settings, a panel bar, ...
Have a look at  the output of `$ top`, and see what  seems interesting in what's
running.

---

Finally, we need to find a better window manager (WM).
Right now, we use xfwm4 (which is the default for xfce4).
But this is a *compositing* window manager; that kind of WM increases the latency.
We should prefer a *stacking* WM.

Note that stacking vs compositing has nothing to do with floating vs tiling.
Those are orthogonal concepts.

My ideal WM would be the awesome  WM; it's powerful, supports compositing but is
probably stacking by default, and is scriptable with lua.
Check this for a start:
<https://awesomewm.org/apidoc/documentation/07-my-first-awesome.md.html#>
There are other interesting pages in the left sidebar.

But awesome would probably be a timesink right now.
There's an easier WM: **openbox**.
So, for the time being, try to install and configure openbox.

Read: <http://openbox.org/wiki/Help:Getting_started>

---

We should also learn how to reduce latency, and how to better judge a terminal.
<https://anarc.at/blog/2018-05-04-terminal-emulators-2/#latency> (read the first part too)
<https://lwn.net/Articles/751763/> (read the first part too)
<https://pavelfatin.com/typing-with-pleasure/>
<https://pavelfatin.com/typometer/>
<https://github.com/pavelfatin/typometer/issues/2>

We recently have switched from urxvt to st.
I think it was a wise decision for different reasons.
In particular, it has divided the latency by two.
We could gain a few more ms by switching to openbox.
But maybe we could also improve the latency by tweaking `config.h`:

    static unsigned int xfps = 120;
    static unsigned int actionfps = 30;

Try to increase those values, and test the compiled st with typometer.
Does it reduce the latency?
Find other possible options which could help.

Also, maybe we should disable UltiSnips' autotrigger even in Vim.
It may not increase the latency, but it may increase the jitter.

