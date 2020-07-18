# What's VB?

An abbreviation which I use in place of 'virtualbox'.

# What's VM?

An abbreviation which I use in place of 'virtual machine'.

##
# Where is the manual for VB?

<https://www.virtualbox.org/manual/>

In particular, the chapter 8 describes the command-line interface:

<https://www.virtualbox.org/manual/ch08.html>

##
# Host configuration
## Where is the VB installation procedure described?

<https://www.virtualbox.org/wiki/Linux_Downloads>

##
## How to add a repository to get a more up-to-date VB package?

    $ sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/virtualbox.list
    # repository to have a more up-to-date virtualbox package
    deb http://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib
    EOF'

## How to check the authenticity of this new repository?

    $ curl -Ls https://www.virtualbox.org/download/oracle_vbox_2016.asc >key.asc

    $ key_check key.asc '...'
      │
      └ custom function in `~/.zshrc`

The first command downloads the key of the repository.
The second command makes sure that it belongs to the owner of the repository.

---

Note that you must replace '...' with the fingerprint found on the download page:

<https://www.virtualbox.org/wiki/Linux_Downloads>

Here's an example of fingerprint:

    B9F8 D658 297A F3EF C18D  5CDF A2F6 83C5 2980 AECF

## How to add the key of the repository to my list of trusted keys?

    $ sudo apt-key add key.asc

## How to install the most recent VB package?

    $ aptitude search virtualbox | grep -E '[0-9]\.[0-9]'
    $ aptitude update && aptitude install virtualbox-x.y
                                                     ^-^
    replace with the values found in the previous command

---

During the installation, you'll read some interesting messages:

>     ureadahead will be reprofiled on next reboot
>     Adding group `vboxusers' (GID 131) ...

## Why should I install `dkms`?

    $ sudo aptitude install dkms

Because VB relies on some (host) kernel modules:

   - vboxdrv
   - vboxnetadp
   - vboxnetflt

And they need to be updated each time the host kernel is updated.

##
## What's the extension pack?

An optional pack of extensions which adds some features to VB:

   - Disk Encryption
   - Host Webcam
   - NVMe
   - PXE ROM
   - USB 2.0 and USB 3.0 Host Controller
   - VirtualBox RDP (Remote Desktop Protocol)

## Where can I download it?

<http://download.virtualbox.org/virtualbox/>

To enter the right directory, execute:

    $ aptitude show virtualbox-x.y
    x.y.ab-cdefgh~
        ^^
    # Enter the directory `x.y.ab`

Then,  download the  file whose  extension  is `.vbox-extpack`,  and whose  name
includes `cdefgh`.

## How to install it?

                                 ┌ directory where firefox has downloaded the pack
                                 ├─────────────────┐
    $ vboxmanage extpack install /tmp/mozilla_user0/Oracle_VM_VirtualBox_Extension_Pack-5.1.22-115126.vbox-extpack
                                                    │
                                                    └ name of the downloaded file

## How to uninstall it?

    $ vboxmanage extpack uninstall 'Oracle VM VirtualBox Extension Pack'
                                    │
                                    └ name of the extension pack as it was installed
                                      and as reported by `VBoxManage list extpacks`

## How to list the extension packs currently installed?

    $ vboxmanage list extpacks

Lister les packs d'extensions actuellement installés.

## Where can I find more info on how to manage my extension pack from the command-line?

<https://www.virtualbox.org/manual/ch08.html#vboxmanage-extpack>

##
## How to list all the types of supported guests OS?

    $ vboxmanage list ostypes

## What to do if only 32 bits OS are supported?

Si seuls  des OS  32 bits sont  listés, se  rendre dans le  BIOS, et  chercher à
activer une technologie de virtualisation du cpu:

Go into your BIOS settings, and enable CPU virtualization:

   - Intel Virtualization Technology (VT-x)
   - ???                             (AMD-V)

## Where will VB create my virtual machines?

    ~/VirtualBox VMs

## How to change this location to `~/VB/`?

    $ vboxmanage setproperty machinefolder ~/VB

##
# Creation of a VM
## How to create a virtual machine named 'ubuntu'?

    $ vboxmanage createvm --name ubuntu --ostype Ubuntu_64 --register

### Why should I use the `--ostype` option of the `createvm` subcommand?

It makes VB automatically select default values for some options of the VM (ram,
nic), which are well-suited.

### Which value can I give to `--ostype`?

    $ vboxmanage list ostypes | grep -Ei '^id:'

### What are the 3 files/directories created/modified after the previous command?

   - ~/VB/ubuntu/ is created (VM directory)

   - ~/VB/ubuntu/ubuntu.vbox is created (VM config)

   - ~/.config/VirtualBox/VirtualBox.xml is modified (VB config)
      an entry is added for the new VM

### What's the effect of the `--register` option of the `createvm` subcommand?

Without `--register`, the VM is not available in the GUI, and it's not listed by
`vboxmanage list vms`.

### What's the subcommand equivalent to `createvm --register`?

    registervm

### How could I have used it to create the VM?

    $ vboxmanage createvm --name ubuntu
    $ vboxmanage registervm ~/VB/ubuntu/ubuntu.vbox
                            │
                            └ VM config file

###

## How to give 1 gig of ram to the VM?

    $ vboxmanage modifyvm ubuntu --memory 1024

## Do I need to give more ram to the VM's graphic card?

If you want to make the VM window enter fullscreen, then yes.
By default, it only has 8 Mo which is not enough.

If you don't care about fullscreen, then no.

### How to give it more ram?

    $ vboxmanage modifyvm ubuntu --memory 1024 --vram 128
                                               ^--------^

##
## How to add an IDE controller to the VM?

    $ vboxmanage storagectl ubuntu --name 'IDE controller' --add ide
                                           │               │
                                           │               └ type of the system bus to which
                                           │                 the storage controller must be connected
                                           └ arbitrary name

### How to rename it?

    $ vboxmanage storagectl ubuntu --name 'IDE controller' --rename 'Other name'
                                                           ^-------------------^

### How to remove it?

    $ vboxmanage storagectl ubuntu --name 'IDE controller' --remove
                                                           ^------^

##
## How to use my ISO file as a disk inserted in the dvd drive of the VM?

    $ vboxmanage storageattach ubuntu \          # name of the VM
               --storagectl 'IDE controller' \   # name of the storage controller to which we attach our iso
               --port 0 --device 0 \             # n° of the port on the storage controller, and n° of the device
               --type dvddrive \                 # type of the hardware to which the iso is attached
               --medium /path/to/iso             # path to the iso

---

Why `--port 0`?

It seems that a storage controller can have several ports.
So, you must specify which port on the controller your dvd drive is connected to.

Why `--device 0`?

It seems that an IDE controller can have 2 devices per port (master and slave).

### Which values can take `--type`?

Usually, one of these:

   - dvddrive
   - hdd

### Which values can take `--medium`?

    ┌───────────────────┬────────────────────────────────────────────────────────────┐
    │ 'none'            │ the device is removed (dvd drive, hard drive, ...)         │
    ├───────────────────┼────────────────────────────────────────────────────────────┤
    │ 'emptydrive'      │ the medium is removed (cd, dvd, floppy disk)               │
    ├───────────────────┼────────────────────────────────────────────────────────────┤
    │ 'additions'       │ attach the Guests Additions                                │
    ├───────────────────┼────────────────────────────────────────────────────────────┤
    │ a UUID            │ attach a medium known by VB (because used in another VM)   │
    ├───────────────────┼────────────────────────────────────────────────────────────┤
    │ a filepath        │ attach a medium stored in a file                           │
    └───────────────────┴────────────────────────────────────────────────────────────┘

### What's the difference between storage device and storage medium?

A storage device is a hardware emulated by VB for a VM.

A storage medium is  a file on the host system, which VB  uses to store the data
of an emulated storage device.
The latter could be a dvd disk, or a hard drive disk.

##
## How to add a 10G hard drive to the VM?

    $ vboxmanage createmedium --filename ~/VB/ubuntu/ubuntu.vdi --size 10000
                                         │
                                         └ path to the file used by VB
                                           to emulate the hard drive

    $ vboxmanage storagectl ubuntu --name 'SATA controller' --add sata

    $ vboxmanage storageattach ubuntu \
                 --storagectl 'SATA controller' \
                 --port 0 --device 0 \
                 --type hdd \
                 --medium ~/VB/ubuntu/ubuntu.vdi

---

From the guest point of view, the hard drive has a capacity of 10G.

But from the host point of view, initially, `ubuntu.vdi` only takes 2M.
Later, when  you'll create files  in the guest  OS, `ubuntu.vdi` will  grow, but
never beyond 10G.

That's why the official documentation uses the term “dynamically allocated file”:

<https://www.virtualbox.org/manual/ch01.html>

## How to make the VM boot from the dvd drive, then from the hard disk?

    $ vboxmanage modifyvm ubuntu --boot1 dvd --boot2 disk --boot3 none --boot4 none

By default, a VM tries to boot from:

   1. a floppy disk
   2. a DVD
   3. a hard drive

##
## How to attach the NIC of the VM to the `enp3s0` interface of the NIC of our host machine?

    $ vboxmanage modifyvm ubuntu --nic1 bridged --bridgeadapter1 enp3s0
                                      │ │         │              │
                                      │ │         │              └ you may need to modify the name
                                      │ │         │                of the interface (see `ifconfig(8)`)
                                      │ │         │
                                      │ │         └ specify which host interface the virtual network interface
                                      │ │           will use
                                      │ │
                                      │ └ type of networking which should be avalaible
                                      │
                                      └ id of the NIC (several could be attached to the VM)

This will allow the VM to connect to the local network, and thus to internet.

The VM will receive  its IP from the local DHCP server  (which typically runs on
your box).

---

Note that NIC stands for Network Interface Controller.

## How to specify which networking hardware VB should presented to the guest?

    $ vboxmanage modifyvm ubuntu --nictype1 'hardware'

By default, the chosen hardware for an Ubuntu/Debian VM is:

    Intel PRO/1000 MT Desktop (82540EM)

---

Atm, it could be  useful to change to either of:

   - `PCnet-PCI II (Am79C970A)`
   - `PCnet-FAST III (Am79C973)`

to be protected from a 0day vulnerability which allows:

>     an attacker with root/administrator privileges in  a guest to escape to a host
>     ring3.
>     Then the attacker  can use existing techniques to escalate  privileges to ring 0
>     via /dev/vboxdrv.

<https://github.com/MorteNoir1/virtualbox_e1000_0day#how-to-protect-yourself>

To do so, you could execute:

    $ vboxmanage modifyvm ubuntu --nictype1 'Am79C973'

Or, you could use the GUI:

   1. Shut down the VM.
   2. Start VB alone: `% virtualbox &!`
   3. Select the VM.
   4. Settings
   5. Network
   6. Advanced
   7. Adapter Type
   8. Select the desired type
   9. OK

However, it seems to break the network.
You can't reach any host with `Am79C973` atm...

###
# Configuration of a VM
## OS Post Install
### How to eject the disk from the VM?

In CLI:

    $ vboxmanage storageattach ubuntu \
                 --storagectl 'IDE controller' \
                 --port 0 --device 0 \
                 --medium 'emptydrive'

In GUI:

      Devices
    > Optical Drives
    > Remove disk from virtual drive

---

Notice that you can  omit `--type`, because VB is able to guess  the type of the
storage medium from the config of the VM.

---

You should eject the disk right after installing the OS of the VM.
It may prevent the Guest Additions ISO file from being mounted.

###
### How to install the Guest Additions from the guest OS Ubuntu?

From the guest OS:

    $ sudo aptitude update && sudo aptitude safe-upgrade
    $ sudo aptitude install dkms
    $ sudo systemctl reboot

    # mount the Guest Additions ISO file inside the VM:
    #
    #       select “Devices” in the virtual machine's menu bar
    #     > select the menu item “Install Guest Additions...”

    $ sudo -i
    $ cd /media/$(whoami)/VBox_GAs_5.2.22
    $ sh ./VBoxLinuxAdditions.run
    $ exit

    $ sudo shutdown -P now

    $ vboxmanage storageattach ubuntu \
                 --storagectl 'IDE controller' \
                 --port 0 --device 0 \
                 --medium 'emptydrive'

#### How to install the Guest Additions from the guest OS Debian?

From the guest OS:

    $ sudo aptitude update && aptitude safe-upgrade

    # I'm not sure about those steps.
    # See here for more info:
    #         https://www.virtualbox.org/manual/ch02.html#externalkernelmodules
    $ sudo aptitude install make gcc linux-headers-2.6-686 dkms
    $ sudo aptitude purge virtualbox-ose-guest-dkms virtualbox-ose-guest-utils virtualbox-ose-guest-x11
    $ sudo aptitude keep-all

    $ sudo shutdown -r now

    # mount the Guest Additions ISO file inside the VM:
    #
    #       select “Devices” in the virtual machine's menu bar
    #     > select the menu item “Install Guest Additions...”

    $ sudo -i
    $ cd /media/$(whoami)/VBox_GAs_5.2.22
    $ sh ./VBoxLinuxAdditions.run
    $ exit

    $ sudo shutdown -P now

    $ vboxmanage storageattach debian \
                 --storagectl 'IDE controller' \
                 --port 0 --device 0 \
                 --medium 'emptydrive'

#### How to UNinstall the Guest Additions from the guest OS?

    # Devices
    #       > Install Guest Additions...
    $ sudo -i
    $ cd /media/$(whoami)/VBox_GAs_5.2.22
    $ sh ./VBoxLinuxAdditions.run uninstall
    $ exit

#### What are the Guest Additions?

Device drivers and system applications which  can be installed inside a guest OS
to improve its performance, and  provide a better integration/communication with
the host OS.

For more info, see:

<https://www.virtualbox.org/manual/ch04.html#guestadditions>

#### Where is the documentation for the Guest Additions?

<https://www.virtualbox.org/manual/ch04.html>

###
### How to make VB synchronize the clipboards of the guest and the host OS?

Assuming you've successfully installed the Guest Additions:

    $ vboxmanage modifyvm ubuntu --clipboard bidirectional

---

Alternatively, in GUI:

      select “Devices” in the virtual machine's menu bar
    > select the menu item “Shared Clipboard”
    > select the menu item “Bidirectional”

### How to exchange files between the guest and the host OS?

Assuming you've successfully installed the Guest Additions, from the host OS:

    $ VBoxManage sharedfolder add ubuntu \
      --name ubuntu_share \
      --hostpath ~/VB/ubuntu/share

    $ mkdir -p ~/VB/ubuntu/share

Then, from the guest OS:

    # the name of the mount point must be different than the name of the shared directory
    $ sudo mkdir -p /media/share
    $ sudo chown $(whoami):$(whoami) /media/share
    $ sudo mount -t vboxsf -o uid=1000,gid=1000 ubuntu_share /media/share
    $ echo 'ubuntu_share /media/share vboxsf uid=1000,gid=1000 0 0' | sudo tee -a /etc/fstab

Alternative to the last command:

    $ echo 'mount -t vboxsf -o uid=1000,gid=1000 ubuntu_share /media/share' | sudo tee -a /etc/rc.local

Now, you can use `~/VB/ubuntu/share/` to exchange files.

---

I'm not sure, but after reading this:

>     --name <name> Specifies the name of the share.
>     Each share has a UNIQUE name within the namespace of the host operating system. Mandatory.

From here:

<https://www.virtualbox.org/manual/ch08.html#vboxmanage-sharedfolder>

It seems that the name given to the shared directory must be unique.
Hence why  I gave  the value  `ubuntu_share` to `--name`  in the  first command,
instead of just `share`.

###
### How to allow the VM to access a usb device on my host machine?

This is a two-step process.

First, you must ask VB to present a virtual USB controller to the guest.
Next, you must tell VB which usb device the VM can access.

Step 1:

    right-click on the VM (it must be shut down)
    > Settings
    > USB

Make sure that the following boxes are ticked:

   - Enable USB Controller
   - Enable USB 2.0 (EHCI) Controller

Step 2:

To add a  new filter, click on the  first icon (usb plug with blue  disk) on the
right, or press INSER.
Then, edit the fields of the filter:

   1. Name   =   arbitrary name given to the filter
   2. Vendor ID
   3. Product ID
   4. Revision
   5. Manufacturer (similar to Vendor ID)
   6. Product (similar to Product ID)
   7. Serial No
   8. Port

Alternatively, you can  display a menu with all the  devices currently connected
to the host by  clicking on the second icon (usb plug with  green plus sign), or
by pressing alt + INSER.
Then, select the device(s) to which you want the VM to have access.

Finally, press OK.

For more info, see:

- <https://www.virtualbox.org/manual/ch03.html#idm1641>
- <https://www.virtualbox.org/manual/ch08.html#idm5816>

#### What's the danger in allowing a VM to access a usb device?

If you give to your VM the access to a usb device, as soon as you start your VM,
the usb  device will be  ejected from the host  OS without having  been properly
unmounted.
Because of this, you may lose data.

Be sure that no usb device is connected  to your machine when you start a VM, or
that the VM can't access the usb device.

##
## Afterwards
### When executing a command, how can I refer to a VM, or to a snapshot?  (2)

You can use its name, or its UUID.
If you use its name, and it contains spaces, you must quote it.

###
### How to list all the VMs currently available?

    $ vboxmanage list vms

### How to print the config of a VM?

    $ vboxmanage showvminfo ubuntu
                            │
                            └ name of your VM

###
### Which subcommand allows me to change the configuration of a VM?

    modifyvm

### Can I use it to configure different options in a single command?

Yes:

    $ vboxmanage modifyvm <VM name> --option1 val1 --option2 val2 ...

###
### How to unregister and delete the VM ubuntu?

    $ vboxmanage unregistervm ubuntu --delete
                 │                     │
                 │                     └ remove the VM files from `~/VB/ubuntu/`
                 │
                 └ unregister the VM from VB config

##
# VM Usage
## What's the Host key?

It's a special key used in default chords to manipulate the VM, like pausing it,
or taking a snapshot.

By default, the Host key is Right-Ctrl.

The actual key is visible in the right bottom of the VM window.

## How to change the Host key?

      select “Input” in the virtual machine's menu bar
    > Keyboard
    > Keyboard Settings...
    > select the “Input” tab
    > select the “Virtual Machine” tab
    > left click in the “Host Key Combination” field
    > press some key(s) which won't conflict with existing key bindings
      Example: shift + left windows

## Where can I find the default Host chords to manipulate the VM?

<https://www.virtualbox.org/manual/ch09.html#idm9215>

## How to change a default Host chord?

The default chord to pause a VM is Host + p.
As an example, if you prefer to press Host + x, you could execute:

    $ VBoxManage setextradata global GUI/Input/MachineShortcuts "Pause=X,..."

## How to make the VM fullscreen?

Press Host + f.

## How to terminate the X server in the guest?

Press Host + Backspace.

This assumes that you have enabled the shortcut M-C-BS, with:

    $ sudo dpkg-reconfigure keyboard-configuration
    # last question

## How to enter the console 3 (tty3) in the guest?

Press Host + F3.

Source: <https://askubuntu.com/a/49573/867754>

##
## How to start the VM?

    $ vboxmanage startvm ubuntu

## How to pause/resume the VM?

    $ vboxmanage controlvm ubuntu {pause|resume}

---

Alternatively, you can press Host + p.

## How to save the current state of the VM?

    $ vboxmanage controlvm ubuntu savestate

It also closes the VM window.

But it doesn't really shut the VM down.
If you really want to shut it down:

    $ shutdown -P now

## Why should I avoid the `reset`, `poweroff`, `acpipowerbutton` subcommands to restart/shutdown the VM?

    $ vboxmanage controlvm ubuntu {reset|poweroff|acpipowerbutton}

`reset` is equivalent to pressing the reset button on your PC.
`poweroff` is equivalent to pulling the power cable on your PC.
`acpipowerbutton` is equivalent to pressing the power button on your PC.

They can all make you lose data in the VM.

##
## What's the current snapshot?

The snapshot from which the current state of the VM is derived.

## If I create a snapshot, does it become the current snapshot?

Yes.

## What's the new current snapshot relative to the previous one?

Its child.

##
## How to list all snapshots of the VM?

        $ VBoxManage snapshot ubuntu list

## How to view the VM settings that were stored with the snapshot?

        $ VBoxManage snapshot ubuntu showvminfo snap1

This is useful because the VM settings may change from a snapshot to another.

##
## How to take a snapshot of the VM, via the command-line, and via a key binding?

                                      ┌ name of the snapshot
                                      │
    $ vboxmanage snapshot ubuntu take snap1 \
      --description 'my first snapshot' \
      --live
        │
        └ allows you to create a snapshot
          while the VM is running

`snap1` is inserted  in the snapshots tree  as a child of  the current snapshot,
and automatically becomes the new current snapshot.

---

Alternatively, you can press Host + t.

## How to restore the state of the VM from the snapshot?

    $ vboxmanage snapshot ubuntu restorecurrent

'snap1' will become automatically the new current snapshot.

## How to restore the state of the VM from the snapshot 'foo'?

    $ vboxmanage snapshot ubuntu restore foo

## How to remove the snapshot 'foo'?

    $ vboxmanage snapshot ubuntu delete foo

## How to change the name or the description of the snapshot 'foo'?

                                          ┌ if 'foo' is the current snapshot,
                                          │ you could also use `--current`
                                          │
        $ VBoxManage snapshot ubuntu edit foo \
            --name 'new name' \
            --description 'new description'

##
# To read

    ┌───────────────────────────────┬────────────────────────────────────────────────────────────────┐
    │ 7. Remote virtual machines    │ https://www.virtualbox.org/manual/ch07.html                    │
    ├───────────────────────────────┼────────────────────────────────────────────────────────────────┤
    │ 8.9. VBoxManage clonevm       │ https://www.virtualbox.org/manual/ch08.html#vboxmanage-clonevm │
    ├───────────────────────────────┼────────────────────────────────────────────────────────────────┤
    │ 8.10. VBoxManage import       │ https://www.virtualbox.org/manual/ch08.html#vboxmanage-import  │
    ├───────────────────────────────┼────────────────────────────────────────────────────────────────┤
    │ 8.11. VBoxManage export       │ https://www.virtualbox.org/manual/ch08.html#vboxmanage-export  │
    └───────────────────────────────┴────────────────────────────────────────────────────────────────┘

<https://hackernoon.com/virtualbox-are-you-getting-your-moneys-worth-4d7f98f3d7d2>

---

Chapter 7 is interesting to learn how to run a VM on a remote server.
This would be useful to avoid consuming resources on our local machine.

The chapter also explains how to secure the communication between the client and
the server.

##
# Issues
## VB crashed!

It  probably has  written  a logfile  in  your home  directory,  or in  whatever
directory you were when you started it.
Find it and read it.

## I can't restore my snapshot!

Shut down the VM.

## I can't move the mouse to the host anymore!

Press Host.

---

Alternative:

Pause the VM by pressing Host + p.
Unpause it,  by pressing Host +  p a second time,  or shut down the  VM from the
terminal.

## When I press Enter once, the guest receives it twice!

It's because of the `xcape` process on the host machine.
If you kill it, the issue disappears:

    $ killall xcape

Note that pressing C-m doesn't cause the issue, only (right) Enter.

I don't know how to fix the issue without killing xcape...

The issue has already been reported on xcape's bug tracker:

<https://github.com/alols/xcape/issues/99>

---

Warning: This may make you validate a choice you didn't want.

Example:

    $ sudo dpkg-reconfigure keyboard-configuration

This command asks you some question.
Do NOT press Enter while in the guest OS, to validate an answer.
Doing so  would make you  automatically validate  the next answer  without being
able to review it.
Instead press C-m.

## I can't configure some setting of my VM from the GUI.  It's grayed out!

Saving the state of your VM is not enough:

    $ vboxmanage controlvm <name> savestate

Even though it closes the VM window.

You must shut it down completely:

    $ shutdown -P now

## I've got errors when I execute a command, due to a file not being found!

If an argument  of your command is a  filepath, and it contains a  tilde, do NOT
quote the path.
VB is unable to expand the tilde.

If you really must quote the path, then expand the tilde yourself.

## When I update my system, I have an error msg: “The following signatures were invalid: BADSIG ...”!

    $ sudo -i
    $ rm /var/lib/apt/lists/*
    $ rm /var/lib/apt/lists/partial/*
    $ apt-get clean
    $ apt-get update

## The guest refuses to boot:  “This kernel requires the following features not present on the cpu: pae”

    Host + s
    > System
    > Processor
    > tick “enable PAE/NX”

Pressing Host + s is equivalent  to selecting “Machine” in the virtual machine's
menu bar, then entering the Settings menu.

## I need to configure some setting from the command-line.  I don't know its name, nor the values it can take!

    $ vboxmanage modifyvm

The command will fail, and print all the possible options/values.
Look for some keyword you think should be present in the option name, like 'nic'
for a network setting.

## I need to access the VM settings, from the GUI, while it's shut down.  But when I shut it down, VB is closed!

1. Shut down the VM (from the guest OS).

2. Start VB by executing:

        $ virtualbox &!

