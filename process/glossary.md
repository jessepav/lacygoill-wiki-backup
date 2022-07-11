# c
## call stack

A subroutine A can call another subroutine B, and the process can repeat itself.
And when the execution of B terminates, the control should be handed back to the
A.  But we need a way to remember the address of the next instruction in A after
the call to B.  That's the job of the **call stack**.

##
# p
## process capabilities

Linux  distinguishes  2 categories  of  processes:  privileged processes  (whose
effective user  ID is  0, referred  to as superuser  or root),  and unprivileged
processes (whose effective UID is nonzero).

Privileged  processes bypass  all kernel  permission checks,  while unprivileged
processes  are  subject to  full  permission  checking  based on  the  process's
credentials  (usually: effective  UID,  effective GID,  and supplementary  group
list).

In this model, if a process needs some privilege associated with superuser, then
you need  to give it *all*  the superuser privileges (typically  via `sudo(8)`).
That can be an issue, because if the process gets compromised, misbehaves, or is
misused, then it could do a lot of damage.

That's why  another model  was introduced,  which lets you  grant only  a subset
of  the  superuser  privileges.   This  is possible  because  Linux  splits  all
the  privileges  associated  with  superuser   into  distinct  units,  known  as
**capabilities**, which can be independently enabled or disabled per process.

In this  model, a process  does not  need to be  run as superuser.   Instead, it
should only  be given the  least amount of privileges  necessary to do  its job.
This way,  if it gets  compromised, misbehaves, or is  misused, then it  will do
less damage.

For more info, see `man 7 capabilities`.

##
# s
## stack frame

That's what a call stack is made of.
Each frame corresponds  to a call to  a subroutine which has  not yet terminated
with a return.

The frame at the top of the stack is for the currently executing routine.

A frame usually includes the following items (in the order they are pushed):

   - the routine's arguments

   - the address of the next instruction in the routine's caller

   - the routine's local variables

