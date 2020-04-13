



#1 Log into YouTube
#2 Grab our liked videos
#3 Create a new playlist
#4 Search for the song
#5 Add the song into the new spotify playlist

import json
import requests
from secrets import spotify_user_id, spotify_token

class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id

    #1 Log into YouTube
    def get_youtube_client(self):
        pass

    #2 Grab our liked videos
    def get_liked_vides(self):
        pass

    #3 Create a new playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "YouTube Liked Videos",
            "description": "All liked videos in YouTube",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
            
        )
        response_json = response.json()

        #Playlist id
        return response_json["id"]



    #4 Search for the song
    def get_spotify_url(self):
        pass

    #5 Add the song into the new spotify playlist
    def add_song_to_playlist(self):
        pass
