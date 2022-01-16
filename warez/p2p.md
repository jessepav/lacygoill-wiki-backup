# How to find a magnet URI
## from a website?

Visit this website: <https://btdig.com/>
Or this onion site: <http://btdigggink2pdqzqrik3blmqemsbntpzwxottujilcdjfz56jumzfsyd.onion/>

The onion url can be found on the BTDigg wikipedia page: <https://en.wikipedia.org/wiki/BTDigg>
Or on the  regular website after clicking  on the "TOR" button at  the bottom of
the page.

Type the title of the book in the search field, then look for a relevant torrent.
Finally, copy the magnet URI, and send it to the transmission daemon, so that it
can start the download:

    $ transmission-remote --add '<magnet URI>'

## from the command-line?

First, install the `we-get` script:

    $ git clone https://github.com/rachmadaniHaryono/we-get

    $ cd we-get
    $ python3 -m pip install .

Next, start `we-get` to  look for some keyword(s) matching the  file you want to
download:

    $ we-get --search 'counterpart s01e01' --results=10 --target 1337x,eztv,jackett_rss,the_pirate_bay,yts
                       ^----------------^
                       arbitrary search keywords

Now, on the  `we-get` prompt, type `show` and `Space`:  a completion menu should
automatically be opened.  Choose the torrent you want, and press `Enter`:

    we-get > show Counterpart.S01E01.WEB.H264-STRiFE[eztv]
    Counterpart.S01E01.WEB.H264-STRiFE[eztv] {
      "leeches": "13",
      "link": "magnet:...",
      "seeds": "192",
      "target": "1337x"
    }

In the output, copy the magnet URI, and pass it to the transmission daemon.

### Can I omit `--target`?

If you do, `rargb` is included in the list of sites, which gives an error:

    ...
    File "/usr/lib/python3.8/json/decoder.py", line 355, in raw_decode
      raise JSONDecodeError("Expecting value", s, err.value) from None
    json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Relevant issue report: <https://github.com/rachmadaniHaryono/we-get/issues/24>
I tried the `dev` branch, but it doesn't help.

### What are the sites that `we-get` can search on?

    $ we-get --get-list

    jackett_rss
    1337x
    yts
    eztv
    the_pirate_bay
    rargb

---

Note that there is a typo in `rargb`; it should be `rargb`.

To fix this, try to apply this patch:
```diff
diff --git a/we_get/modules/rargb.py b/we_get/modules/rargb.py
index 093698f..587534d 100644
--- a/we_get/modules/rargb.py
+++ b/we_get/modules/rargb.py
@@ -11,8 +11,8 @@ SEARCH_LOC = "/api/v2/list_movies.json?query_term=%s&quality%s&genre=%s"
 LIST_LOC = "/api/v2/list_movies.json?quality=%s&genre=%s"
 
 
-class rargb(object):
-    """ rargb module using the JSON API.
+class rarbg(object):
+    """ rarbg module using the JSON API.
     """
 
     def __init__(self, pargs):
@@ -79,7 +79,7 @@ class rargb(object):
 
 
 def main(pargs):
-    run = rargb(pargs)
+    run = rarbg(pargs)
     if run.action == "list":
         return run.list()
     elif run.action == "search":
```
Then run this shell command:

    $ mv we_get/modules/{rargb,rarbg}.py

##
# From the command-line, how to
## download a torrent?

    $ transmission-remote --add 'magnet:...'

## pause a torrent?

                                    torrent ID as reported by `transmission-remote --list`
                                    vvv
    $ transmission-remote --torrent 123 --stop
                                        ^----^

## list the files in a torrent?

    $ transmission-remote --torrent 123 --info-files
                                        ^----------^

## only download the files 45 and 67 to 89 in a torrent?

    $ transmission-remote --torrent 123 --no-get all --get 45,67-89
                                        ^----------^ ^------------^

First, `--no-get all` disallows the download for all files.
Then, `--get ...` allows the download for some files.

## ask for more peers?

    $ transmission-remote --torrent 123 --reannounce
                                        ^----------^

## monitor all the downloads?

    # in TUI
    $ watch -n 3 transmission-remote --list

    # in GUI
    $ xdg-open 'http://localhost:9091/transmission/web/'
                                                      ^
                                                      this slash is important to avoid an error:
                                                      https://askubuntu.com/a/44696

## delete a torrent (and the downloaded files)?

    $ transmission-remote --torrent 123 --remove-and-delete
                                        ^-----------------^

## delete a torrent (but keep the downloaded files)?

    $ transmission-remote --torrent 123 --remove
                                        ^------^

##
## I get an "Unauthorized error"!

    Unexpected response: <h1>401: Unauthorized</h1>Unauthorized User

Run these shell commands:

    $ sudo systemctl stop transmission-daemon.service
    $ sudo systemctl disable transmission-daemon.service

    $ transmission-daemon

### Why do I need to do that?

The   daemon   which   is   automatically  started   after   you   install   the
`transmission-daemon` package reads its config in this file:

    /etc/transmission-daemon/settings.json

The latter contains these settings:

    ...
    "rpc-authentication-required": true,
    "rpc-password": "{30a67f16c4a2b51ade72b030a6d3f09012ce6d04UGFLHIh5",
    "rpc-username": "transmission",
    ...

Because of `rpc-authentication-required` which is `true`, every time you want to
interact with the daemon, you need to authentify.
The credentials are given by `rpc-username` and `rpc-password`.
You would need to pass them to the daemon via `--auth`:

    $ transmission-remote --auth username:password
                          ^----------------------^

But the problem is that the password is  not saved in plain text; only some kind
of hash of the password is.

The solution would be to edit this config file, and write a new password:

    $ sudo systemctl stop transmission-daemon
    $ sudoedit /etc/transmission-daemon/settings.json
    # write plain password in the value of `rpc-password`
    $ sudo systemctl start transmission-daemon

   > The password that's being overwritten is a hash. The program is smarter than
   > usual and  detects that your  password is not a  hash, so it  overwrites the
   > password with the hash to be secure.

Source: <https://superuser.com/a/113652>

For more info, see:

   - `man transmission-daemon /^OPTIONS/;/-g --config-dir/`
   - <https://github.com/transmission/transmission/wiki/Configuration-Files#settingsjson>
   - <https://github.com/transmission/transmission/wiki/Editing-Configuration-Files#rpc>

### I don't want to manually start a daemon every time I restart the OS!

Then install a systemd service to do it automatically:

    $ tee <<'EOF' ~/.config/systemd/user/transmission-daemon.service
    [Unit]
    Description=Transmission BitTorrent Daemon
    [Service]
    ExecStart=/usr/bin/transmission-daemon --foreground --log-error
    ExecStop=/bin/kill --signal STOP $MAINPID
    ExecReload=/bin/kill --signal HUP $MAINPID
    [Install]
    WantedBy=default.target
    EOF

    $ systemctl --user enable transmission-daemon.service

### How come this new daemon is not also affected by the same issue?

The `transmission-daemon`  process that you start  as your usual user  reads its
config  in `~/.config/transmission-daemon/settings.json`,  which contains  these
settings:

    ...
    "rpc-authentication-required": false,
    "rpc-host-whitelist-enabled": true,
    "rpc-port": 9091,
    "rpc-url": "/transmission/",
    "rpc-whitelist": "127.0.0.1",
    "rpc-whitelist-enabled": true,
    ...

Notice  that `rpc-authentication-required`  is set  to `false`;  that's why  you
don't need to give credentials.

#### Is it less secure?

No because `rpc-whitelist-enabled` is set  to `true`, and `rpc-whitelist` is set
to `127.0.0.1`, which means the daemon will only accept requests from your local
machine.   For  an  attacker  to  interact with  the  daemon  without  providing
credentials, they would first need to access your machine.

##
### I still have an issue!

If the daemon is started as a systemd service, then inspect the systemd journal:

    $ journalctl --user-unit transmission-daemon.service

Otherwise, kill the daemon, and restart it like this:

    $ transmission-daemon --logfile /tmp/log --log-debug
                          ^----------------^ ^---------^
                                             max verbosity level

The daemon will then write all its messages in the `/tmp/log` file.

##
# Todo
## How to limit the bandwidth?

Look for the keyword "limit" at `man transmission-remote(1)`.
Also, look at the examples at the bottom of the same manpage.

##
## Watch and document this playlist:

<https://www.youtube.com/watch?v=ee4XzWuapsE&list=PLqv94xWU9zZ05Dbc551z14Eerj2xPWyVt>

We  need  a bunch  of  shell  aliases/functions  to  make the  interaction  with
transmission easier.  The first video has some good info for that.

---

And this video:
<https://www.youtube.com/watch?v=0uXFffq-UPU>
*torsocks - Access The Tor Network*

##
## review torrentflix as an alternative to we-get

<https://github.com/ItzBlitz98/torrentflix/>

Pros:

   - can download subtitles automatically
   - can stream
   - Trakt.tv integration

Trakt.tv seems  to be some  kind of  social website dedicated  to movies/series,
which could be useful to discover things to watch.
How good is it though?
How does it compare to these alternatives?:

   - <https://followmy.tv/>
   - <https://simkl.com/>

Are there better alternatives?

Cons:

   - require nodejs
   - require peerflix
   - pull many dependencies
   - does too much?  too complex?
   - only streaming?  no persistent download?

Update:  All those cons are not warranted.
However, peerflix and torrentflix are not real alternatives to `we-get`.
They are more an alternative to stremio (minus the catalogue and the posters).

## How to install stremio?

Download a `.deb` from here:
<https://www.stremio.com/downloads>

Install the deb like this:

    $ sudo apt install ./stremio*.deb

But not like this:

    $ sudo dpkg -i stremio*.deb

The latter would not automatically install any missing dependency.
The former will.

TODO: Document how to install the torrentio plugin/addon.

##
## Try to start xbindkeys via a systemd service.

    # look for todo items here:
    ~/wiki/admin/systemd.md
