# Animes

<https://animetorrents.me/>

# Reddit

   - <https://www.reddit.com/r/Piracy/>
   - <https://www.reddit.com/r/TPB/>
   - <https://www.reddit.com/r/megalinks/>
   - <https://www.reddit.com/r/trackers/>

##
# Ebooks
## Library Genesis

<http://gen.lib.rus.ec/>

If the page is written in russian, click on the button labeled 'EN' in the toolbar.

## #ebooks

    /server irc.irchighway.net
    /j #ebooks

Maybe wait 30 seconds after joining to send to channel.
Run `@search your_book_title` to get a list of results in a zip archive.
Unzip the archive, and search a line containing the book you're looking for.
Finally, copy the bang command, and run in the channel.
Example:

    !temerut Nick Cutter - The Troop (epub).rar

For more info, see:
<http://ebooks.byethost6.com/index.html>

## #bookz

    /server irc.undernet.org
    /j #bookz

## google

<https://cse.google.com/cse/publicurl?cx=011394183039475424659:5bfyqg89ers>

Google custom search using this list of predefined urls: <http://pastebin.com/62tKNmm1>

   - <http://gen.lib.rus.ec/*>
   - <http://en.bookfi.org/*>
   - <http://bookzz.org/*>
   - <http://forum.mobilism.org/*>
   - <http://tuebl.ca/books/*>
   - <http://avxhome.se/ebooks/*>
   - <http://www.4shared.com/*>
   - <http://mediafire.com/*>
   - <http://ipmart-forum.com/*>
   - <http://ebook3000.com/*>
   - <http://freebookspot.es/*>
   - <http://demonoid.ph/*>
   - <http://ebookee.org/*>
   - <http://kat.cr/*>
   - <http://www.downeu.org/ebook/*>
   - <https://onebigtorrent.org/torrents/*>
   - <http://manybooks.net/titles/*>
   - <http://freshwrap.ws/*>
   - <http://www.plentyofebooks.net/*>
   - <http://book.pdfchm.net/*>
   - <http://www.freebookspot.es/*>
   - <http://www.feedurbrain.com/forum/*>
   - <http://ebookbrowsee.net/*>
   - <http://2020ok.com/books/*>
   - <http://librs.net/*>
   - <http://thepiratebay.la/torrent/*>
   - <http://bitsnoop.com/*>
   - <http://www.giuciao.com/books/*>
   - <http://books.tr200.org/*>
   - <http://booksc.org/*>
   - <http://club.topsage.com/*>
   - <http://ebookjunkie.com/*>
   - <http://nips.djvuzone.org/*>
   - <http://pdf-giant.com/*>
   - <http://manybooks.net/*>
   - <https://www.scribd.com/*>
   - <http://freecomputerbooks.com/*>
   - <http://www.freetechbooks.com/*>
   - <http://www.onlinefreeebooks.net/*>
   - <http://www.onlineprogrammingbooks.com/*>
   - <http://www.ebooklobby.com/*>
   - <http://bookboon.com/*>
   - <https://www.reddit.com/r/eebooks/*>
   - <https://www.reddit.com/r/mathbooks/*>
   - <https://www.reddit.com/r/csbooks/*>
   - <https://www.reddit.com/r/physicsbooks/*>
   - <https://www.reddit.com/r/econbooks/>

## See also

   - <http://learnbyreading.herokuapp.com/?hack=true>
   - <https://forum.mhut.org/viewforum.php?f=6> (LG forum)
   - <https://www.reddit.com/r/Piracy/comments/7q856s/is_there_a_problem_with_library_genesis/>
   - <https://www.reddit.com/r/Scholar/comments/2raea8/libgen_down/>
   - <https://genofond.org/viewtopic.php?p=9000/>
   - <https://ebookee.org>
   - <https://www.reddit.com/r/Piracy/comments/60gbf7/library_genesis_broken/>
   - <https://www.reddit.com/r/Scholar/comments/3bs1rm/meta_the_libgenscihub_thread_howtos_updates_and/>
   - <https://www.reddit.com/r/antilibrary/comments/6ow6tq/antilibrary_faq/>
   - <https://www.reddit.com/r/Piracy/comments/3i9y7n/guide_for_finding_textbooks/>
   - <https://www.reddit.com/r/trackers/comments/hrgmv/tracker_with_pdfsebooks_of_college_textbooks/c1xrq44>

##
# Youtube-dl
## Getting info
### How to get more help?

    $ youtube-dl --help

###
### How to extract the url of a video embedded inside a webpage?

    $ youtube-dl -g 'webpage url'
                  │
                  └ --get-url

#### How to stream it in mpv?

    $ mpv $(youtube-dl -g 'url')

###
### How to get the final name of the file which would be downloaded from an url?

Use the `--get-filename` argument.

#### How to restrict it to only ASCII characters, and avoid "&" and spaces?

Use the `--restrict-filenames` argument.

###
### How to list all the formats in which a video is available?

Use the `-F` (`--list-formats`) argument.

### How to select the stream whose format code is 123?

Use the `-f123` (`--format 123`) argument.

### How to select and merge the two streams of index 12 and 34?

    $ youtube-dl -f12+34
                  ^----^

For more info, see `man youtube-dl /FORMAT SELECTION`.

##
## Audio
### How to convert a video file into audio file?

    $ youtube -dl -x
                   │
                   └ --extract-audio

Requires `ffmpeg` or `avconv`, and `ffprobe` or `avprobe`.

#### How to select mp3 as the audio format?

    $ youtube-dl -x --audio-format mp3
                      ^----------^

##
## Subtitles
### How to list all the languages for which subtitles are available?

Use the `--list-subs` argument.

### How to select the english and french subtitles?

    $ youtube-dl --sub-lang fr,en ...
                   ^-----------^

### How to download all the subtitles of a video

    $ youtube-dl --all-subs
                   ^------^

#### only the ones selected by `--sub-lang`?

    $ youtube-dl --write-sub
                   ^-------^

#### only the ones automatically generated by YouTube?

    $ youtube-dl --write-auto-sub
                   ^------------^

###
### I don't want the video!  Only the subtitles!

    $ youtube-dl --skip-download ...
                   ^-----------^

##
## How to download all the videos in a playlist
### whose index is between 12 and 34?

    $ youtube-dl --playlist-items 12-34 ...

### whose index is between 1, 2, 3, 7, 10, 11, 12, 13?

    $ youtube-dl --playlist-items 1-3,7,10-13 ...

##
## How to change the template used to name a downloaded file?

Use the `-o` argument.

Example:

    -o "%(autonumber)02d - %(title)s.%(ext)s"

This example could name a file like so:

        42 - My Wonderful Video.mp4
        │    │                  │
        │    │                  └ %(ext)s
        │    └ %(title)s
        └ %(autonumber)02d

The  item `%(autonumber)0Nd`  allows you  to number  the downloaded  files, when
there are several (e.g. playlist); 2 specifies the number of digits to use.

If you think you're going to download between 10 and 99 videos, use 2.
Between 100 and 999 videos, use 3.
Etc.

##
# Issues
## tpb is unavailable!

Try to visit the tor site:
<http://www.uj3wazyk5u4hnvtk.onion/>

If you can't click on a magnet, search  for the text 'magnet' in the source code
of the webpage; copy the link and paste it in transmission.

---

TODO: Watch and document these videos:

torsocks - Access The Tor Network - Linux CLI: <https://www.youtube.com/watch?v=0uXFffq-UPU>
W3M Magnet Links Handler - Linux CLI: <https://www.youtube.com/watch?v=euk_LMdXNOU>

##
# Todo

Review the quality of the sites given here:
<https://github.com/Igglybuff/awesome-piracy#courses-and-tutorials>

