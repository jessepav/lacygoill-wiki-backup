# ?

Each type  of note can have  one or more card  types; when you add  a note, Anki
will create one card for each card type.
Each card type has two templates, one for the question and one for the answer.
In  the above  French  example, we  wanted  the recognition  card  to look  like
this:

    Q:  Bonjour
    A:  Hello
        Page #12

To do  this, we  can set  the question and  answer templates  to:

    Q:  {{French}}
    A:  {{English}}<br>
        Page  #{{Page}}

By surrounding a  field name in double  curly brackets, we tell  Anki to replace
that section with the actual information in the field.
Anything not surrounded by curly brackets remains the same on each card.
(For instance, we  don’t have to type  “Page #” into the Page  field when adding
material – it’s added automatically to every  card.) <br> is a special code that
tells Anki to move to the next line; more details are available in the templates
section.

# ?

Anki allows you to create different types of notes for different material.
Each type of note has its own set of fields and card types.
It’s a  good idea to  create a  separate note type  for each broad  topic you’re
studying.
In the  above French example,  we might create a  note type called  “French” for
that.
If we wanted to  learn capital cities, we could create a  separate note type for
that as well, with fields such as “Country” and “Capital City”.
When Anki checks for duplicates, it only compares other notes of the same type.
Thus if you add a capital city called “Orange” using the capital city note type,
you  won’t see  a duplicate  message when  it  comes time  to learn  how to  say
“orange” in French.
When you  create a new  collection, Anki  automatically adds some  standard note
types to it.
These note types are provided to make Anki easier for new users, but in the long
run it’s  recommended you  define your own  note types for  the content  you are
learning.
The standard note types are as follows:

    Basic

Has Front and Back fields, and will create one card.
Text you enter in Front will appear on the front of the card, and text you enter
in Back will appear on the back of the card.

    Basic (and reversed card)

Like  Basic, but creates two  cards for the  text you
enter: one from front→back and one from back→front.

    Basic  (optional reversed  card)

This is a front→back card, and optionally a back→front card.
To do this,  it has a third field  called “Add Reverse.”  If you  enter any text
into that field, a reverse card will be created.
More information about this is available in the Cards and Templates section.

    Cloze

A note type which makes it easy to select text and turn it into a cloze deletion
(e.g.,  “Man landed on the moon in […]” → “Man landed on the moon in 1969”).
More information is available in the cloze deletion section.

To add your own note types and modify  existing ones, you can use Tools → Manage
Note Types from the main Anki window.

---

    Note

Notes and note types are common to  your whole collection rather than limited to
an individual deck.
This means you  can use many different  types of notes in a  particular deck, or
have different cards generated from a particular note in different decks.
When you add  notes using the Add window,  you can select what note  type to use
and  what deck  to use,  and these  choices are  completely independent  of each
other.
You can  also change the  note type of some  notes after you’ve  already created
them.

##
# How to install the most recent version of anki?

Follow the instructions at: <https://apps.ankiweb.net/>

    $ tar xjf Downloads/anki-2.1.8-amd64.tar.bz2
    $ cd anki-2.1.8-linux-amd64
    $ sudo checkinstall

Make sure to give a valid version number during the installation.

# How to include the deck `bar` inside the deck `foo`?

Rename it like so:

    foo::bar

You can also drag and drop `bar` inside `foo` from the deck list.
But in general, the drag and drop is less accurate.

## What does this feature allow me to do?

Organizing decks into a tree of arbitrarily nested subdecks.

##
# Which cards will be shown, if I select the deck
## `foo::bar`?

The cards in the subdeck `bar` of the parent deck `foo`.

## `foo`?

The cards in the parent deck `foo`.

##
# Where does anki put a card which somehow becomes separated from all decks?

In the default deck.

##
# Issues
## I can't see the default deck in the deck list!

That's because it doesn't contain any card, and you have created other decks.

## I can't install any plugin, because of a SSL connection error!

    SSLHandshakeError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)

Update anki.

##
# TODO

Read this: <https://www.juliensobczak.com/write/2016/12/26/anki-scripting.html>
