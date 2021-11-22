import SpotifyClient
import voiceRec

# import localClient.AuthenticationServer as auth

isDebugging = True


if __name__ == '__main__':

    spotifyClient = SpotifyClient.SpotifyClient()

    audio_escrito = voiceRec.recognize2()

    #spotifyClient.volume(option = "quieter")

    voiceRec.command_parser(audio_escrito, spotifyClient)


    


