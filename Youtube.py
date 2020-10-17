import os
import pickle
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class YoutubeClient(object):
    def __init__(self):
        credentials = None

        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists('token.pickle'):
            print('Loading Credentials From File...')
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...\n')
                credentials.refresh(Request())
            else:
                print('Fetching New Token...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=['https://www.googleapis.com/auth/youtube.readonly']
                )

                # Runs a local server to get the credentials
                flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    authorization_prompt_message=''
                )

                credentials = flow.credentials

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as f:
                    print('Saving Credentials for Future use...')
                    pickle.dump(credentials, f)

        self.youtube = build(serviceName='youtube', version='v3', credentials=credentials)

    def get_video_ids(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        )

        response = request.execute()

        video_ids = []
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)

        return video_ids

    def get_artist_and_track(self, video_id):
        request = self.youtube.videos().list(
            part='snippet',
            id=video_id
        )

        response = request.execute()

        for title in response['items']:
            track = title['snippet']['title']

            # !!! IF YOUTUBE VIDEO TITLE DOESN'T INVOLVE THE BAND NAME !!!
            if not ' - ' in track:
                artist = title['snippet']['channelTitle']
                artist = artist.split(' - ')[0]
                track = (f"{artist} - {track}")

            # REMOVES SPECIALS CHARS FROM THE VIDEO NAME
            track = re.sub("[\(\[].*?[\)\]]", "", track)
            track = re.sub("\|", "", track)
            track = re.sub("Napalm Records", '', track)
            track = re.sub(' +', ' ', track)

            if ' - ' in track:
                artist = track.split(' - ')[0]
                title = track.split(' - ')[1]
            else:
                artist = None
                title = None

        return artist, title
