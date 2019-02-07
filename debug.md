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

Amplifying a subtle problem whose origin is hard to locate exactly makes it more
obvious.

