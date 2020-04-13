#Created by WilliamOtieno

#1 Log into YouTube
#2 Grab our liked videos
#3 Create a new playlist
#4 Search for the song
#5 Add the song into the new spotify playlist

import json
import requests
import os


from secrets import spotify_user_id, spotify_token
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    #1 Log into YouTube
    def get_youtube_client(self):
        #Copied from youtube data api
        #Disable OAuthlib's HTTPS verification when running locally
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api.service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        #Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube data API
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials = credentials)

        return youtube_client

    #2 Grab our liked videos and create dictionary of important song info
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part = "snippet, contentDetails, statistics",
            myRating = "like"
        )
        response = request.execute()

        # collect each video and get important info
        for item in response["item"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://youtube.com/watch?v={}".format(item["id"])

            # use youtube_dl to collect the song name and artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download = False)
            song_name = video["track"]
            artist = video["artist"]

            # save all important info
            self.all_song_info[video_title] = {
                "youtube_url":youtube_url,
                "song_name":song_name,
                "artist":artist,

                # add the uri, easy to get song to put into playlist
                "spotify_uri":self.get_spotify_uri(song_name, artist)
            }



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
    def get_spotify_url(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(song_name, artist)
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["trakcs"]["items"]

        # only use the 1st song
        uri = songs[0]["uri"]

        return uri 

    #5 Add the song into the new spotify playlist
    def add_song_to_playlist(self):
        
        #populate our songs dictionary
        self.get_liked_videos()

        #collect all of uri

        #add all songs into new playlist
