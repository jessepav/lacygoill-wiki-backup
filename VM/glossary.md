# a
## appliance

An  entire software  configuration (e.g.  mail  server), which  can be  shipped,
installed and run onto any machine.

An appliance can be packed into a VM, which can then be imported in a VirtualBox
instance on the desired machine.

##
# b
## base folder

Root directory where all the files of a VM are stored.

Example of value:

    /home/user/VirtualBox VMs/ubuntu

## bridged networking

Networking mode  in which  VirtualBox uses  a device driver  on the  host system
(called a “net  filter driver”) that filters data from  the physical network
adapter.
This  lets  VirtualBox intercept/inject  data  from/into  the physical  network,
effectively creating a new network interface in software, through which the host
and the guest can exchange data.

To the host  system, it looks as  if the guest was physically  connected to this
interface using a network cable.  Among other things, this lets you:

   - set up routing or bridging between the guest and the rest of your network
   - run a server program inside the VM

##
# c
## clone

Copy of an existing VM.

Typically used to:

   - experiment with a VM configuration
   - test different guest OS levels
   - back up a VM

### full clone

A full clone can operate fully without the source VM.
To achieve this,  it copies all dependent  disk images to the  new VM directory,
which means that it takes as much space as the source VM.

### linked clone

A linked clone needs the source VM to operate.
It creates new differencing disk images based on the source VM disk images.
It takes much less space than the source VM (e.g. 400Mb vs 7GiB).

##
# d
## (kernel) driver

A bit of compiled code which lets the kernel talk to some hardware device.
It "drives" the hardware.

A driver is a special kind of module.

##
# e
## extension pack

An optional pack of extensions which adds some features to VirtualBox:

   - Disk Encryption
   - Host Webcam
   - NVMe
   - PXE ROM
   - USB 2.0 and USB 3.0 Host Controller
   - VirtualBox RDP (Remote Desktop Protocol)

##
# g
## guest additions

Device drivers and system applications which  can be installed inside a guest OS
to improve its performance, and  provide a better integration/communication with
the host OS.

##
# h
## host key

A special key used  in default chords to manipulate the VM,  like pausing it, or
taking a snapshot.

By default, it's Right-Ctrl, but it can be changed.
Its current value key is visible in the right bottom of the VM window.

For more info, see:
<https://www.virtualbox.org/manual/ch09.html#host-key-customize>

##
# m
## (kernel) module

A bit  of compiled code that  can be inserted  into the kernel at  runtime; e.g.
with `insmod(1)` or `modprobe(1)`.

##
# n
## Network Address Translation (aka NAT)

Default networking mode for a new VM.

It's good enough to  browse the Web, download files, and  view emails inside the
VM.  But it suffers from some limitations, such as the inability to:

   - run a server program (unless you set up port forwarding)
   - connect to another virtual machine in order to simulate a network

##
## network adapter (aka NIC)

Piece of hardware (data-link abstraction).

NIC stands for Network Interface Controller.

## network interface

Piece of software (IP-level abstraction).

##
# s
## storage device

Hardware emulated by VirtualBox for a VM.

## storage medium

File on the host system, which VirtualBox  uses to store the data of an emulated
storage device.  The latter could be a dvd disk, or a hard drive disk.
