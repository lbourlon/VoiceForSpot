# This is the main program, in charge of initializing the different components.

import SpotifyClient
import voiceRec

# import localClient.AuthenticationServer as auth

isDebugging = True


if __name__ == '__main__':
    # Initializing TokenManagers
    # TODO

    # Initializing clients
    spotifyClient = SpotifyClient.SpotifyClient()

    # Program main loop
    while(True):
        recognized_audio = voiceRec.recognize2()

        # Go to next loop if recognition failed.
        if(recognized_audio == "Nope"): continue

        voiceRec.command_parser(recognized_audio, spotifyClient)
