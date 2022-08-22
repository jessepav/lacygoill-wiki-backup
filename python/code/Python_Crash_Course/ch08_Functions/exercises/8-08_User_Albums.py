# Purpose: Start  with your  program from  Exercise 8-7.   Write a  `while` loop
# that  allows users  to  enter an  album's  artist and  title.   Once you  have
# that  information, call  `make_album()` with  the user's  input and  print the
# dictionary that's  created.  Be sure  to include a  quit value in  the `while`
# loop.

# Reference: page 142 (paper) / 180 (ebook)

def make_album(artist, title, songs_number = None):
    album = {'artist': artist.title(), 'title': title.title()}
    if songs_number:
        album['number of songs'] = songs_number
    return album

while True:
    print(
        '\nPlease enter the name of an artist and their music album.'
        "\n(enter 'q' at any time to quit)"
    )

    artist = input('\nArtist: ')
    if artist == 'q':
        break

    title = input('Title: ')
    if title == 'q':
        break

    print('\n' + str(make_album(artist, title)))
#     Please enter the name of an artist and their music album.
#     (enter 'q' at any time to quit)
#
#     Artist: michael jackson
#     Title: thriller
#
#     {'artist': 'Michael Jackson', 'title': 'Thriller'}
#
#     Please enter the name of an artist and their music album.
#     (enter 'q' at any time to quit)
#
#     Artist: q
