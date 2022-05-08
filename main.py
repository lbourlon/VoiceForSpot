# This is the main program, in charge of initializing the different components.

import SpotifyClient
#import voiceRec

#import localClient.AuthenticationServer as auth
isDebugging = True


if __name__ == '__main__':
    # Initializing TokenManagers
    # TODO

    # Initializing clients
    spot_client = SpotifyClient.SpotifyClient()
    spot_client.play_song("Le metro Bazar et bémols")

"""

    # Program main loop
    while(True):
        recognized_audio = voiceRec.recognize2()

        # Go to next loop if recognition failed.
        if(recognized_audio == "Nope"): continue

        voiceRec.command_parser(recognized_audio, spot_client)"""
