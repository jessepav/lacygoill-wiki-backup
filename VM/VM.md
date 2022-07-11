# How do I know whether the guest system is capturing the host keyboard and mouse?

Look for  two icons on the  right-hand-side of the bar  at the bottom of  the VM
window,  one  representing a  mouse,  the  other  containing an  arrow  pointing
downward.

If the mouse is grayed out, the mouse is not captured.
If the downward arrow is not lit up in green, the keyboard is not captured.

# How to change the Host key?

From CLI:

    $ vboxmanage setextradata global 'GUI/Input/HostKeyCombination' 65515
                                                                    ^---^
                                                                    decimal scancode of Left Windows Key

Source: <https://forums.virtualbox.org/viewtopic.php?f=22&t=95318#p461161>

---

From GUI:

    File (button in menu bar)
    > Preferences (button in dropdown menu)
    > Input (tab in left vertical bar)
    > Virtual Machine (right tab)
    > Host Key Combination:
        double click on the right cell: "Shortcut"
        press new key
        click "OK" button

---

The resulting setting is saved in `~/.config/VirtualBox/VirtualBox.xml`:

    $ grep 'HostKeyCombination' ~/.config/VirtualBox/VirtualBox.xml
    <ExtraDataItem name="GUI/Input/HostKeyCombination" value="65515"/>
                                                              ^---^

## How to get the decimal scancode of the new key?

    $ xev \
        | grep --after-context=2 --line-buffered '^KeyPress' \
        | sed -n '/keycode /s/^.*(keysym \(0x[^,]*\), \(.*\)).*$/\2  \1/p'

    # press: Windows Left key
    Super_L  0xffeb
               ^--^

                               v--v
    $ echo "ibase=16; obase=A; FFEB" | bc
    65515

---

Simpler alternative:

    $ xev-terse
      ^-------^
      custom fish shell function in: ~/.config/fish/functions/xev-terse.fish

    # press: Windows Left key
    Super_L  0xffeb  133
               ^--^

                                       v--v
    $ convert-base --from=hex --to=dec ffeb
      ^----------^
      custom fish shell function in: ~/.config/fish/functions/convert-base.fish

##
# How to access the host's loopback interface from a VM?

Same as on the host, but instead of using the IP address `127.0.0.1`, use `10.0.2.2`.

## How is it useful?

This  lets  you access  any  network  service  running  on the  host's  loopback
interface, from the VM.

For example, you  could run a web  application under development in  the VM, and
the database server on the loopback interface on the host.

##
# How to install a VM?

Use our `vm-install` script:
<https://github.com/lacygoill/config/blob/master/bin/vm-install>

##
# VM Usage
## Where can I find
### some documentation about VirtualBox?

Use our custom `doc` fish function:

    $ doc virtualbox installation
    $ doc virtualbox user-manual

Press tab after `doc virtualbox` to possibly get more topics suggested.

It's defined in `~/.config/fish/functions/doc.fish`.

### some useful key bindings to interact with a VM?

Read:

    ~/wiki/cheat40/virtualbox

### some useful shell commands to interact with a VM?

See our cheat sheets:

    ~/.local/share/navi/cheats/mine/vm.cheat

To read them with a better highlighting, use our Vim syntax plugin:

    ~/.vim/pack/mine/opt/cheat/syntax/cheat.vim

And our `C-g  C-g` fish key binding  to pass those cheat sheets  to `fzf(1)` and
[navi][1].  The key binding is defined here:

    ~/.config/fish/config.fish

It calls this function:

    ~/.config/fish/functions/cheat-sheets.fish

##
## Why should I clone a freshly installed VM?

It can save a lot of time.

After installing  the OS, and  doing a system update  on the guest,  don't start
working on the VM itself.  First, clone it.  Then, work on the cloned VM.

You can  view the first  VM as  a "template", which  can be used  to instantiate
other VMs.

This way,  you don't need  to re-install the system  whenever you need  to start
working from a fresh system.

## Why should I avoid the `reset`, `poweroff`, `acpipowerbutton` subcommands to restart/shutdown the VM?

    $ vboxmanage controlvm <vmname> {reset|poweroff|acpipowerbutton}

`reset` is equivalent to pressing the reset button on your PC.
`poweroff` is equivalent to pulling the power cable on your PC.
`acpipowerbutton` is equivalent to pressing the power button on your PC.

They can all make you lose data in the VM.

##
## What's the current snapshot?

The snapshot from which the current state of the VM is derived.

If you create a snapshot, it becomes  the current snapshot, as well as the child
of the previous snapshot.

##
## How to transfer an existing VM from the local machine to a remote one?

On the local machine:

    # export the VM to an .ova file
    $ vboxmanage export <vmname> --output=<exported>.ova [--description=<description info>]
                                                         ^--------------------------------^
                                                         can be used to record details about the VM
                                                         in a way which is meaningful for the user

    # copy the .ova file to the remote machine
    $ scp <exported>.ova <user>@<IP>:

On the remote machine:

    $ cd
    # import the transferred file into VirtualBox
    $ vboxmanage import <exported>.ova
    $ rm <exported>.ova

    # find out the name of the host network interface
    $ ip addr show | awk '/inet.*brd/ { print $NF; exit }'

    # configure the network of the VM
    $ vboxmanage modifyvm <vmname> --nic1=bridged --bridgeadapter1=<host_network_interface>

    # start the VM
    $ vboxmanage startvm <vmname>

### How to change the way the VM is imported?

Before importing the `.ova` file, use the `--dry-run` option.
It should print:

   - a description of the appliance's contents
   - how it would be imported into VirtualBox, as a list of numbered items
   - how to change the way it will be imported (via command-line options for each item)

Example of output:

    0: Suggested OS type: "RedHat_64"
       (change with "--vsys 0 --ostype <type>"; use "list ostypes" to list all possible values)
    1: Suggested VM name "alma 1"
       (change with "--vsys 0 --vmname <name>")
    2: Suggested VM group "/"
       (change with "--vsys 0 --group <group>")
    ...

Then, run `$ vboxmanage import` again, without `--dry-run`, and with the desired
combination of the suggested command-line options.  For example:

    $ vboxmanage import WindowsXp.ova \
        --vsys=0 --unit=8 --ignore --unit=9 --ignore --unit=14 --controller=13

   - `--vsys=0`: specify the VM whose configuration needs to be changed
     (the appliance could contain several)

   - `--unit=8 --ignore`: disable whatever is described in item 8
   - `--unit=9 --ignore`: disable whatever is described in item 9

   - `--unit=14 --controller=13`: change whatever is described in item 14 (possibly a hard disk image),
     so that it's connected to the controller described in the item 13

For more info, see:
<https://www.virtualbox.org/manual/ch08.html#vboxmanage-import-ovf>

##
# Pitfalls
## I can download an ISO with 3 different types: `boot`, `minimal`, `dvd`.  I don't know what to choose!

Choose the `minimal` one.  It's the best compromise.

The  `dvd` one  is too  big, and  you probably  don't need  all the  packages it
contains.
The  `boot` one  is too  small; every  time  you install  a VM,  you'll need  to
download packages just to get a basic system, which takes valuable time.

Note that if you use a torrent, it might contain all types of ISOs (e.g. `dvd` +
`minimal` + `boot`).  You don't need all of them; to speed up the process, limit
the download to the type you want.

For a real example where you can find these 3 types of ISOs, visit:
<http://mirror.crexio.com/almalinux/9.0/isos/x86_64/>

##
## I can't move the mouse outside the VM window!

That's because it has been captured by the guest.
Press Host to "free" the mouse, then try again to move it outside the VM.

For a permanent solution, install the Guest Additions.

## I can't Alt-Tab from the VM window to another window in the host!

Again, press Host, then try again.

---

To prevent the *automatic* capture of the host keyboard by the guest system, run this:

    $ vboxmanage setextradata global 'GUI/Input/AutoCapture' false

Note that you can still manually capture the host keyboard, by pressing the Host
key.  And if you do, you'll need to press it again to free the keyboard.

## I can't resize the window of a program inside the guest using Alt+Mouse motion!

That's because this particular chord is intercepted by the virtualbox window itself.

Workaround: Don't use the Alt modifier.

Position  the  mouse pointer  near  a  border/corner,  until its  shape  changes
indicating that it can be used to move the border/corner.
Then, while  maintaining the left-click  pressed, move  the mouse to  change the
window's size as desired.

##
## I need to configure some setting from the command-line.  I don't know its name, nor the values it can take!

    $ vboxmanage modifyvm | grep -i '<keyword>'

Replace `<keyword>`  with whatever keyword  you think  should be present  in the
option name.  Like `nic` for a network setting.

## I need to access the VM settings, from the GUI, while it's shut down.  But when I shut it down, VirtualBox is closed!

Start VirtualBox like this:

    $ virtualbox & disown

## I can't restore my snapshot!

Shut down the VM first.

## I can't configure some setting of my VM from the GUI.  It's grayed out!

Saving the state of your VM is not enough:

    $ vboxmanage controlvm <vmname> savestate

Even though it closes the VM window.

You must shut it down completely:

    $ systemctl poweroff

## I've got errors when I execute a command, due to a file not being found!

If an argument of your command is a filepath, and it contains a tilde, expand it
manually.  Only the shell can expand it automatically; not VirtualBox.
And the shell can't expand it if:

   - the path is quoted

         $ vboxmanage ...  --hostpath '~/.../file'
                                      ^          ^

   - the path is in the middle of a word

                           from the shell's point of view, that's a single word
                           v-------------------v
         $ vboxmanage ...  --hostpath=~/.../file
                                     ^
                                     because of this equal assignment,
                                     the shell does not see the path as a whole word;
                                     it's in the middle of a bigger word

## I get a black screen after logging in!

Reboot the system, and in the GRUB menu, choose an entry with the word "rescue".
From there, try to fix whatever is broken.

##
## When I update my system, I have an error msg: “The following signatures were invalid: BADSIG ...”!

    $ sudo rm /var/lib/apt/lists/*
    $ sudo rm /var/lib/apt/lists/partial/*
    $ sudo apt clean
    $ sudo apt update

## The guest refuses to boot:  “This kernel requires the following features not present on the cpu: pae”

    Host+s
    > System
    > Processor
    > tick “enable PAE/NX”

Pressing  Host+s  is  equivalent  to  selecting  “Machine”  in  the  virtual
machine's menu bar, then entering the Settings menu.

##
## I want to virtualize a 32 bits system!

Go into your BIOS settings, and enable CPU virtualization:

   - Intel Virtualization Technology (VT-x)
   - ???                             (AMD-V)

## VirtualBox crashed!

It  has probably  written  a logfile  in  your home  directory,  or in  whatever
directory you were when you started it.  Find it and read it.

##
## Do I need to install DKMS?

No.

In the past, VirtualBox did need DKMS (Dynamic Kernel Module Support) to rebuild
its kernel modules whenever the kernel was upgraded:

   > Technical note: VirtualBox does not use dkms, but installing it also
   > installs the software needed to build the drivers.

Source: <https://www.virtualbox.org/wiki/LinuxAdditionsDebug>

   > DKMS is a framework designed to allow individual kernel modules to be upgraded
   > without changing the whole kernel. It is also very easy to rebuild modules as
   > you upgrade kernels.

Source: `$ apt show dkms | grep --after-context=3 Description`

But it was not reliable enough:
<https://www.virtualbox.org/ticket/7536>

Since VirtualBox 5.1.0, DKMS is no longer necessary:

   > Linux installers: no longer rely on DKMS for module rebuilding

Source: <https://www.virtualbox.org/wiki/Changelog-5.1>

It's not even mentioned once in the current user manual for VirtualBox 6.1.34.

---

I think that's only true if you install VirtualBox from upstream (e.g. via PPA).
If  you   install  it   from  your  Linux   distribution  default   repos  (e.g.
via  `apt(8)`),  then  you  might  need  some  DKMS-related  packages,  such  as
`virtualbox-dkms` on the host, and `virtualbox-guest-dkms` on the guest:

   > On Ubuntu hosts, the Ubuntu-provided virtualbox package
   > needs the virtualbox-dkms package to build the VirtualBox
   > host-side kernel modules. In Ubuntu guests, the Ubuntu-provided
   > virtualbox-guest-additions-iso package needs the virtualbox-guest-dkms
   > package to build the VirtualBox guest-side kernel modules.

Source: <https://forums.virtualbox.org/viewtopic.php?f=7&t=104808&p=511194&hilit=dkms#p511194>

But VirtualBox is too important (and too  complex already) for us to deal with a
modified version.  Let's stick to upstream.

---

You might still need DKMS if you have a DKMS module installed.
You can check this with:

    $ dkms status

Or:

    $ ls /var/lib/dkms

See: <https://askubuntu.com/a/653632>

##
# Todo
## Why does `guestcontrol <vmname> run --exe='/path/to/cmd'` fail?

    $ vboxmanage guestcontrol fedora run \
        --username=toto \
        --password=beebee \
        --verbose \
        --putenv PWD=/run/media/toto/VBox_GAs_6.1.34 \
        --exe='/bin/sudo' \
        -- /bin/sh ./VBoxLinuxAdditions.run

Doesn't work.  Try 1 (while VM still at login screen):

    Creating guest session as user 'toto'...
    Waiting for guest session to start...
    VBoxManage: error: Error starting guest session (current status is: terminated)
    Closing guest session ...

Try 2:

    Creating guest session as user 'toto'...
    Waiting for guest session to start...
    VBoxManage: error: Waiting for guest process failed: VERR_DUPLICATE
    VBoxManage: error: Details: code VBOX_E_IPRT_ERROR (0x80bb0005), component GuestSessionWrap, interface IGuestSession, callee nsISupports
    VBoxManage: error: Context: "WaitForArray(ComSafeArrayAsInParam(aSessionWaitFlags), 30 * 1000, &enmWaitResult)" at line 891 of file VBoxManageGuestCtrl.cpp
    Closing guest session ...

Why?

Even a simple `/bin/ls` fails:

    $ vboxmanage guestcontrol fedora run \
        --username=toto \
        --password=beebee \
        --exe='/bin/ls'

And yet, according to this link, it should work:
<https://askubuntu.com/a/908137>
What gives?

## Read chapter 7 of the user manual to learn how to run a VM on a remote server

<https://www.virtualbox.org/manual/ch07.html>

This would be useful to avoid consuming resources on our local machine.
The chapter also explains how to secure the communication between the client and
the server.

## Document how to allow the VM to access a USB device from the host

First, you must ask VirtualBox to present a virtual USB controller to the guest.
Next, you must tell VirtualBox which USB device the VM can access.

Document a way to do that in CLI.
Use that info to update our `vm-install` script.

---

In GUI, this is a two-step process.

Step 1:

    right-click on the VM (it must be shut down)
    > Settings
    > USB

Make sure that the following boxes are ticked:

   - Enable USB Controller
   - Enable USB 2.0 (EHCI) Controller

Step 2:

To add a  new filter, click on the  first icon (USB plug with blue  disk) on the
right, or press INSER.  Then, edit the fields of the filter:

   1. Name   =   arbitrary name given to the filter
   2. Vendor ID
   3. Product ID
   4. Revision
   5. Manufacturer (similar to Vendor ID)
   6. Product (similar to Product ID)
   7. Serial No
   8. Port

Alternatively, you can  display a menu with all the  devices currently connected
to the host by  clicking on the second icon (USB plug with  green plus sign), or
by pressing alt + INSER.
Then, select the device(s) to which you want the VM to have access.

Finally, press OK.

For more info, see:

- <https://www.virtualbox.org/manual/ch03.html#usb-support>
- <https://www.virtualbox.org/manual/ch08.html#vboxmanage-usbcardreader>
- <https://www.virtualbox.org/manual/ch08.html#vboxmanage-usbfilter>

---

Also, document that if  you give to your VM the access to  a USB device, as soon
as you  start your  VM, the  USB device will  be ejected  from the  host without
having been properly unmounted.  Because of this, you might lose data.

Be sure that no USB device is connected  to your machine when you start a VM, or
that the VM can't access the USB device.

##
# Reference

[1]: https://github.com/denisidoro/navi
