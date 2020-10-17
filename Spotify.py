import secrets
import time
import requests
from spotipy import oauth2


class SpotifyClient(object):
    def __init__(self):
        sp_oauth = oauth2.SpotifyOAuth(
                    client_id=secrets.client_id,
                    client_secret=secrets.client_secret,
                    redirect_uri=secrets.redirect_uri,
                    scope=secrets.scopes
                    )
        token_info = sp_oauth.get_cached_token()
        self.oauth = sp_oauth
        self.token_info = token_info

        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            response = input('Paste the above link into your browser, then paste the redirect url here: ')

            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)

            token = token_info['access_token']

        else:
            now = int(time.time())
            print(str(((token_info)['expires_at'] - now) // 60) + ' min')
            token = token_info['access_token']
        self.token = token

    def refresh(self):
        global token_info, sp

        if self.oauth.is_token_expired(self.token_info):
            token = token_info['access_token']
        else:
            token_info = self.oauth.refresh_access_token(self.token_info['refresh_token'])


    def get_spotify_id(self, artist, track):
        """Search For the Song"""
        url = f"https://api.spotify.com/v1/search?q={artist,track}&type=track"

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()

        results = response_json["tracks"]["items"]

        # only use the first song
        if results:
            # Take the first track in the list we come across
            return results[0]["id"]


    def already_liked(self, song_id):
        query = (f"https://api.spotify.com/v1/me/tracks/contains?ids={song_id}")
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()

        return response_json

    def put_in_liked(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )

        return response.ok

    def get_song_name(self, id):
        query = (f"	https://api.spotify.com/v1/tracks/{id}")
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        for artists in response_json['artists']:
            artist = artists['name']
        track = response_json['name']

        return artist, track
