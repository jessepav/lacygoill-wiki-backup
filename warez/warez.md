# General Websites

   - Curated list 1: <https://github.com/Igglybuff/awesome-piracy>
   - Curated list 2: <https://www.reddit.com/r/Piracy/wiki/megathread>
   - Curated list 3: <https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki>

# Anime Website

<https://nyaa.si/>

##
# Ebooks
## Websites

   - Library Genesis: <https://libgen.fun/> (don't miss the "Fiction" section)
   - Unofficial fork of Library Genesis: <https://libgen.rs/>
   - Library Genesis reddit wiki: <https://www.reddit.com/r/libgen/wiki/index>

   - Curated list 1: <https://github.com/Igglybuff/awesome-piracy#ebooks>
   - Curated list 2: <https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/reading>
   - Curated list 3: <https://www.reddit.com/r/Piracy/wiki/megathread/reading_material_and_elearning>

   - ZLibrary: <https://b-ok.cc/>
   - Recommendations: <https://app.thestorygraph.com/recommendations>

##
## IRC
### #ebooks on IRChighway

    /connect irc.irchighway.net
    /join #ebooks

To get a list of results in a zip archive, execute this command in the channel:

    @search your_book_title

Once  downloaded, unzip  the  archive;  in the  extracted  file,  search a  line
containing the book you're looking for.

Finally, copy the bang command, and execute it in the channel.
Example:

    !temerut Nick Cutter - The Troop (epub).rar

For more info, see:

- <https://irchighway.net/help/i-m-new-to-irc>
- <http://ebooks.byethost6.com/index.html>

### #bookz on Undernet

    /connect irc.undernet.org
    /join #bookz

For more info, see:

- <https://www.undernet.org/help.php>
- <https://encyclopediadramatica.online/Bookz>

###
### I can read an ad about an ftp server.  How to look at what it can serve?  How to download from it?

Let's assume the ad prints this:

    @Oatmeal │ @ --Bookstuff is now open via ftp @ ftp://book:stuffing@173.80.4.19/

From a terminal, run `ftp(1)`:

          replace with whatever IP address was given in the message
          v---------v
    $ ftp 173.80.4.19
    ftp> Connected to 173.80.4.19.
    ftp> 220 Welcome

    ftp> Name (173.80.4.19:lgc): book
                                 ^--^
                                 replace with whatever name was given in the message

    ftp> 331 Password required for book
    ftp> Password: stuffing
                   ^------^
                   replace with whatever password was given in the message

    # print the contents of the remote directory
    ftp> ls
    # download a particular file from the previous listing
    ftp> get <filename>

For more info, `man ftp`, or:

    ftp> help
    ftp> help ls
    ftp> help get
    ftp> help ...

##
## Where can I find audio books?

The best site seems to be BTDigg.

---

For a more specialized site (but not better than BTDigg), try AudioBook Bay:
<http://audiobookbay.nl/>

Focus the search field  in the top right corner of the page,  and type the title
of your ebook.
A list of front covers should be now displayed; click on the relevant one.
In the long table, find the info hash  of the torrent, and use it to reconstruct
the magnet URI:

    magnet:?xt=urn:btih:<infohash>
                        ^--------^
                        copied from the website

Finally, pass the magnet URI to the transmission daemon so that it can start the
download:

    $ transmission-remote --add '<magnet URI>'

##
# yt-dlp
## Getting info
### How to get more help?

    $ yt-dlp --help

###
### How to extract the url of a video embedded inside a webpage?

    $ yt-dlp --get-url 'webpage url'

#### How to stream it in mpv?

With a recent enough `mpv(1)`, you can pass it the url directly:

    $ mpv 'url'

This is possible thanks to the yt-dlp hook-script.
The latter looks at  the input URL, and plays the video  located on the website.
It works with many streaming sites, not just youtube.

The yt-dlp  hook-script is  enabled by  default; `--ytdl`  is assumed  even when
omitted.

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

    $ yt-dlp --format 12+34
             ^------------^

For more info, see `man yt-dlp /^FORMAT SELECTION`.

##
## Audio
### How to convert a video file into audio file?

    $ yt-dlp --extract-audio
             ^-------------^

Requires `ffmpeg` or `avconv`, and `ffprobe` or `avprobe`.

#### How to select mp3 as the audio format?

    $ yt-dlp --extract-audio --audio-format mp3
                             ^----------------^

##
## Subtitles
### How to list all the languages for which subtitles are available?

Use the `--list-subs` argument.

### How to select the english and french subtitles?

    $ yt-dlp --sub-lang fr,en ...
             ^--------------^

### How to download all the subtitles of a video

    $ yt-dlp --all-subs
             ^--------^

#### only the ones selected by `--sub-lang`?

    $ yt-dlp --write-sub
             ^---------^

#### only the ones automatically generated by YouTube?

    $ yt-dlp --write-auto-sub
             ^--------------^

###
### I don't want the video!  Only the subtitles!

    $ yt-dlp --skip-download ...
             ^-------------^

##
## How to download all the videos in a playlist
### whose index is between 12 and 34?

    $ yt-dlp --playlist-items 12-34
             ^--------------------^

### whose index is between 1, 2, 3, 7, 10, 11, 12, 13?

    $ yt-dlp --playlist-items 1-3,7,10-13
             ^--------------------------^

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

The item `%(autonumber)0Nd` lets you number the downloaded files, when there are
several (e.g. playlist); 2 specifies the number of digits to use.

If you think you're going to download between 10 and 99 videos, use 2.
Between 100 and 999 videos, use 3.
Etc.

##
# Pitfalls
## I can't access a website!

Maybe  it's  blocked  by your  ISP,  or  maybe  it  has blacklisted  your  IP/AS
(Autonomous System).

If so, check its status on a website such as:
<https://downforeveryoneorjustme.com/>

Also, try to access it using the TOR browser:
<https://tb-manual.torproject.org/installation/>

    $ cd ~/.local/bin/

    # download TOR browser, and extract the `tor-browser_en-US/` directory here
    $ cd tor-browser_en-US/

    $ ./start-tor-browser.desktop --register-app
    # now you can start the TOR browser from your application launcher (e.g. whisker menu)

