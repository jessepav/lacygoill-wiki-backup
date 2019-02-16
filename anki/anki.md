# ?

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

##
# Deck
## I can't see the default deck in the deck list!

That's because it doesn't contain any card, and you have created other decks.

##
## How to install the most recent version of Anki?

Follow the instructions at: <https://apps.ankiweb.net/>

    $ tar xjf Downloads/anki-2.1.8-amd64.tar.bz2
    $ cd anki-2.1.8-linux-amd64
    $ sudo checkinstall

Make sure to give a valid version number during the installation.

## How to include the deck `bar` inside the deck `foo`?

Rename it like so:

    foo::bar

You can also drag and drop `bar` inside `foo` from the deck list.
But in general, the drag and drop is less accurate.

### What does this feature allow me to do?

Organizing decks into a tree of arbitrarily nested subdecks.

###
## Which cards will be shown, if I select the deck
### `foo::bar`?

The cards in the subdeck `bar` of the parent deck `foo`.

### `foo`?

The cards in the parent deck `foo`.

###
## Where does Anki put a card which somehow becomes separated from all decks?

In the default deck.

##
# Note
## Why is it a good idea to create a separate note type for each broad topic I'm studying?

To prevent Anki from detecting false duplicates.
Indeed, when  Anki checks for  duplicates, it only  compares other notes  of the
same type.

Suppose that you use the same type of note to learn French, and capital cities.
In  your french  deck, you  have  a note  whose  first field  contains the  word
“Orange”, and which generate cards for your french deck.
Now you want  to create another note,  whose first field also  contains the word
“Orange”, this time to generate cards in your capital cities deck.

It won't work, because Anki will detect  a duplicate note; i.e. 2 notes with the
same front; the first field will be highlighted in red.

## How to change the type of an existing note?

Click on the buttons:

   - `Browse` (or press `b`)
   - `Change Note Type...` – in the contextual menu (or press `C-S-m`)
   - `New note type:`

##
## How to make Anki generate several cards from a given note?

Add a new card type to the currently used type of note.

Press <kbd>C-l</kbd> or click on the  `Cards...` button, then click on `Options`
and finally `Add Card Type...`.

Repeat the process as many times as desired.

## My type of note has 2 card types.
### I've just used it to generate 2 cards.  Why does Anki only make me review one of them?

They're considered siblings, and so Anki has buried the second card until another day.

### How to make Anki place the generated cards into different decks?

Each card type has its own copy of an option called `Deck Override...`.

By default it's off.
Turn it on for every card type for  which the created card should be placed in a
different deck than the current one.

You can do so by clicking on the buttons:

   - `Options`
   - `Deck Override... (off)`

##
# Issues
## I can't install any plugin, because of a SSL connection error!

    SSLHandshakeError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)

Update Anki.

##
# TODO

Read this: <https://www.juliensobczak.com/write/2016/12/26/anki-scripting.html>
