# <https://spin0r.wordpress.com/2012/12/25/terminally-confused-part-six/>
## What's a process group?

A collection of related processes which  can all be signalled at once, sometimes
abbreviated as “pgrp”.

It is identified by an ID, abbreviated as PGID.

##
## What is the value of the PGID of a newly created process?

The one of its parent (inheritance).

### What does it imply?

A child joins the process group of its parent; so, each process in the system is
a member of a process group.

##
## What's a process group leader?

A process which verifies the relationship: PID = PGID.

As an  example, the process init(8),  the initial process of  the system, starts
with PID=PGID=1.
It is the process group leader for the process group 1.

## What happens if a process group leader dies?

The process group will be  without a leader until it is dissolved;  i.e., until all other
processes in the group either die or move to other process groups.

##
## Which system call can a process use to
### discover the PGID of itself or any other process?

getpgid(2)

### join another existing – or newly created – process group?

setpgid(2)

This system call can also be used on a child of the calling process.
IOW, a parent can change the process group of one of its children.

#### on which condition?

It must not be the leader of its process group.

##
## When I run a shell command, the resulting process is placed in a different process group from the shell.
### How does that happen?

   1. the shell fork(2)

   2. the shell calls setpgid(2) to move its fork into another process group
      (initially, the fork was in the same group as the shell)

   3. the child calls exec(2) to launch the requested program

##
## What does it mean for the `STATE` column to contain, for a given process, the flag
### `R`?

The process is running.

### `S`?

The process is sleeping, and can be interrupted by a signal.

#### Why do these 3 processes have the `S` flag?

    S  PPID   PID  PGID COMMAND

    S  4541 13243 13243 /bin/bash
    S 13243 13447 13447 strace -p 931
    S 13243 13448 13447 grep --color=auto ioctl

Note that `$ strace -p 931 | grep ioctl > ~/931_dbg &` has been run.

↣
The shell is wait(2)ing for ps to exit.

strace is ptrace(2)ing a process and waiting for it to make a system call.

grep is blocked on a read(2), waiting for strace to produce output.
↢

### `T`?

The process has been stopped by a job control signal (e.g. `C-z`, `$ kill -TSTP`).

### `Z`?

The process is defunct: it was terminated but not reaped by its parent.
Also called a "zombie" process.

##
## ?

Process  groups  are further  grouped  into  sessions,  in  the sense  that  two
processes in different sessions can’t be in the same process group.
When  the  system starts  up,  init(8)  is initially  the  only  process and  is
therefore the session leader of the session it’s in.
When a  process fork(2)s, the child  always ends up  in the same session  as the
parent.
A process may move itself into a  new session using the setsid(2) call, becoming
the session leader of the new session.
It  should be  clear that  any session  leader is  also a  process group  leader
(because, when  its session was  first created, it was  the only process  in the
only process group in that session), but the reverse is not necessarily true.
A process  is not allowed to  move to a new  session if it is  already a process
group leader, because this would change its process group as well.
(This implies that  session leaders cannot move into new  sessions; after all, a
session leader is also a process  group leader.) When a session leader dies, the
session will be without a leader until it is dissolved.

## ?

<https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html>
<https://stackoverflow.com/questions/6548823/use-and-meaning-of-session-and-process-group-in-unix>

##
# Jobs
## definitions
### What's a job?

A set  of processes, comprising  a shell  pipeline, and any  processes descended
from it, that have all been placed in the same process group (but different from
the shell's).

### What's a jobspec?

The shell artificially generates a job ID  for each job you start; the first job
you start from a given shell is 1, the second job is 2, and so on.

In a `fg`, `bg`,  `kill` or `disown` command, you can refer to  the job whose ID
is 123 with the token `%123`; this token is called a jobspec in `$ man bash`.

The term is a shorthand for “job specification”.

### What's the current job?

The last job which you've stopped or resumed.

### What's a background job?

A job that is running, but is not receiving input from the terminal.

### What's a foreground job?

The single job that is running and is receiving input from the terminal.

### What are the main differences between a foreground and background job?

Contrary to a  foreground job, a background job is  immune to keyboard-generated
signals, and can't read from the terminal.

### What are the two states in which a job can be?

Suspended or running.

###
### What's job control?

It refers to control of jobs by an interactive shell.

It allows  the shell  to control  the multiple related  processes entailed  by a
single shell command as one entity.

#### Which features does it provide?

   - starting a job in the background (&)
   - bringing a background job into the foreground (fg)
   - suspending, resuming or terminating jobs (C-z, bg, C-c)
   - sending an already running job into the background (C-z + bg)

##
## Which pid does the shell print when I start a pipeline as a job?

The pid of the last command in the pipeline.

##
## How to refer to
### the current job in a `$ kill`, `$ jobs`, `$ fg` or `$ bg` command?

    %

    %%

    %+

### the last but one job?

    %-

### a job with a prefix of its name or a substring appearing in its command-line?

Write a prefix after `%`:

    $ kill %prefix

Or a substring after `%?`:

    $ kill %?substring

---

    $ while true; do echo 'foo'; sleep 1000; done  & \
      sleep 1000                                   & \
      while true; do echo 'bar'; sleep 1000; done  &

    $ jobs
    [1]    running    while true; do; echo 'foo'; sleep 1000; done~
    [2]  - running    sleep 1000~
    [3]  + running    while true; do; echo 'bar'; sleep 1000; done~

    $ kill %sl
    $ kill %?foo
    $ kill %?bar

Here, we've started 3 jobs, and killed:

   - the second one, by referring to its prefix 'sl'
   - the first one, by referring to its substring 'foo'
   - the third one, by referring to its substring 'bar'

### a waited job?  (2)

You can use its pid or its jobspec.

In the previous script, the jobs were referred to thanks to their jobspecs.
Here's another version where they're referred to thanks to their pids:

    $ cat /tmp/sh.sh

            sleep 2 &
            pid1=$!
            sleep 1 &
            pid2=$!
            wait "${pid2}"
            echo '`sleep 1` has terminated'
            wait "${pid1}"
            echo '`sleep 2` has terminated'

##
## How to prevent a background job from writing to the terminal?

    $ stty tostop

This can be reversed with:

    $ stty -tostop

And you can see whether a background job can write to the terminal with:

    $ stty | grep tostop

##
## To what is the standard output of a job connected?

To the terminal from which the job was started.

### What's the unexpected consequence of this?

The job can  write on the terminal, even  if the user is writing  or executing a
command.

##
## What happens to a job if I kill the shell from which I started it?  Why?

The job is killed too.

It happens because a job is attached to the shell from which it was started.

##
## How to execute a command after
### *all* the jobs have terminated?

Use the `wait` builtin:

    $ cat /tmp/sh.sh

            #!/bin/bash
            sleep 1 &
            sleep 2 &
            wait
            if pidof sleep >/dev/null; then
              echo 'command executed while the jobs are still running'
            else
              echo 'command executed AFTER all the jobs have terminated'
            fi

    $ /tmp/sh.sh
    command executed AFTER the job has terminated~

For more info, see:

<https://unix.stackexchange.com/q/76717/289772>

### *a specific* job has terminated?

    $ cat /tmp/sh.sh

            sleep 2 &
            sleep 1 &
            wait %2
            echo '`sleep 1` has terminated'
            wait %1
            echo '`sleep 2` has terminated'

    $ /tmp/sh.sh
    # after 1s
    `sleep 1` has terminated
    # after 2s
    `sleep 2` has terminated

##
## job table
### What's the job table?

A per-shell table  keeping track of the background jobs  which were started from
the  current shell,  along  with their  job  number and  job  state (stopped  or
running).

### How to print the job table, with the pid of the jobs, and their original working directories?

    % jobs -dl
            ││
            │└ print the pids
            └ print the original working directory (zsh only)

### How to print info about the running jobs?  The stopped jobs?

    $ jobs -r
    $ jobs -s

### How to get the pid of the current job?

    echo $!

##
## fg / bg
### What's the main difference between `$ kill` and `$ fg`/`$ bg`?

`$ fg` and `$ bg` accept only job IDs as parameters.
In addition to those, `$ kill` also accept PIDs.

### How to stop the job whose id is 123?  How to resume it?

    fg %123
    bg %123

### How to start 3 jobs with a single command?

Add the `&` control operator after each command  you want to start as a job, and
concatenate all of them:

    $ sleep 101 & sleep 102 & sleep 103 &
                ^           ^           ^
                control operator

###
### How to bring into the foreground a job which is currently suspended in the background?  What if it's running?

In both cases:

    $ fg

### How to make a process, which runs in the foreground, run in the background?

    C-z
    $ bg

---

Here are all the possible transitions between the states of a process:

                 ┌─────────┐
                 │         │
            ┌───>│ running │<───┐
            │    │ in fg   │    │
            │    │         │    │
         fg │    └────┬────┘    │ fg
            │         │         │
            │     C-z │         │
            │         │         │
       ┌────┴────┐    │    ┌────┴──────┐
       │         │    └───>│           │
       │ running │         │ suspended │
       │ in bg   │<────────│ in bg     │
       │         │    bg   │           │
       └─────────┘         └───────────┘

###
### What does `$ %123` do?

It brings the job 123 from the background into the foreground.
Equivalent to `fg %123`.

### What does `$ %123 &` do?

It resumes the job 123 in the background.
Equivalent to `bg %123`.

##
## disown
### How can I prevent a job from being terminated when the parent shell session ends?

To circumvent the shell's hangup handling:

   - use nohup

     to tell the child process to ignore SIGHUP

   - use disown

     to remove the job from the job table, and tell the shell to not send SIGHUP
     once the session ends

### What does `$ disown` do?

It removes  jobs from the  job table,  so that when  the session ends  the child
process  groups are  not  sent SIGHUP,  nor  does  the shell  wait  for them  to
terminate.

### What happens to the current job after executing `$ disown`, and exiting the current shell?

Its processes become orphans, and are adopted by the init process.

### Which command should I prefer:  disown or nohup?  Why?

    $ disown

`nohup` doesn't prevent  SIGHUP to be sent to  the job, it just asks  the job to
ignore the signal.
`disown` *does* prevent SIGHUP to be sent to the job.
So, `disown` is more reliable.

For more info, see:

<https://unix.stackexchange.com/a/194640/289772>

### Which options are supported by zsh's disown builtin?

None.

###
### What's the effect of removing a job from the job table?

The shell will no longer report its status,  and will not complain if you try to
exit, while the job is still running or stopped.

### How to remove
#### the current job from the job table?

    $ disown

#### the jobs whose id are 1, 2 and 3 from the job table?

    $ disown %1 %2 %3

#### all the jobs from the job table?

    $ disown -a
             ├┘
             └ bash-only

#### all running jobs from the job table?

    $ disown -r
             ├┘
             └ bash-only

###
### How to mark a job so that it's NOT sent SIGHUP when the shell receives this signal?

    $ disown -h %123
             ├┘
             └ bash-only

### How to mark all jobs in the job table?

    $ disown -a -h

### Can a marked job still be interacted with `fg`, `bg`, ...?

Yes.

### How to start `cmd` as a running job without it being put in the job table?

    % cmd &!
          ├┘
          └ zsh-only

FIXME:

Try to download a playlist and use `&!` at the end to prevent the job from being
terminated once you close the shell:

    % dl_pl 'url' &!

Exit the shell: the job ends ✘

Update:

Try this:

        % ( dl_pl 'url' >/dev/null 2>&1 &! )

It seems to only download the first video in the playlist.
Is it because we closed the shell?

What happens if we don't close the shell?

What happens if we don't use a subshell?

What happens if we don't use a redirection?
(hint: it seems C-d ends the shell AND the `dl_pl` process)

##
# anacron
## How is anacron started?

By systemd because of the service `/lib/systemd/system/anacron.service`,
and/or the timer `/lib/systemd/system/anacron.timer`.

And by the `cron` daemon, because of the `/etc/cron.d/anacron` file.

However, only the first `anacron` instance does something.
The second one doesn't start any job, because of the timestamps in the spooldir.

## How to check whether systemd has started anacron?

    $ systemctl status anacron

##
##
##
# Todo
## playlist

<https://www.youtube.com/playlist?list=PLU2hZmcNdDQJN43RL6pGcX79fQVBFlobl>

## books

    classic shell
    375-377, 476

    how linux works
    159-161

    freebsd
    520-523

    cookbook
    228, 308, 347

    wicked
    154-162, 171, 254, 308

## anacron (unix stack exchange)

<https://unix.stackexchange.com/search?tab=votes&q=anacron>

