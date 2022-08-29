# c
## card type

In  order for  Anki to  create cards  based on  a note,  you need  to give  it a
blueprint that says which  fields should be displayed on the front  or back of a
card and how; this blueprint is called a card type.

A card type is made of 3 sections:

   - a template for the front of the card
   - a template for the back of the card
   - a styling section to customize the appearance of both faces of all cards

## collection

All the material stored in Anki:

   - notes
   - note types
   - cards
   - decks
   - deck options
   - ...

##
# f
## field

A type of information used to create a note.

##
# n
## note

A set of related pieces of information necessary to create one or several cards.

## note type

Set of fields and card types.

##
# p
## parent deck

A top-level deck; also sometimes called superdeck.

Example:

    foo::bar
    │    │
    │    └ subdeck
    └ parent deck

##
# s
## subdeck

A deck that has  been nested under another deck (that is, that  has at least one
“::” in its name).

