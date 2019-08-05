# Basic concepts
## What's a trigger prefix?

It's the character you have to write in  front of the name of a command which is
recognized by the bots on the channel.
You can use `!` to get the results as notices, or `.` to get them as as PMs.

## What are the pro(s) and con(s) of each prefix?

`!` work with all commands, contrary to `.`:

    ✘
    .la

    ✔
    !la

---

The buffer  opened by a command  prefixed by `.` is  automatically pre-filled by
the output of  past commands; this includes commands executed  during a previous
session.
IOW, `.cmd` gives you persistence of data across restarts.

## What's a filtering?   An exclusion?

An exclusion is the reverse of a filtering:

             ┌ filtering: only german movies
             ├────┐
    !movies  german
    !movies -german
            ├─────┘
            └ exclusion: any movie except german ones

## How to exclude several strings at once?

Separate them with commas:

    !movies -german,xxx 720p

##
# Get info
## How to get help?

    !help

## How to get info about a pack?

    !nfo releasename
         │
         └ != name of the file;
           do NOT include an extension (`.mkv`, `.avi`, ...)

Example:

    .nfo Kings.2017.720p.BluRay.x264-GUACAMOLE

Output:

    pre: 30.08.2018
    size: 3325 Mb (70x50mb)
    runtime: 86min

    imdb: https://www.imdb.com/title/tt5843850/
    rating: 4,7/10 from 1.113 users
    genre: Crime, Drama, Romance

    video: X264 2 Pass @ 4589 kbps
    reso: 1280 x 536 @ 2,40:1
    fps: 23,976

    audio: english 6ch dts @ 768kbps

##
## How to view my chat stats?

    !stat [nick]
           │
           └ optional nick of another user

Output example:

    -- │ o_o (unix@only.4.u): [#MG-CHAT] (lg) WORDS: 143 - LETTERS: 1084 - LINES: 76 (w/o cmds: 1) - CHARS/LINES: 14 -
       │ WORDS/LINES: 2 - CMDS: 75 (98.7%) - Activity: 1m ago
       │ Unknown option -- o_o (unix@only.4.u): [#MG-CHAT] (lg) WORDS: 143 - LETTERS: 1084 - LINES: 76 (w/o cmds: 1) -
       │ CHARS/LINES: 14 - WORDS/LINES: 2 - CMDS: 75 (98.7%) - Activity: 1m ago

## How to view my download stats?   (2)

Use the `!dl` or `!checkstats` commands.

`!dl` gives more info, and uses the buffer of the abjects server.
`!checkstats` gives less info, and uses the buffer of the `#mg-chat` channel.

---

Output example (!dl):

    -- │ BotReign (Bot@Me.Serve.You.Long.Time): [USER]       RANK: 1st Lieutenant-II (lg) (20518) ---> next RANK:
       │ Captain-III (30.0%) (16515 Users) - CREDITS: 3.38GiB
    -- │ BotReign (Bot@Me.Serve.You.Long.Time): [TRAFFIC]    COMPLETEs: 13x - ATTEMPTs: 20x - TRAFFIC: 29.53GiB
    -- │ BotReign (Bot@Me.Serve.You.Long.Time):              MONTH: 499.37MiB, 2x (Last: 0.00B, 0x) - WEEK:
       │ 499.37MiB, 2x - TODAY: 0.00B, 0x
    -- │ BotReign (Bot@Me.Serve.You.Long.Time): [SPEED]      LAST: 1.62MiB/s - SLOWEST: 40.00KiB/s
       │ ([mg]-MV|EU|007) - FASTEST: 2.37MiB/s ([MG]-HDTV|EU|S|Escape) - ACTIVITY: 1day 4hrs ago
    -- │ BotReign (Bot@Me.Serve.You.Long.Time): [#MG-CHAT]   WORDS: 129 - LETTERS: 990 - LINES: 72 (w/o cmds: 1) -
       │ CHARS/LINE: 13.8 - WORDS/LINE: 1.8 - CMDS: 71 (98.6%) - Activity: 1min 11secs

---

Output example (!checkstats):

    !BotReign │ lg is Level: 2 Total Downloaded: 29.53GiB Gets: 13 [Need 7 gets for Level 3] Request Credits:
              │ 3.38GiB

##
## How to list global xdcc channel stats?

    !stats

Output example:

    ~ls │ - STATS #MOVIEGODS ( 111/5042 Bots | 49425 packs | 14651 )
        │ TOTAL: Slots|1324 - Speed|1.07TB/s - Offered|60.32TB - Transferred|6.84PB - Queued|35
        │ CURRENT: Leechers|108 - Speed|205.44MB/s - Speed/Leechers|1.9MB/s
        │ RECORD : Leechers|764 - Speed|594.71MB/s - Speed/Leechers|2.35MB/s

##
## If the bot wall-e puts me in a queue, how to ask it to send a notification about my position in the latter?

    !queue wall-e

Make sure to check for notices in #moviegods.

##
## How to get an imdb link for the movie 'real steel'?

    !il real steel (2011)

This command will output up to 6 results.

## How to get details about the movie 'real steel' from 2011 querying imdb?  rottentomatoes?

    !i real steel (2011)
                  ├────┘
                  └ the year is optional, but if present it must be surrounded by parentheses

    !rt real steel (2011)

## How to get details about a movie whose name looks like 'real steel' querying imdb?

    !i -m real steel
       ├┘
       └ flip the match from exact to popular matches

##
## How to get the list of new/returning/subcribed shows for today?

    !today new

## How to get the details about the tv-show dexter?

    !ep dexter

## How to get the schedule for today's series episodes?  tomorrow's ?  monday's?  sunday's?

    !today
    !tomorrow

    !mon
    !sun

You can also get the schedule for the other days:

    !tue
    !wed
    !thu
    !fri
    !sat

##
## How to get the movie openings of the current week?  next week?  3 weeks ago?

    !next
    !next 2
    !next -3
           │
           └ you can use any number between -9 and 9

##
## How to list general averaged downloadstats from the last 24 hours?

    !24

##
# List packs
## What are the 27 sections I can search through?

   - android
   - apps

   - console
   - games
   - nds
   - ps3
   - psp
   - wii
   - xbox

   - ebook
   - latest
   - music

   - bluray
   - classic    (old known movies)
   - german
   - hd
   - hdtv
   - movies
   - mvid
   - pack
   - sd
   - sdtv
   - tv
   - x264
   - xvid
   - xxx
   - web

## How to list the packs of a given section?   The most downloaded ones during the last hour?

    !section

    !hot section

##
## What are the 10 genres of videos I can dl?

   - action
   - adventure
   - comedy
   - crime
   - drama
   - mystery
   - romance
   - sci-fi
   - sport
   - thriller

## How to list the videos of a given genre?

    !genre <type>

Examples:

    !genre adventure
    !genre mystery
    !genre thriller

##
## What are the 18 genres of music I can dl?

   - alternative
   - ambient
   - bass
   - black
   - dance
   - funk
   - hardcore
   - hip-hop
   - house
   - indie
   - jazz
   - metal
   - pop
   - punk
   - rap
   - reggae
   - rock
   - techno

## How to list house, pop, rock mp3s?

    !mp3genre house
    !mp3genre pop
    !mp3genre rock

##
## How to list the most downloaded releases?

    !tops

## How to list the most downloaded packs of the last 7 days containing the string 'hdtv', but not 'german'?

    !topdl7 -german hdtv

---

You need a level greater than 4 to go beyond 7 days.

---

The general syntax of the `!topdl` command is:

    !topdl[days] [filter|-exclusion] [SECTION/MOVIENAME/RELEASENAME/STRING]

##
## How to list the packs, in PMs, whose names contain the string 'foo', then a character, then 'bar'?

    .s foo?bar

## How to list the packs, in notices, whose names contain the strings 'foo' and 'bar'?   Including offline packs?

    !s  foo*bar
    !sa foo*bar
      │
      └ browse through All packs, including the offline ones

## How to list the packs, in notices, whose names contain the string 'homeland' in their name, but not 'german'?

    !s -german homeland
    │
    └ trigger prefix

Will display:

   - current number of gets
   - pack size
   - name of the pack
   - xdcc command to download it
   - queuesize
   - average userspeed

##
## How to list retail movies (dvd, bluray, ...)?

    !retail

## How to list SD Rips (not in german)?   HD Rips in 720p?   Webrips?

    !sd  -german
    !hd  -german 720p
    !web -german

## How to list the movies whose positions (from the latest one) are between `250` and `300`?

    !movies50-250
           ├────┘
           └ works with all `!section` triggers (`!hd`, `!games`, ...)

##
## How to list the latest 50 packs?   Ignoring the tv section?

    !latest50
    !latest50 -tv

FIXME:
We should be able to shorten the name of the command to `l` (like for `!search` → `!s`):

    !l50

But in practice, it doesn't work.
Do we need a higher rank?

## How to list the latest 5 packs in each section (ebook, games, mp3, ...)?

    !la

## How to list the latest packs, excluding the ones from the section mp3, tv, and `xxx`?

    !latest -mp3,tv,xxx

## How to get an overview of all possible layouts for the results?   How to use the second one?

    !l0
    !l2

##
## How to list the latest movies encoded with the `xvid` codec?   `x264` codec?

    !xvid
    !x264

## How to list the 20 latest packs from the bot '[mg]-stor|005' and matching the section `x264`?

    !bot20  [mg]-stor|005  x264

##
# Get packs
## How to make the bot `wall-e` send me the packet 123 right away, jumping on the queue if necessary?

    !send wall-e 123

The bot must support it, and you must be at least level 5.

## How to jump on a queue and get a packet by its name (regardless of its number)?

    !get file

## How to ask a bot to send me the contents of a tar file, instead of the archive itself?

    !extract archive.tar

## How to subscribe for a TV show season?

    !subscribe TV SHOWNAME.S06

New episodes will be autosent to you when available.

Level 8 required.
Up to 120 subscriptions.

##
# Common new movie tags
## What's a webrip?

Captured digital webstream e.g. from Netflix.

## What's the quality of a webrip?

Similiar to DVDRips, or BluRays when streamed in HD.

## What's the downside of a webrip?

If not  done properly, it can  have sporadic glitches or  OS notification sounds
embedded.

##
## What's a hd(tv)rip?

Captured tv stream.

## What's the quality of a hd(tv)rip?

It should be similiar to DVDRips, or BluRays when streamed in HD.
But it can vary a lot.
Without checking it is barely possible to tell how good or bad it is.

## What's the downside of a hd(tv)rip?

It can have artefacts/glitches due to transmission errors during streaming.

##
## What's a webdl?

Downloaded digital copy e.g. from itunes.

## What's the quality of a webdl?

Usually  good quality,  with none  of  the downsides  of webrips  but all  their
benefits.

web-dl  usually  “air”  way  before  retails,  making  them  a  very  attractive
alternative to retail rips.

They often feature dd5.1 sound, some  even subtitles, and are often available up
to 1080p.

##
## Order the different tags from best to worst quality?

   1. bluray hd ~ hd web-dl
   2. hd webrip
   3. hd(tv)rip
   4. hd-to-sd web-dl
   5. hd-to-sd webrip
   6. dvdrip ~ sd webdl
   7. sd webrip ~ sdtv

##
# Misc.
## What's the difference between a “releasename” and a “filename”?

    filename = releasename + extension

Example:

    ┌ releasename
    ├───────────────────────────────────┐
    Kings.2017.720p.BluRay.x264-GUACAMOLE.mkv
    ├───────────────────────────────────────┘
    └ filename

##
## How fast can I send messages to the channel without being kicked?

Don't send more than a few lines (3-5) every 20 seconds.
The actual number may vary with time.

If you send more than these few lines in 20 seconds, the channel flood mechanism
is triggered, and you'll be kicked.

In practice, when someone is kicked, the channel receives a message such as:

    ⟵ │ irc.abjects.net has kicked user (Channel flood triggered (limit is 5 lines in 20 secs))
                                                                           ^
                                                                           may change regularly

##
## How to change the default layout of a search result?

    !setsearch LAYOUT

E.g.:

    !setsearch |%COLOR,01%GETSx| |%SIZE| %RLS | %COLOR,16 /msg %NICK xdcc send #%PNUM  | %COLOR,04%OFFLINE

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

        !resetsearch

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
# Issues
## Why don't some commands work (no output, no effect)?

You probably don't have a high enough level.

## What's the purpose of the `!toppre` command?

Syntax:

    !toppre [section/moviename/releasename]

Here's the description given by the help:

> Listing  current  average   pretimes,  either  globally  or   for  a  specific
> section/moviename/releasename.

But what is a “pretime”?

## How to dl a packet via SSL?

Here's what the help says:

> To start a download via SSL, you will need:
>
>         - KVIrc (4.3.1 or higher)
>         - our SSL-cert/keyfile
>         - to use XDCC SSEND instead of XDCC SEND
>
> You can get kvirc from here:
>
>         !search KvIRC.v4.3.1.v6322_DCC_SSL_Support.tar
>
> If you're using mirc, you can try our own mirc SSL DCC script.
> Get it from here:
>
>         !search MG_SSL_DCC_MIRC.tar
> Or:
>         http://forums.mirc.com/ubbthreads.php/topics/240129/Secure_DCC_File_Transfers_aka_#Post240129

The help mentions a “SSL-cert/keyfile”.
Where can I dl it?

## How to implement a dcc rollback in WeeChat?

According  to  the help,  a  dcc  rollback  decreases  the probability  of  data
corruption when aborting/resuming transfers.

> To maintain a 5mb dcc rollback, add this line to your remote:
>
>         on *:getfail:*: /btrunc $filename $iif($calc($file($filename).size - 5120000 ) > 0, $ifmatch, 0)

## How to place my downloaded files in different folders, according to their names?

According to the help, it's possible in Mirc:

> To place  your downloads automatically in  different folders each, go  into your
> options: DCC/folders.
> Add an entry for each desired "category".
> E.g.:
>
>         *XXX* ->c:\xxx\
>     OR
>         *HDTV*x264* ->C:\tvx264
>     OR
>         *Bluray*,*Blu?Ray* -> C:\Blurays
>
> Or for games:
>
>     *SKIDROW*,*RELOADED*,*-FLT*,*-HI2U*,*-GENESIS* -> C:\GAMES

##
##
##
# Mirc-tricks
## 8

To add an extended  dcc send allowance check , add this to  your remote, it will
only allow sends from bots in moviegods that are voiced:

    ctcp *:DCC SEND *:?: if (($nick !isvoice #moviegods) || ([mg]* !iswm $nick) ) { echo -a BLOCKED SEND FROM $nick | haltdef }

##
# Request system
## What's a request?

An order for a particular file, which currently no bot on the channel has.

## What's a filled request?

A request which has been accepted, and  for which a bot has received the desired
file.

## How to send a request?

    !req releasename
         │
         └ if possible try to use a particular p2p or scene releasename.

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

    !reqclose <id/wildcard/partial requestname match (w/o spaces)> [reason for closure]
                                                                    │
                                                                    └ optional

## How to change my requestname?

    !reqchange <id/wildcard/partial requestname match(w/o spaces)> <New Requestname>

##
## How to list my latest 50 closed requests?

    !reqclosed

## How to list the latest 50 filled requests by the user toto?

    !reqfilled toto

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

