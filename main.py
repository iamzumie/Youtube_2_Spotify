from Youtube import YoutubeClient
from Spotify import SpotifyClient
from spotipy import SpotifyException
import sys
import secrets

youtube = YoutubeClient()
spotipy = SpotifyClient()

def run():
    while True:
        video_ids = youtube.get_video_ids(secrets.playlist_id) # get a list of videos from my youtube playlist

        # Print out the songs from youtube
        print("Youtube playlist:")

        songs_not_found = []
        for video_id in video_ids:
            artist, track = youtube.get_artist_and_track(video_id)  # Extract artist & title name

            # If artist and track has been found in spotify add them and return Spotify track id
            spotify_songs_to_add = []
            if artist and track:
                print(f"> {artist} - {track}")
                track_id = spotipy.get_spotify_id(artist, track)

                if track_id == None:
                    songs_not_found.append([artist, track])
                spotify_songs_to_add.append(track_id)
            else:
                pass


        print() # Show songs that can't be added
        for song_not_found in songs_not_found:
            print(f'Cannot add song: {song_not_found[0]} - {song_not_found[1]}')

        # Asks if you want to add all the songs to spotify:
        while True:
            want_do_add = int(input("\nDo you want to add all the songs to spotify? 1 = yes, 0 = no: "))
            if want_do_add == 1:
                break
            else:
                sys.exit()


        # Add the songs one by one in spotify:
        spotify_added_songs = []
        for song in spotify_songs_to_add:
            artist, track = spotipy.get_song_name(song)
            if spotipy.already_liked(song) == [True]:
                print(f"Skipping song {artist} - {track}: {song}..")
            else:
                print(f"Adding song {artist} - {track}: {song}..")
                spotipy.put_in_liked(song)
                spotify_added_songs.append([artist,track])


        # Returns a list of all the songs which are added
        if len(spotify_added_songs) != 0:
            print("\nGet a list of added liked tracks on Spotify:")
        for track in spotify_added_songs:
            print(f"-   {track[0]} - {track[1]}")

        # Show how many songs are added
        if len(spotify_added_songs) != 1:
            print(f"\n{len(spotify_added_songs)} Songs added!")
        else:
            print(f"\n{len(spotify_added_songs)} Song added!")
        sys.exit()

# RUN
if __name__ == '__main__':
    while True:
        try:
            run()
        except SpotifyException:
            spotipy.refresh()
            print('Refreshed token')
