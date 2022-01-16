# Basic concepts
## What's DCC?

An IRC-related sub-protocol  enabling peers to interconnect using  an IRC server
for handshaking in  order to exchange files (or perform  non-relayed chats; i.e.
send/receive  messages  *directly*  to/from  another peer,  without  them  being
relayed to a server).

Once established, a typical DCC session runs independently from the IRC server.

It stands for "Direct Client-to-Client".

## What's XDCC?

A computer file sharing method, using an  IRC server as a host service, in which
IRC bots  run file sharing  programs to serve  usually large files  for download
using the DCC protocol.

It stands for "eXtended DCC".

For more info, see:
<https://www.youtube.com/watch?v=4tEgck_LaBc>

## What's abjects?

An IRC network where you can join the channel `#mg-chat`.
On this channel, you can download movies via XDCC.

    /connect irc.eu.abjects.net
    /join #mg-chat

If `irc.eu.abjects.net` doesn't work, try one of these domains instead:

   - `irc.eu.abjects.org`
   - `irc.eu.abjects.us`
   - `irc.us.abjects.com`
   - `irc.us.abjects.net`
   - `irc.us.abjects.org`
   - `irc.us.abjects.us`

---

For a download to work, you also need to join the `#moviegods` channel:

    /join #moviegods

But only as long as you're downloading.
You don't need to be on `#moviegods` just to look for movies on `#mg-chat`.

`#moviegods` is very noisy, since all bots are constantly spamming ads about all
the packs they can  serve.  If your ISP gives you a data  cap, or you just don't
like the idea of your download bandwidth being uselessly consumed, don't stay on
this channel more than  necessary.  That is, join it only  right before asking a
bot for a specific pack, and leave it as soon as the download is complete.

##
## What's a trigger prefix?

It's the character you have to write in  front of the name of a command which is
recognized by the XDCC bots on an IRC channel.

On `#mg-chat`, the results of a command can be received:

   - as notices in the buffer for the abjects server, if you use the `!` prefix
   - as PMs, if you use the `.` prefix

### What's the benefit of the `.` prefix?

The buffer  opened by a command  prefixed by `.` is  automatically pre-filled by
the output of  past commands; this includes commands executed  during a previous
session.

IOW, `.cmd` gives you data persistence across WeeChat restarts.

##
## What's a filtering?   An exclusion?

An exclusion is the reverse of a filtering:

             ┌ filtering: only german movies
             ├────┐
    .movies  german
    .movies -german
            ├─────┘
            └ exclusion: any movie except german ones

### How to exclude several strings at once?

Separate them with commas:

    .movies -german,xxx 720p

##
## What's the difference between a “releasename” and a “filename”?

    filename = releasename + extension

Example:

    ┌ releasename
    ├───────────────────────────────────┐
    Kings.2017.720p.BluRay.x264-GUACAMOLE.mkv
    ├───────────────────────────────────────┘
    └ filename

##
## What are the different types of videos, from best to worst quality?

   1. bluray hd
      hd web-dl

   2. hd webrip
   3. hd(tv)rip

   4. hd-to-sd web-dl
   5. hd-to-sd webrip

   6. dvdrip
      sd webdl

   7. sd webrip
      sdtv

"hd" = High Definition
"sd" = Standard Definition

##
## What's a webdl?

Downloaded digital copy e.g. from itunes.

### What's the quality of a webdl?

Usually  good quality,  with none  of  the downsides  of webrips  but all  their
benefits.

web-dl  usually “air”  way before  retails,  making them  a very  attractive
alternative to retail rips.

They often feature dd5.1 sound, some  even subtitles, and are often available up
to 1080p.

##
## What's a webrip?

Captured digital webstream e.g. from Netflix.

### What's the quality of a webrip?

Similiar to DVDRips, or BluRays when streamed in HD.

### What's the downside of a webrip?

If not  done properly, it can  have sporadic glitches or  OS notification sounds
embedded.

##
## What's an hd(tv)rip?

Captured tv stream.

### What's the quality of a hd(tv)rip?

It should be similiar to DVDRips, or BluRays when streamed in HD.
But it can vary a lot.
Without checking it is barely possible to tell how good or bad it is.

### What's the downside of a hd(tv)rip?

It can have artefacts/glitches due to transmission errors during streaming.

##
# Get info
## How to get help?

    .help

## How to view my download stats?

    .dl

##
## How to list the packs whose names contain
### the strings 'foo' and 'bar'?

    .s  foo*bar

### the string 'foo', but not 'bar'?

    .s -bar foo

### the string 'foo', then a character, then 'bar'?

    .s foo?bar

##
# Get packs
## How to make the bot `wall-e` send me the packet 123 right away, jumping on the queue if necessary?

    .send wall-e 123

The bot must support it, and you must be at least level 5.

## How to jump on a queue and get a packet by its name (regardless of its number)?

    .get file

## How to ask a bot to send me the contents of a tar file, instead of the archive itself?

    .extract archive.tar

## How to subscribe for a TV show season?

    .subscribe TV SHOWNAME.S06

New episodes will be autosent to you when available.

Level 8 required.
Up to 120 subscriptions.

## If the bot wall-e puts me in a queue, how to ask it to send a notification about my position in the latter?

    .queue wall-e

Make sure to check for notices in #moviegods.

##
# Misc.
## How fast can I send messages to the channel without being kicked?

Don't send more than a few lines (3-5) every 20 seconds.
The actual number can vary with time.

If you send more than these few lines in 20 seconds, the channel flood mechanism
is triggered, and you'll be kicked.

In practice, when someone is kicked, the channel receives a message such as:

    ⟵ │ irc.abjects.net has kicked user (Channel flood triggered (limit is 5 lines in 20 secs))
                                                                           ^
                                                                           can change regularly

##
## How to change the default layout of a search result?

    .setsearch LAYOUT

E.g.:

    .setsearch |%COLOR,01%GETSx| |%SIZE| %RLS | %COLOR,16 /msg %NICK xdcc send #%PNUM  | %COLOR,04%OFFLINE

---

Available tokens:

    ┌───────────┬─────────────────────────────────────────────────────────────────────────┐
    │ %ID       │ position of the package among all the results: 001, 002, ...            │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %COLOR,01 │ set the color for the following text using the first color in a palette │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %CHAN     │ channel name                                                            │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %GETS     │ number of times the package was downloaded                              │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %SIZE     │ size of the package                                                     │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %RLS      │ release name                                                            │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %NICK     │ bot nickname                                                            │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %PNUM     │ package number                                                          │
    ├───────────┼─────────────────────────────────────────────────────────────────────────┤
    │ %OFFLINE  │ online status                                                           │
    └───────────┴─────────────────────────────────────────────────────────────────────────┘

## How to reset the layout?

    .resetsearch

##
## My tar file unpacks without any error message, but the extracted file is incomplete/corrupted.  What to do?

Join `#incomplete` and request the missing/corrupted files or use `!extract`.

## My tar file fails unpacking (UNEXPECTED END OF ARCHIVE).  What to do?

Try resuming the download of the file from the same bot a few more times.
If the dl resumes, try unpacking the archive one more time.

---

If this didn't work,  try resuming the dl of the file  from different bots until
one of them succeeds.
Retry unpacking it.

---

If none of the bots was able to resume the dl of your file, you will have to get
the missing/corrupted files separately via `#incomplete`.

Additionally, you can report the corrupted/incomplete files in `#mg-lounge`.
Name the bot and the filename.
Report the name/version of the software you used to unpack the archive.

##
# Request system
## What's a request?

An order for a particular file, which currently no bot on the channel has.

## What's a filled request?

A request which has been accepted, and  for which a bot has received the desired
file.

## How to send a request?

    .req releasename
         │
         └ if possible, try to use a particular p2p or scene releasename

Whenever the request gets filled, your file will be autosent (level 3 required).

You have to wait a certain period  before you can request again (the higher your
level, the shorter your wait).

##
## What does `CREDITS` stand for?

The amount of data you can request.

## How to gain credits?

By idling and downloading.

##
## How to cancel my request?

    .reqclose <id/wildcard/partial requestname match (w/o spaces)> [reason for closure]
                                                                    │
                                                                    └ optional

## How to change my requestname?

    .reqchange <id/wildcard/partial requestname match(w/o spaces)> <New Requestname>

##
## How to list my latest 50 closed requests?

    .reqclosed

## How long do the bots try to fill a request?

It expires automatically after about 2 days.

## Is there a limit on the amount of data I can request?

Yes, the bigger the data, the greater level you need:

    ┌─────────────┬────────────┐
    │ level range │ size limit │
    ├─────────────┼────────────┤
    │     3-6     │    20GB    │
    ├─────────────┼────────────┤
    │     7-10    │    30GB    │
    ├─────────────┼────────────┤
    │    11-15    │    40GB    │
    ├─────────────┼────────────┤
    │     16+     │    45GB    │
    └─────────────┴────────────┘

## How are all the requests received by the bots tagged?

Accepted requests are tagged as ACKD.

    ┌ downloading?
    │
    │        ┌ available?
    │        │
    Incoming/spreading requests are tagged as DLIN/FILL.
                                              ├──┘
                                              └ DownLoadINg ?
###
### .help reqclose

    Type !reqclose <name/num> to close your own request. This is only possible
    if your request has not already been accepted. If your request has been
    accepted, that means a filler is currently adding your request to channel.
    The command syntax: !reqclose <name/num>
    Ex: !reqclose The.Expanse.s01 or !reqclose #######

### .help reqclosed

    Type !reqclosed to see a list of most recently closed (not filled) requests.
    Type !reqclosed <user> to see requests closed for a specific user.

### .help reqfilled

    Type !reqfilled to see a list of the most recently filled requests.
    Type !reqfilled <user> to see requests filled for a specific user.

### .help request

    If you are !rank 3 or higher, you can request files that are not currently in !s.

    Request limits are as follows: level 3-6 20GB, 7-10 30GB, 11-15 40GB, 16+ 45GB per.
    When requesting, be as specific as possible. If you are not specific, fillers may
    either close the request, or use their judgement to fill it as close as possible.
    Once your request is filled, you will have to wait to request again. The times are:
    Lvl 0-6 72h | Lvl 7-9 60h | Lvl 10-12 48h | 13+ 24h
    Ex: !req The.Expanse.S01.DVDRip or !req The.Expanse.S01.SD
    For related commands, type !help reqclose, reqclosed, reqfilled

