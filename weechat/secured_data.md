# What's secured data?

Any  data you  consider to  be sensitive,  such  as a  password, the  name of  a
channel, a proxy ip/name...

## Where does WeeChat store them?

In the configuration file `~/.config/weechat/sec.conf`.

### When does WeeChat read this file?

Before any other file.

##
## Where can I use them?

In:

   - command `/eval`

   - command line argument `--run-command`

   - options `'weechat.startup.command_{before|after}_plugins'`

   - other options that may contain sensitive data;
     see `/help` on the options to check if they are evaluated (i.e. contains "note: content is evaluated")

## How to print the algorithms used to encrypt them?

Use the `/secure` command:

    /secure
    Hash algo: sha256  Cipher: aes256  Salt: on~

    Passphrase is not set~

    No secured data set~

##
# Using secured data
## Why should I set a passphrase before adding secured data?

This will encrypt data in sec.conf instead of letting them in plain text.

### How to do it?

Use the `/secure passphrase` command:

    /secure passphrase this is my passphrase

#### What will happen afterwards, every time WeeChat is started?

It is asked by WeeChat on startup.

##### How to avoid this?  (2)

Set the environment variable `WEECHAT_PASSPHRASE`.

Or set the option `sec.crypt.passphrase_file` to read the passphrase from a file.
Note that only the first line of the file is read.

Also, even  if you  use a passphrase  file, it  seems that you  need to  set the
passphrase manually with  `/secure passphrase`, otherwise the  password would be
saved in plain text in sec.conf.

The environment variable has priority over the file.

###
## How to add secured data?

Use the `/secure set` command:

    /secure set <key> <value>

Example:

    /secure set freenodepass mypassword

The key  can be an  arbitrary name, which  you'll have to  use to refer  to your
value later.

### How to make sure my secured data can be correctly decrypted?

Press M-v in the `secured_data` buffer (the one opened by `/secure`).
The password should be printed on the screen.

Press M-v again to hide it.

###
## How to refer to some secured data?

Use the expression `${sec.data.<key>}`.

Example:

    /set irc.server.freenode.sasl_password "${sec.data.freenode}"

##
## How to remove secured data?

    /secure del <name of secured data>

## How to remove the passphrase?

    /secure passphrase -delete

###
# Using a secured password
## How to authenticate on freenode automatically on startup, using SASL, and a secured password?

Set your passphrase:

    $ echo 'this is my passphrase' >~/.weechat-passphrase
    $ chmod 600 ~/.weechat-passphrase
    /secure passphrase this is my passphrase
    /set sec.crypt.passphrase_file ~/.weechat-passphrase

If you choose a different file location, make sure the parent directory can't be
written by any user except you.

Secure your password (make WeeChat encrypt it):

    /secure set freenodepass mypassword
                │
                └ you can name your secured data however you like

Press  M-v in  the `secured_data`  buffer, to  check that  your password  can be
correctly decrypted.

Make WeeChat use your secured password to connect to freenode, using the [SASL][1] framework:

    /set irc.server.freenode.sasl_username "myusername"
    /set irc.server.freenode.sasl_password "${sec.data.freenodepass}"

If you don't use SASL, you can replace these lines with the single line:

    /set irc.server.freenode.password "${sec.data.freenodepass}"

### It doesn't work!

Make sure your sasl options are set correctly:

    /set *freenode*sasl*

Make sure the options `sec.crypt.*` are set correctly:

    /set sec.crypt.*

Make sure  that your passphrase  is set, and that  you can decrypt  your secured
password (by pressing M-v):

    /secure

Make sure your passphrase file is readable:

    $ ls -lh ~/.weechat-passphrase

Make sure `WEECHAT_PASSPHRASE` is not set:

    $ echo $WEECHAT_PASSPHRASE

Read `/help secure` and `/help sec.crypt.passphrase_file`.

Also, read this:

   - <https://weechat.org/blog/post/2013/08/04/Secured-data>
   - <https://gist.github.com/pascalpoitras/8406501>

The last gist contains the configuration of a user which uses a secured password
and SASL to get identified on freenode.

#### This doesn't help!

Then try to find a MWE:

    $ echo 'this is my passphrase' >/tmp/passphrase
    $ weechat -d /tmp/.weechat
    /server add freenode chat.freenode.net -nicks=mynick
                                                  ^^^^^^
    /secure passphrase this is my passphrase
    /set sec.crypt.passphrase_file /tmp/passphrase
    /secure set freenodepass mypassword
                             ^^^^^^^^^^
    /set irc.server.freenode.password "${sec.data.freenodepass}"

Also,  run `/fset  autoconnect` to  disable all  networks to  which you  connect
automatically on startup, except freenode.
And  run `/fset  autojoin` to  disable all  channels you  join automatically  on
connection.

Finally, run `/save` to save your settings, and restart WeeChat.
Try to join a channel which requires that you're identified, e.g. `#tmux`.
It should work.
From there, progressively re-include your  usual custom settings until something
breaks.

##
# Reference

[1]: https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer

