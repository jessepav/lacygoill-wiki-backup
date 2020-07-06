# How to bind the keyword 'foo' to the urls of irc servers?

    /server add foo <url>[,...]

# How to set a boolean option, such as 'ssl', local to a server?   (2)

    /set irc.server.freenode.ssl
    /server add chat.freenode.net -ssl

# How to set a non-boolean option (i.e. 'autojoin') local to a server?   (2)

    /set irc.server.freenode.autojoin "#foo,#bar,#baz"
    /server add chat.freenode.net -autojoin=#foo,#bar,#baz

# How to connect to the network bound to the keyword 'foo' on port 1234?

    /connect foo/1234

# How to automatically connect to the network 'foo' when I start WeeChat?

    /set irc.server.foo.autoconnect on

# How to automatically join `#bar` and `#baz` when I connect to the network 'foo'?

    /set irc.server.foo.autojoin "#bar,#baz"

# How to remove the network 'foo' from the list of known networks?

    /server del foo

# How to duplicate the network 'freenode' as 'freenode-test'?

    /server copy freenode freenode-test

# How to rename the network 'freenode-test' into 'freenode2'?

    /server rename freenode-test freenode2

##
# What happens when I add the network 'abjects' to the list of known networks?

When you do:

    /server add abjects irc.eu.abjects.net

WeeChat creates 41 new options:

    abjects.addresses = "irc.eu.abjects.net"
    abjects.proxy
    abjects.ipv6
    abjects.ssl
    abjects.ssl_cert
    abjects.ssl_priorities
    abjects.ssl_dhkey_size
    abjects.ssl_fingerprint
    abjects.ssl_verify
    abjects.password
    abjects.capabilities
    abjects.sasl_mechanism
    abjects.sasl_username
    abjects.sasl_password
    abjects.sasl_key
    abjects.sasl_timeout
    abjects.sasl_fail
    abjects.autoconnect
    abjects.autoreconnect
    abjects.autoreconnect_delay
    abjects.nicks
    abjects.nicks_alternate
    abjects.username
    abjects.realname
    abjects.local_hostname
    abjects.usermode
    abjects.command
    abjects.command_delay
    abjects.autojoin
    abjects.autorejoin
    abjects.autorejoin_delay
    abjects.connection_timeout
    abjects.anti_flood_prio_high
    abjects.anti_flood_prio_low
    abjects.away_check
    abjects.away_check_max_nicks
    abjects.msg_kick
    abjects.msg_part
    abjects.msg_quit
    abjects.notify
    abjects.split_msg_max_length

Their names are all prefixed by `irc.server.`.

# How to reset the values of all the options local the network 'abjects'?

    /unset -mask irc.server.abjects.*

Note that WeeChat doesn't remove them.
They're made empty, but they still exist.

##
# How to change the url(s) of the server(s) connecting to the network 'abjects'?

    /set irc.server.abjects.addresses "my.new.url[,...]"

# How to change the list of nicks for the network 'abjects'?

    /set irc.server.abjects.nicks "my,new,nicks"

##
# How to list all known networks to which I can connect?

    /server [list]

# Assuming the list is “criten,abjects,freenode”, how to reorder it into “freenode,abjects,criten”?

Use the `reorder` subcommand:

    /server reorder freenode,abjects,criten
            ^-----^

# How to print all the values of the options local to the freenode network, in the core buffer?

    /server listfull freenode

---

You could also execute:

    /set irc.server.freenode.*

But it would open a new `fset` buffer.

Pro: interactive
Con: more verbose

##
# How to focus the buffer of the current network?

    /server jump

##
# How to get statistics about the size of the IRC network?

    /lusers

# Why is it better to use the canonical name of an IRC server (i.e. `chat.freenode.net`), rather than its IP address?

IP addresses can change without notice:

   - the administrator running the server may decide to use a different machine
   - the route through which it connects to the rest of the Internet may change

##
# Issues
## I can't connect to the server. It says I'm K:lined. What does it mean?

Your address  matches an entry  on the server's  internal list of  addresses not
permitted to use it.

K:lines are known as  such because the part of the  configuration file where the
server  stores  these  “kill  lines”,  and  checks  upon  them  with  each  user
connection, consists of lines beginning with `K:`.

Not all server operators are kind enough to provide a reason, so it might return
no more than a generic "Banned" or "You are not welcome" notice.

The most  common reason for  being K:lined is  that the server's  operators have
observed misbehavior from  users within a group of addresses  (of which yours is
one), and therefore have  decided not to permit any user from  that group to use
the server.

Another reason  for a  K:line could  be that you  are expected  to use  a server
closer to you in terms of either network topology or geographical location.

Remove the server from your list and try to connect to a different one.

## I can't connect to the server. It says I'm G:lined. What does it mean?

Some  IRC  networks   that  have  a  global  abuse   policy  implement  G:lines:
network-wide K:lines (also called “global K:lines”).

On  these networks,  repeated  or  extensive abuse  may  result in  simultaneous
K:lining from all servers on that network.

Many servers admin don't  take too much care to remove old  K:lines, so they may
remain in place indefinitely, even for years.

G:lines  tend to  have a  set expiration  date, which  can be  anywhere from  20
minutes to a month after it was set.

Some modern server versions use temporary K:lines, automatically removed after a
short while.

Try to ask one of the server's  operators or email the server's admin address to
have it lifted - if they are inclined to do so.

##
## The connection closes after a minute or two with the message “Ping timeout”!

The server got no reply from your client from the first PING.
It  must receive  a PONG  reply to  confirm that  your client  is connected  and
responding.

The cause may be:

   - a slow network connection

   - a heavy load on the server machine
     (which delays the PING on its way to you)

    - a heavy load on your machine
     (which prevents the reply from reaching the server before the timeout)

---

Install  the  package  `inetutils-traceroute`,  then  use  the  `traceroute6(8)`
command to diagnose the connection between your machine and the server:

    $ traceroute6 chat.freenode.net

## The connection fails with the message “timeout”!

Try to connect using only telnet.

    $ telnet chat.freenode.net 6667

You should see something like:

    :leguin.freenode.net NOTICE * :*** Looking up your hostname...~
    :leguin.freenode.net NOTICE * :*** Checking Ident~
    :leguin.freenode.net NOTICE * :*** Couldn't look up your hostname~

If that's not the case, weechat is not the issue.
The irc server is unavailable.

For more info, see:
<https://stackoverflow.com/a/12661281/9780968>

## The connection fails with the message “No more connections” or “Server full”!

You can either use  another server or wait a little  for the previous connection
to timeout on the server's side.

---

This issue arises when the number of connections the server has allotted to your
connection class is full.

Servers often  define address groups  with a maximum limit  of users who  may be
connected simultaneously.
For example, they could assign the class  20 to all foreign addresses, and set a
limit of 50 connections for this class in the configuration file.

In this case,  once the quota of  50 users is exhausted, the  server rejects all
foreign users  attempting to connect,  until at least  one client of  that class
disconnects and frees the spot for another.

---

Another common reason  for these messages is that you  were previously connected
to the server and lost your connection.
But the server hasn't noticed it yet.

As a  result, it detects  your attempt to  reconnect as a  duplicate connection,
which  is forbidden  if the  server permits  a maximum  of one  client from  any
particular address.

## The connection fails with the message “Connection Refused”!

No IRC server was listening for connections on the machine and/or port you tried
to connect to.

Make sure the server name and the port number are correct.

If the issue persists, the IRC server or the machine is having a problem.
Try to connect to a different server.

## The connection fails with the message “Unable to Resolve Server Name”!

A name server has failed to  convert the canonical name, such as irc.server.com,
into an IP address such as 256.10.2.78.

Either your local name  server or the one on which  the server's address resides
are out of order.

Your client sends your  query to your local name server, which  in turn looks up
the name  server that holds  the records of  the server's site  (server.com) and
then queries it for the IP address matching the canonical name you have given it
(irc.server.com).

If this happens with  all servers, it's definitely your local  server that has a
problem.

If your ISP can't fix it for a while, your options are either to use an off-site
name server, which requires  you to know a name server's IP  address, or to find
an IP address from an existing list of them.

The easier solution is to find the IP  addresses of the IRC servers you use most
and add them to your list separately.

If you don't know any, try asking on one of the other networks' help channel, or
try the network's website if there is one.

## The connection fails with the message “No Authorization”!

You may be trying to connect to a  foreign server, which accepts few or no users
from outside its domain.

---

Another explanation is name server failure.
The server may attempt to convert your IP address into a canonical host name.

But  some ISPs  have omitted  adding reverse  records for  their addresses,  not
considering it essential to smooth operation.
And the server may refuse to accept users whose IP address will not resolve to a
canonical host name.

To check whether your ISP has set up reverse DNS for your IP, execute this shell
command:

    $ dig +noall +answer -x <your IP>

It should contain a hostname.
If not, ask your ISP to set up reverse DNS for your IP.

##
## The server sends me the message “Illegal Nickname”!

You've selected a nickname that's already in use, or it contains an unacceptable
character.

Valid characters for nicknames include the characters in the following set:

    [a-zA-Z0-9\`^-|_[]{}]

The leading character cannot be a number or dash.

---

Note that two nicknames which seem to be different may still conflict.
Indeed, IRC is not case-sensitive: so `user` is the same as `UsEr`.

Besides, the following pairs of characters are confused by many servers:

    [ ↔ {
    ] ↔ }
    | ↔ \

Indeed, IRC  originated in  Scandinavia, and on  a Scandinavian  keyboard, those
keys correspond to the same keys (with/out the shift modifier).

---

If the nickname is valid and someone else is using your first choice, as well as
your  alternative nicknames,  the server  prompts you  to enter  a new  nickname
before it will accept you.

If you don't enter a new nickname soon enough, the server disconnects you with a
Ping timeout.

---

Some servers or networks may reject  nicknames that would be legitimate on other
servers, such as those with an underscore in them.

If you  can find nothing else  wrong with your  nickname, try using one  made up
entirely of letters.

## The server sends me the message “Nickname or Channel Temporarily Unavailable”!

You need to select a new nickname before the server accepts you.

---

The nickname was  recently in use by  someone who didn't sign  off "normally" as
seen from your server.
Maybe the user was disconnected by accident, and will reconnect soon.

Even  if the  user signed  off normally,  some servers  prevent the  use of  the
nickname for approximately 15 minutes.

---

You may change back  to your original nickname after the  nick delay expires and
the nickname becomes available again.

##
## I end up on a different server than the one I asked!

The server  you asked  to connect  to may  have been  taken down  permanently or
temporarily.
To spare the users the trouble of looking for another server, its administration
may have chosen to redirect them to a different server.

