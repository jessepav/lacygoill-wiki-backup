How to include the deck `bar` inside the deck `foo`?

Rename it like so:

    foo::bar

You can also drag and drop `bar` inside `foo` from the deck list.
But in general, the drag and drop is less accurate.

If I select the deck
`foo::bar` which cards will be shown?

The cards in the subdeck `bar` of the parent deck `foo`.

`foo` which cards will be shown?

The cards in the parent deck `foo`.

---

Decks can contain other decks, which allows you to organize decks into a tree.
Anki uses “::” to show different levels.
A deck  called “Chinese::Hanzi”  refers to a  “Hanzi” deck, which  is part  of a
“Chinese” deck.
If you  select “Hanzi” then only  the Hanzi cards  will be shown; if  you select
“Chinese” then all Chinese cards, including Hanzi cards, will be shown.
To place  decks into a  tree, you  can either name  them with “::”  between each
level, or drag and drop them from the deck list.
Decks that have been nested under another  deck (that is, that have at least one
“::”  in  their names)  are  often  called  subdecks,  and top-level  decks  are
sometimes called superdecks or parent decks.

Anki starts  with a deck called  “default”; any cards which  have somehow become
separated from other decks will go here.
Anki will hide the default deck if it contains no cards and you have added other
decks.
Alternatively, you may rename this deck and use it for other cards.

