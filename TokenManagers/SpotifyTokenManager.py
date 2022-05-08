import requests
import json
import datetime
from base64 import b64encode as b64
import os

import sys
sys.path.append('../')  # So that the working directory is the same as main.
from TokenManagers.retrieve_server import get_master_token

class SpotifyTokenManager():
    def __init__(self):
        self.dateformat = "%d/%m/%Y at %H:%M and %S,%f seconds"

        self.path_master_token = "./secrets/master_token.json"
        self.path_to_client_ids = "./secrets/client_ids.json"
        self.path_refresh_token = "./secrets/refresh_token.json"
        self.path_access_token = "./secrets/access_token.json"

        json_creds = self.read_json_file(self.path_to_client_ids)
        client_id = json_creds["client_id"]
        client_secret = json_creds["client_secret_id"]

        self.enc_creds = b64(f"{client_id}:{client_secret}".encode()).decode()

        if not os.path.isfile(self.path_master_token):
            master_code = get_master_token(client_id)
            self.write_json_file(self.path_master_token, {"spotify":master_code})
 

        #if the refresh token exists we assume the user is authorized
        if not os.path.isfile(self.path_refresh_token): 
            self.get_authorization()


    def get_authorization(self):
        """ Method uses the Spotify Authorization Code Flow"""
        authorization_code = self.read_json_file(self.path_master_token)["spotify"]

        # From here we send a query containing the authorization_code and user info to spotify
        request_body = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri":"http://localhost:6789"
        }

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(
            query,
            data=request_body,
            headers = {"Authorization": f"Basic {self.enc_creds}"}
        )

        if response.status_code not in range(200, 299) or 'error' in response.json():
            print (f"Request failed, info: {response.text}")


        resp_data = response.json() # contains : { "access_token", "token_type", "scope", "expires_in", "refresh_token"}

        self.write_json_file(self.path_refresh_token, resp_data["refresh_token"])
        resp_data.pop("refresh_token")
        self.write_token_file(resp_data, self.path_access_token)


    def refresh(self):
        """ Method updates the current access token.
            Requires a valid refresh_token    
        """

        refresh_token = self.read_json_file(self.path_refresh_token)

        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        query = "https://accounts.spotify.com/api/token"
        response = requests.Response

        try:
            response = requests.post(
            query,
            data=request_body,
            headers = {"Authorization": f"Basic {self.enc_creds}"}
        )
        except Exception:
            print(f"Exception caught while refreshing token : {Exception}")

        finally:
            if response.status_code not in range(200, 299) or 'error' in response.json():
                print (f"Authorization failed, info: {response.text}")

        response_data = response.json()
        self.write_token_file(response_data)
        
        return

    def get_token(self):
        """To be used by the spotify client to send the token"""
        token_data = self.read_json_file(self.path_access_token)
        now = datetime.datetime.now()
        expires_at = datetime.datetime.strptime(token_data['expires_at'], self.dateformat)

        isExpired = now >= expires_at

        if isExpired:
            self.refresh()
            token_data = self.read_json_file(self.path_access_token)

        return token_data['access_token']

    def write_token_file(self, token_data, token_file):
        """ Expects dict containing : { "access_token", "token_type", "scope", "expires_in"}  """

        now = datetime.datetime.now()

        expires_in = token_data['expires_in'] #seconds
        expires_at = now + datetime.timedelta(seconds=expires_in)

        token_data.pop("expires_in")
        token_data['expires_at'] = expires_at.strftime(self.dateformat)
        
        self.write_json_file(token_file, token_data)

    def read_json_file(self, file):
        # TODO: if expired, raise exception, if not returns the token
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
        return data

    def write_json_file(self, file, data):
        with open(file, "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
