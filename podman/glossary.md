# c
## Linux *c*ontainer

A way to run an application inside an isolated environment.

Applications running natively on a system share the same:

   - binaries
   - libraries
   - kernel
   - filesystem
   - network
   - users

This can cause issues when an application is updated, especially wrt conflicting
libraries or unsatisfied dependencies.

OTOH, a container doesn't suffer from  these issues, because it doesn't interact
or conflict with other containers, nor with native applications.
To achieve  this, a containerized process  is isolated from the  host (and other
containerized processes) via Linux namespaces.

##
# n
## Linux *n*amespace

A kernel feature which is necessary to enable Linux containers.
It exposes alternative  and isolated system resources  (e.g. network, filesystem
mounts, users, ...) to an isolated process.

There are eight kinds of namespaces:

   - PID (Process ID) namespace
   - User namespace
   - UTS (UNIX Time-Sharing) namespace
   - network namespace
   - IPC (InterProcess Communication) namespace
   - cgroup namespace
   - mount namespace
   - time namespace

## PID *n*amespace

Processes  in different  PID  namespaces can  have the  same  PID.  This  allows
processes inside a  container to keep their PIDs after  suspending then resuming
the container, or after migrating it to a new host.

For more info, see: `man 7 pid_namespaces`.

##
## ?

    - A PID namespace isolates the process ID number in a separate space,
      allowing processes in different PID namespaces to retain the same PID.

    - A user namespace isolates user and group IDs, root directory, keyrings,
      and capabilities.  This allows a process to have a privileged UID and GID
      inside the container while simultaneously having unprivileged ones outside
      the namespace.

    - A UTS namespace allows the isolation of the hostname.

    - A network namespace allows isolation of networking system resources, such
      as network devices, IPv4 and IPv6 protocol stacks, routing tables,
      firewall rules, port numbers, and so on.  Users can create virtual network
      devices called veth pairs to build tunnels between network namespaces.

    - An IPC namespace isolates IPC resources such as System V IPC objects and
      POSIX message queues.  Objects created in an IPC namespace can be accessed
      only by the processes that are members of the namespace.  Processes use
      IPC to exchange data, events, and messages in a client-server mechanism.

    - A cgroup namespace isolates cgroup directories, providing a virtualized
      view of the process's cgroups.

    - A mount namespace provides isolation of the mount point list that is seen
      by the processes in the namespace.

    - A time namespace provides an isolated view of system time, letting
      processes in the namespace run with a time offset against the host time.

---

    - it  has a separated filesystem view, and  its program is executed from the
      isolated filesystem itself

    - it's run under an independent process ID (PID)

    - it has its own user and group IDs (UID/GID)

    - it has its own network resources (network devices, IPv4 and IPv6 stacks,
      routing tables, firewall rules, ...)

    - ...

##
# p
## podman

Short for Pod Manager.

It's the Red Hat replacement for Docker, which is meant to run containers.
It comes with greatly enhanced security, and features that aren't in Docker.

##
# r
## rootless container

A container run as a regular user.
This is only possible via Podman, not Docker.
