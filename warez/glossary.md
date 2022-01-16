# m
## magnet

A URI scheme that defines the format of magnet links.

## magnet URI

A de  facto standard for identifying  files by their content,  via cryptographic
hash value rather than by their location.

      magnet URI
    v------------v
    magnet:?xt=URN
           │├┘ ├─┘
           ││  └ value of parameter
           │└ parameter (eXact Topic)
           └ start query string

         URN
    v----------v
    urn:btih:NSS
        ├──┘ ├─┘
        │    └ namespace-specific string (e.g. sha1 of file)
        └ namespace identifier (NID): BitTorrent Info-Hash

### Why is it so useful in p2p file sharing networks?

Authentication: it  gives the guarantee that  the retrieved resource is  the one
intended, regardless of how it was retrieved.

Decentralization: it doesn't require a central  authority to be issued (i.e. you
can compute  it locally, provided  you already have  the file identified  by the
URN).

Distribution: it can be  distributed as a search term (which  is easier to share
than a torrent file; less space, and can be embedded in any text file).

Reliability: it lets a  file be referred to without the  need for a continuously
available host.

##
# U
## URI

A unique sequence of characters that identifies a logical or physical resource.
It  can be  used to  identify anything,  including real-world  objects, such  as
people and  places, concepts,  or information  resources such  as web  pages and
books.

URIs include URLs and URNs.

It stands for: Uniform Resource Identifier.

## URL

A URI which provides a means  of locating and retrieving an information resource
on a network.

It stands for: Uniform Resource Locator.

## URN

A URI that uses the urn scheme.

It's  a  globally  unique  persistent   identifier  assigned  within  a  defined
namespace, meant to remain  available for a long period of  time, even after the
resource which it identifies ceases to exist or becomes unavailable.

It cannot be used to directly locate an item.
It doesn't need to be resolvable, as  it's simply a template that another parser
can use to find an item.

It stands for: Uniform Resource Name.
