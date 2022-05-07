import requests
import json
import datetime
import base64
import os


import sys
sys.path.append('../')  # So that the working directory is the same as main.

from secrets_for_the_app import client_id, client_secret_id

class SpotifyTokenManager():
    def __init__(self):
        self.dateformat = "%d/%m/%Y at %H:%M and %S,%f seconds"

        self.path_to_spotify_refresh_token = "./secrets/SpotifyRefreshToken.json"
        self.path_to_spotify_token = "./secrets/SpotifyToken.json"
        self.path_to_secrets_for_login = "./secrets/secrets_for_login.json"
        path_to_secrets = "./secrets"

        #if the refresh token exists we assume the user is authorized
        if not os.path.isfile(self.path_to_spotify_refresh_token): 
            self.get_authorization()


    def get_authorization(self):
        """ Method uses the Spotify Authorization Code Flow

            # TODO : Make this work from a webserver
            Click on the link below, login, the return url will contain a 'GET' method passing "code" as a parameter
            that's the one time use the 'authorization_code', paste it below 
        """
        with open(self.path_to_secrets_for_login,'r') as file:
            secrets = json.load(file)

        authorization_code = secrets["spotify"]

        # From here we send a query containing the authorization_code and user info to spotify
        request_body = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri":"http://localhost:6789"
        }

        
        client_creds = f"{client_id}:{client_secret_id}"
        encoded_creds64 = base64.b64encode(client_creds.encode())

        query = "https://accounts.spotify.com/api/token"

        try:
            response = requests.post(
                query,
                data=request_body,
                headers = {
                    "Authorization": f"Basic {encoded_creds64.decode()}"
                }
            )

        except Exception as exeption_name:
            print(f"Exception caught while authorizing the application : {exeption_name}")

        finally:
            if response.status_code not in range(200, 299) or 'error' in response.json():
                print (f"Authorization failed, info: {response.text}")

        #if it works the response will contain a refresh_token, that needs to be kept as well as the first access_token data
        response_data = response.json()  # contains : { "access_token", "token_type", "scope", "expires_in", "refresh_token"}

        print(response_data)
        refresh_token = response_data["refresh_token"]
        with open(self.path_to_spotify_refresh_token, 'w') as jsonFile:
            json.dump(refresh_token, jsonFile)

        response_data.pop("refresh_token")

        write_token_file(response_data, self.path_to_spotify_token)

        return

    def refresh(self):
        """ Method updates the current spotify token.
            Requires a valid refresh_token    
        """

        refresh_token = read_token_file(self.path_to_spotify_refresh_token)

        print(refresh_token)

        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        client_creds = f"{client_id}:{client_secret_id}"
        encoded_creds64 = base64.b64encode(client_creds.encode())

        query = "https://accounts.spotify.com/api/token"
        response = requests.Response

        try:
            response = requests.post(
            query,
            data=request_body,
            headers = {
                "Authorization": f"Basic {encoded_creds64.decode()}"
            }
        )
        except Exception:
            print(f"Exception caught while refreshing token : {Exception}")
            print(response.reason)
            print('\n\nyahoo\n')

        finally:
            if response.status_code not in range(200, 299) or 'error' in response.json():
                print (f"Authorization failed, info: {response.text}")

        response_data = response.json()
        write_token_file(response_data)
        
        return

    def get_token(self):
        token_data = read_token_file(self.path_to_spotify_token)
        now = datetime.datetime.now()
        expires_at = datetime.datetime.strptime(token_data['expires_at'], self.dateformat)

        isExpired = now >= expires_at

        if isExpired:
            self.refresh()
            token_data = read_token_file(self.path_to_spotify_token)

        return token_data['access_token']

    def remove_authorization(self):
        if os.path.isfile(self.path_to_spotify_refresh_token): 
            os.remove(self.path_to_spotify_refresh_token)


def write_token_file(token_data, path_to_file):
    """ Expects dict containing : { "access_token", "token_type", "scope", "expires_in"}  """

    now = datetime.datetime.now()

    expires_in = token_data['expires_in'] #seconds
    expires_at = now + datetime.timedelta(seconds=expires_in)

    token_data.pop("expires_in")
    token_data['expires_at'] = expires_at.strftime("%d/%m/%Y at %H:%M and %S,%f seconds")
    

    with open(path_to_file, 'w') as jsonFile:
        json.dump(token_data, jsonFile)

def read_token_file(file):
    # TODO: if expired, raise exception, if not returns the token
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data
