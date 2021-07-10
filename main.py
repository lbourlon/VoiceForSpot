import SpotifyClient
import voiceRec

# import localClient.AuthenticationServer as auth

isDebugging = True


if __name__ == '__main__':
    #song =  voiceRecognition()

    spotifyClient = SpotifyClient.SpotifyClient()

    rec = voiceRec.recognize()

    if(rec == "" or rec == None):
        rec = "Beneath The Brine"


    spotifyClient.play_song(song = rec)

    


