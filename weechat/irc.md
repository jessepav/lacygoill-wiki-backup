# Where does the term 'relay' in 'Internet Relay Chat' come from?

Let's  say Jack  wishes to  send a  message to  Jill, but  their machines  don't
connect directly, instead:

   - Jack is connected to the server A
   - Jill is connected to the server B
   - the servers A and B are connected

Therefore, Jack can make  use of the indirect route that  exists between him and
Jill.

What Jack does is send server A a message.
In this  message, he will tell  server A the message's  final destination (Jill)
and its contents.
Server A is aware  of the existence of Jill, although she's  not connected to it
directly, and it knows that she's connected to server B.
It therefore forwards — or RELAYS — the  message to server B, which in turn sees
that the recipient is one of its own  clients and sends the message to Jill, who
can then read it.
Server A also adds the identity of  the client sending it (Jack) before relaying
it, so the recipient knows who it's from.

# Why do most IRC networks use several servers?

To allow people to connect to a server close to them.

This gives the user a faster connection; he or she is using a nearby server, and
the faster and  more powerful connection of the organization  running the server
carries traffic between users.

A network  of servers acts a  bit like a  postal service:
the servers carry  the "mail" from city  to city in big, fast  vehicles, and the
user just drops off the message at the local server.

# Is IRC case-sensitive?

No.

`user` is the same as `UsEr`.
`#chan` is the same as `#ChAn`.
