# Assimil
## ?

        video playlist

        https://unix.stackexchange.com/search?tab=votes&q=anacron

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

##
##
##
# How is anacron started?

By systemd because of the service `/lib/systemd/system/anacron.service`,
and/or the timer `/lib/systemd/system/anacron.timer`.

And by the `cron` daemon, because of the `/etc/cron.d/anacron` file.

However, only the first `anacron` instance does something.
The second one doesn't start any job, because of the timestamps in the spooldir.

# How to check whether systemd has started anacron?

        $ systemctl status anacron

##
##
##
# Jobs
## What's a job?

The shell's internal representation of a process group.

---

It maps the  shell concept of a command  to the OS concept of  the possibly many
processes that it entails.
Indeed, a  process may  create additional  child processes,  and a  single shell
command may consist of a pipeline of multiple communicating processes:

        grep title somefile.txt | sort | less

This example creates at  least three processes: one for grep,  one for sort, and
one for less.

## What's a jobspec?

It's how `$ man bash` calls the  `%n` notation which allows the user to interact
with a job in a `fg`, `jobs`, `kill` command.

The term is a shorthand for “job specification”.

## What are the two states in which a job can be?

Suspended or running.

##
## Are all processes in a pipeline members of the same job?

Yes.

A job is defined in POSIX as:

> A set of  processes, comprising a shell pipeline, and  any processes descended
> from it, that are all in the same process group.

Example:

            ┌ process 1
            │                  ┌ process 2
            │                  │
        $ { find / -name '*' | wc -l ;} 2>&- &
        $ jobs

## What's the useful consequence of this?

The a user  can stop/resume/kill a pipeline of several  processes, with a single
command.

## Which pid does the shell print when I start a pipeline as a job?

The pid of the last command in the pipeline.

##
## What's the current job?

The last job which we've stopped or resumed.

## How to refer to the current job in a `$ kill`, `$ jobs`, `$ fg` or `$ bg` command?

        %

        %%

        %+

## How to refer to the last but one job?

        %-

## How to refer to a job without using its number?

You can use a prefix of its name, or a substring that appears in its command-line.

        $ while true; do echo 'foo'; sleep 1000; done  & \
          sleep 1000                                   & \
          while true; do echo 'bar'; sleep 1000; done  &

        $ kill %sl
        $ kill %?foo
        $ kill %?bar

Here, we start 3 jobs, and kill:

        • the second one, by referring to its prefix 'sl'
        • the first one, by referring to its substring 'foo'
        • the third one, by referring to its substring 'bar'

##
## What's a background job?

A job that is running, but is not receiving input from the terminal.

## What's a foreground job?

The single job that is running and is receiving input from the terminal.

## What are the main differences between a foreground and background job?

Contrary to a  foreground job, a background job is  immune to keyboard-generated
signals, and can't read from the terminal.

##
## What's job control?

It refers to control of jobs by an interactive shell.

It allows  the shell  to control  the multiple related  processes entailed  by a
single shell command as one entity.

## Which features does it provide?

        • starting a job in the background (&)
        • sending an already running job into the background (C-z + bg)
        • bringing a background job into the foreground (fg)
        • suspending, resuming or terminating jobs (C-z, bg, C-c)

##
## How to prevent a background job from writing to the terminal?

        $ stty tostop

This can be reversed with:

        $ stty -tostop

And you can see whether a background job can write to the terminal with:

        $ stty | grep tostop

## To what is the standard output of a job connected?

To the terminal from which the job was started.

## What's the unexpected consequence of this?

The job can  write on the terminal, even  if the user is writing  or executing a
command.

## What happens to a job if I kill the shell from which I started it?  Why?

The job is killed too.

It happens because a job is attached to the shell from which it was started.

##
## How to execute a command AFTER ALL the jobs have terminated?

Use the `wait` builtin:

        $ cat /tmp/sh.sh

                #!/bin/bash
                sleep 1 &
                sleep 2 &
                wait
                if pgrep sleep >/dev/null; then
                  echo 'command executed while the jobs are still running'
                else
                  echo 'command executed AFTER all the jobs have terminated'
                fi

        $ /tmp/sh.sh
        command executed AFTER the job has terminated~

For more info, see:

        https://unix.stackexchange.com/q/76717/289772

## How to execute a command after a SPECIFIC job has terminated?

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

## How to refer to a waited job?  (2)

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

        • use nohup

          to tell the child process to ignore SIGHUP

        • use disown

          to remove  the job from  the job table, which  tells the shell  to not
          send SIGHUP once the session ends

        • use a terminal multiplexer like tmux

          so that the job is a child of the tmux server

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
`disown` DOES prevent SIGHUP to be sent to the job.
So, `disown` is more reliable.

For more info, see:

    https://unix.stackexchange.com/a/194640/289772

### Which options are supported by zsh's disown builtin?

None.

###
### What's the effect of removing a job from the job table?

The shell will no longer report its status,  and will not complain if you try to
exit, while the job is still running or stopped.

### How to remove the current job from the job table?

        $ disown

### How to remove the jobs whose id are 1, 2 and 3 from the job table?

        $ disown %1 %2 %3

### How to remove all the jobs from the job table?

        $ disown -a
                 ├┘
                 └ bash-only

### How to remove all running jobs from the job table?

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

