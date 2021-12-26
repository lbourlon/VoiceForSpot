# This Object is in charge of the Spotify API communication,
# Doesn't handle Authentication.

import requests
import json
from secrets_ import client_id, client_secret_id
import base64
import datetime

import utility


from utility import responseDebugg
from TokenManagers.SpotifyTokenManager import SpotifyTokenManager

# Maybe use a dictionnary to store all the commands.
spotify_commands = ["play", "pause", "resume", "louder", "quieter", "mute", "blast"]

class SpotifyClient():
    """Spotify client class in charge of communicating with the API."""

    # spot_com_dict = {"play":self.play_song}
    def __init__(self):
        self.tokenManager = SpotifyTokenManager()

    def __str__(self):
        self.

    def execute_command(self, command_input):
        command = command_input[0]

        last_command = ""
        for word in command_input[1:]:
            last_command += word + " "

        if command == "play":
            self.play_song(song = last_command)

        elif command == "resume" or command == "pause" :
            self.resume_pause_song(option = command)
        
        elif command == "louder" or "quieter" or "mute" or "blast":
            self.set_volume(option = command)
        
        else :
            print("Command not found.")

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
        # device_list = self.get_list_of_devices(self.tokenManager.get_token())
        device_list = self.get_list_of_devices()
        
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
        # TODO : Check for active

        song_uri = self.get_song_uri(song)

        request_body = json.dumps({
            "uris": ["{}".format(song_uri)],
        })

        query = "https://api.spotify.com/v1/me/player/play"

        if(device_id): query += + "?device_id=" + device_id

        response = requests.put(
            query,
            data = request_body,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )
        
        responseDebugg(response, "Play Song")

    def resume_pause_song(self, option = None, device_id = None):
        """Method to resume / pause current song."""
        # dev_id = self.get_device_id('lbourlon')
        if option == "resume" :
            option = "play"

        query = f"https://api.spotify.com/v1/me/player/{option}"

        if(device_id): query += "?device_id=" + device_id

        response = requests.put(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )

        responseDebugg(response, "resume / start")

    def set_volume(self, option = None, device_id = None):
        """Method to set the volume of the active player."""
        devices = self.get_list_of_devices()
        dev = devices[0]

        current_volume = dev["volume_percent"]
        volume = ""

        # volume_dict {
        #     "mute":"0",
        #     "blast":"100",
        #     "louder": str(utility.get_new_volume(current_volume, "louder")),
        #     "quieter": str(utility.get_new_volume(current_volume, "quieter"))
        # }
        if option == "mute": volume = "0"
        elif option == "blast": volume = "100"
        elif option == "louder": volume = str(utility.get_new_volume(current_volume, "louder"))
        elif option == "quieter": volume = str(utility.get_new_volume(current_volume, "quieter"))



        query = f"https://api.spotify.com/v1/me/player/volume"

        if(device_id): query += "?device_id=" + device_id
        query += "?volume_percent=" + volume

        response = requests.put(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization":"Bearer {}".format(self.tokenManager.get_token())
            }
        )

        responseDebugg(response, "resume / start")
        # print (f"the device {name} has the volume {current_volume}")


        return