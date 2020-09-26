import SpotifyClient
import voiceRec

#import localClient.AuthenticationServer as auth

isDebugging = True


if __name__ == '__main__':
    #song =  voiceRecognition()

    spotifyClient = SpotifyClient.SpotifyClient()

    song = voiceRec.recognize()
    
    #spotifyClient.play_song(song = song)
