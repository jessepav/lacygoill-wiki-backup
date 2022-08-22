# Purpose: Write  a  function called  `make_album()`  that  builds a  dictionary
# describing a music album.   The function should take in an  artist name and an
# album title, and it should return  a dictionary containing these two pieces of
# information.   Use  the  function  to  make  three  dictionaries  representing
# different albums.  Print  each return value to show that  the dictionaries are
# storing the album information correctly.
#
# Use `None` to  add an optional parameter to `make_album()`  that allows you to
# store the number of  songs on an album.  If the calling  line includes a value
# for the number of songs on an album, add that value to the album's dictionary.
# Make at least  one new function call  that includes the number of  songs on an
# album.

# Reference: page 142 (paper) / 180 (ebook)

def make_album(artist, title, songs_number = None):
    album = {'artist': artist.title(), 'title': title.title()}
    if songs_number:
        album['number of songs'] = songs_number
    return album

print(make_album(artist='michael jackson', title='thriller'))
print(make_album(artist='whitney houston', title='the bodyguard'))
print(make_album(artist='shania twain', title='come on over'))
#     {'artist': 'Michael Jackson', 'title': 'Thriller'}
#     {'artist': 'Whitney Houston', 'title': 'The Bodyguard'}
#     {'artist': 'Shania Twain', 'title': 'Come On Over'}

#                                                 v-------------v
print(make_album(artist='iggy pop', title='free', songs_number=10))
#     {'artist': 'Iggy Pop', 'title': 'Free', 'number of songs': 10}
#                                             ^-------------------^
