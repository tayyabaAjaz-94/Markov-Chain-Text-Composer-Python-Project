import lyricsgenius

# Generate an API key and paste it here
genius = lyricsgenius.Genius("api-key-here")

def save_lyrics(songs, artist_name, album_name):
    for i in range(len(songs)):
        song_title = songs[i]
        song = genius.search_song(song_title, artist_name)
        lyrics = song.lyrics
        with open(f'songs/{"/".join(artist_name.split())}/{i+1}_{album_name}_{song_title.replace(" ", "-")}.txt', 'w') as f:
            f.writelines(lyrics.split('\\n'))

if __name__ == '__main__':
    songs = [
        'the box',
        'down below',
        'project dreams',
        'die young',
        'boom boom room',
        'high fashion',
        'roll dice',
        'war baby',
        'every season'
    ]
    save_lyrics(songs, 'roddy ricch', 'some-album')
