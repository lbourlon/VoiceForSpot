import requests
import json
from secrets_ import client_id, client_secret_id
import base64
import datetime

from utility import responseDebugg
from TokenManagers.SpotifyTokenManager import SpotifyTokenManager

class SpotifyClient():
    """A Spotify client class"""
    def __init__(self):
        self.tokenManager = SpotifyTokenManager()


    def get_list_of_devices(self):
        """Returns a list of active connected devices
        scopes : user-read-playback-state
        """

        query = "https://api.spotify.com/v1/me/player/devices"
        
        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )
        
        responseDebugg(response, "Device Search")
        device_list = response.json()["devices"]

        

        return device_list

    def get_device_id(self, device):
        """Returns a device id """
        device_list = self.get_list_of_devices(self.tokenManager.get_token())
        
        try:
            for e in self.list_of_devices:
                if (e["name"] == device):
                    return e["id"]
        except:
            #TODO (Léon) Make an exception for this (token errors too)
            print("coulnd't find any matching device")


    def get_song_uri(self, song_name):
        """ Gets song uri (first result)"""
        #TODO : addd the artist to the query
        query = "https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(
            song_name
        )

        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )

        responseDebugg(response, "Song Search")

        track_data = response.json()["tracks"]["items"]
        
        return track_data[0]["uri"]



    def play_song(self, song = None, device_id = None):
        """
        Plays the song on the specified device
        scopes : user-modify-playback-state
        """
        #TODO : Check for active

        song_uri = self.get_song_uri(song)
        

        request_body = json.dumps({
            "uris": ["{}".format(song_uri)],
            
        })

        query = "https://api.spotify.com/v1/me/player/play"

        if(device_id): query = query + + "?device_id=" + device_id

        response = requests.put(
            query,
            data = request_body,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )
        
        responseDebugg(response, "Play Song")
