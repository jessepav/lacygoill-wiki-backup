# ?

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
## Why can't I see the default deck in the deck list?

Probably because it doesn't contain any card, and you have created other decks.

##
## How to install the most recent version of Anki?

Follow the instructions at: <https://apps.ankiweb.net/>

    $ tar xjf Downloads/anki-2.1.8-amd64.tar.bz2
    $ cd anki-2.1.8-linux-amd64
    $ sudo make install

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
## What are the 4 standard note types which comes with Anki by default?

    Basic

Has `Front` and `Back` fields, and will create one card.
Text you  enter in `Front` will  appear on the front  of the card, and  text you
enter in `Back` will appear on the back of the card.

    Basic (and reversed card)

Like  `Basic`,  but  creates *two*  cards  for  the  text  you enter:  one  from
front→back and one from back→front.

    Basic  (optional reversed  card)

This is a front→back card, and optionally a back→front card.
To do this, it has a third field called “Add Reverse”.
If you enter any text into that field, a reverse card will be created.

    Cloze

This makes it easy to select text and turn it into a cloze deletion (e.g.,  “Man
landed on the moon in […]” → “Man landed on the moon in 1969”).

## Why is it a good idea to create a separate note type for each broad topic I'm studying?

To prevent Anki from detecting false duplicates.
Indeed, when  Anki checks for  duplicates, it only  compares other notes  of the
same type.

Suppose that you use the same note type to learn French, and capital cities.
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

## How to create a new note type?

Press `C-S-n`, or click the buttons:

   - Tools
   - Manage Note Types

Then, click the buttons:

   - Add
   - Manage Note Types

Select an existing note type; it will serve as a base for cloning.
Finally, give it a name.

---

From the `Manage Note Types` window, your new note type can be:

   - renamed (`Rename`)
   - deleted (`Delete`)
   - given new fields (`Fields...`)
   - given new card types (`Cards...`)

##
## How to make Anki generate several cards from a given note?

Add a new card type to the currently used note type.

Press  `C-l` or  click on  the `Cards...`  button, then  click on  `Options` and
finally `Add Card Type...`.

Repeat the process as many times as desired.

## My note type has 2 card types.
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
