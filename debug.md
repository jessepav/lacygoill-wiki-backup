# How to bisect a long config file?

Note the current undo sequence number.
It will be useful later to restore the file in its original state.

Then press:

   - `yCiE` (yank code in the whole file)
   - `viE` (select whole file)
   - `p` (replace whole file with only the code; in effect, you've removed empty/commented lines)

Then, bisect the code.
Once you've  found the problematic line(s),  press `-u` to restore  the original
state of the file.

##
# Hard-to-reproduce issue
## How to find a MWE?

First, find an easy way to reset your environment so that the issue disappears.
Then, use it as often as you can.

This serves two purposes.
First, it will help you manually and quickly fix the issue when needed.
Second, it will help you find a reliable MWE.
Indeed, to do so, you need to remember what you've done recently.
Don't let the bug last too long.
The longer  it lasts, the less  chance you have  to retrieve in your  memory the
action which triggered it (“is it because I did X?”, “or Y?”, “or Z?”, ...).

We used  this trick  to find  a MWE to  reproduce an  issue where  sometimes Vim
caused the command-line/screen to be redrawn prematurely while we were trying to
copy some text in tmux copy mode.
We noticed  that we could temporarily  and manually fix the  issue by restarting
Vim from another pane.

##
# But report
## When shoud I write one?

Whenever you face an issue which you find hard to solve.

---

Don't make the mistake of thinking that a bug report is only useful to be posted
on an issue tracker.
It can help in many ways; read the next questions to understand how.

It doesn't matter whether your report:

   - would be badly received  on a forum (e.g. downvoted, ridiculed)
   - is too broad to be posted anywhere
   - doesn't belong to any existing issue tracker

You don't have to post it to reap benefits.

## What should I do at the very beginning, and then repeat regularly?

Start by writing the title of your issue, even if it's just a temporary title.

Use the keywords in this title to search for information on the issue tracker.
This may help you find more relevant info, and a solution.

If you don't find any solution, go on writing your report.
But whenever you make progress in  your understanding of the issue, stop writing
the report, update the title, and use its most important keywords in a search on
the issue tracker.

Bottom line: the title of your issue is *very* useful.

---

If you had  followed this rule, you  would have wasted less  time when writing
your bug report concerning the truncation of the clipboard in tmux + st.

## What groups of words should I pay attention to in the text of my report?

    For some reason
    Weirdly enough
    I don't know why but

When you  write that, it may  mean that you  have found something else  than the
current issue, which is also weird.
Understanding this weird thing may solve your issue, or simplify it.

Dedicate a  new report to  this weird  thing, even if  you have no  intention of
posting it online.
The mere  fact of explaining it  may help you  understand it, and then  in turn,
this may help you solve your issue.

---

As an  example, when we  tried to copy  some text from  tmux copy mode  while in
xterm, the clipboard was not written with the text.

We soon discovered  that tmux modifies the  OSC 52 sequence (it  removes the `c`
parameter).

This was a weird thing.

We should  have immediately asked  ourselves whether this removal  could explain
why xterm didn't write the text in its clipboard.
That would have saved us a lot of time.

We could  have ended up  thinking that  maybe xterm did  write the text,  but in
another selection.
Then, we could have inspected the output of `$ xsel -p`, `$ xsel -s`, `$ xsel -b`.
We would have found that xterm wrote the text in the primary selection.
We then would have  looked at `$ man xterm` to check whether  it was possible to
configure xterm and make it write to the clipboard.
There are only 25 matches for the pattern `clipboard` in the manpage atm.
So, we would have quickly found  the option `selectToClipboard`, tried to change
its default value from false to true, and fixed the issue.

## What should I do before posting my report?

Use it as temporary notes to explain your issue to a fictional listener.
Don't read it from start to finish; this would break the interactivity of the process.
Just use it to refresh your memory when necessary.

Make the  fictional listener active, i.e.  make them ask questions  whenever you
feel sth is not clearly explained, or  make them suggest sth whenever you have a
new idea for tackling the issue.

If it doesn't help, consider letting some time lapse, and retry a second time.
After a few days,  you may have gained a new insight  which leads your fictional
listener to ask better questions/suggest better ideas.

##
# What's the difference between “debugging” and “troubleshooting”?

You debug the design of a product which is faulty.
You troubleshoot a *copy* of a product whose design is known to be good.

You debug a broken design.
You troubleshoot a broken part in a product.

Car designers debug; car mechanics troubleshoot.
Software engineers debug; doctors troubleshoot the human body.

# What's the purpose of a troubleshooting book?

It's a compendium of everything that has  ever broken in a given type of system,
and what the symptoms and fixes were.
It gives  a troubleshooter the experience  of many others, and  helps in finding
known problems faster.

But it doesn't help much with new, unknown problems.
And thus it can't help with design problems.

If you're troubleshooting a standard  system, consult a troubleshooting guide to
see if your problem is listed.
If it isn't, or if the fix doesn't work, you'll have to debug the problem yourself.

##
# Give 2 examples of
## simulating a problem.

Some paragraphs are missing in the documents you write with your word processor.
You assume that the issue happens when you save the file to the disk.
So you write a  script which constantly writes to the  disk, to quickly simulate
the issue.

---

You have a leaky window.
You assume that the issue is due to the design of the window.
So you spray water against a seemingly identical window, to reproduce the issue.

## sTimulating a problem.

Some paragraphs are missing in the documents you write with your word processor.
You write a  script which generates keystrokes, and you  watch what gets written
to the disk.

---

You have a leaky window.
You climb  up a ladder,  use a hose  to spray water on  the roof and  watch from
where does the window leak.

##
# Why simulating a problem is often bad?

When you simulate a problem:

   - you have no guarantee that your testing environment is identical to the one
     where the issue was discovered

   - you make an assumption on the cause of the issue which may be wrong;
     this wrong assumption may lead you to fix a different issue

# What are the two main ways of sTimulating a problem?

You can automate it, or amplify it.

## What are their benefits?

Automating a problem makes it happen more  quickly, and allows you to focus your
attention on the exact conditions in which  it happens; in turn, this allows you
to better understand the cause of the problem.

Amplifying a  subtle problem, whose origin  is hard to locate  exactly, makes it
more obvious.

