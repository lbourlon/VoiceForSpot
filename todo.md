# Problems : 
- The authentication requires manual input
- The readme.md is pretty bad
- The way the voice recon is set up it only recognizes the command "play"
- Poor Secret storing
- "Access Revoked" isn't well managed


# General TODOs :
- The authentication should be run on a webserver where you can just log in
- Make the program accept one sentence inputs : 
 -- input1 : "Hey John, play Stairway To Heaven"
 -- input2 : "Hey John" + "play Stairway To Heaven"
- Maybe put the commands selection directly in voiceRec.py


# Spotify TODOs :
- Use "GET_playback_state" on SpotiClient https://developer.spotify.com/documentation/web-api/reference/#/operations/get-information-about-the-users-current-playback
- Authentication
- Simple: play, pause, volup, voldown, next song commands
- More complex : Playlists play

# Other Functionalities
- Simple : whether, certain alt-coin value?, Tell me a joke
- Complex : Youtube Interaction? see chromecast interaction?
- Time Consuming : put it on the rasbpi, with mini-screen / battery / speaker (JBL GO?)
    or use LCD crystal display ?  
- Change name for something better ("dude / dudette" ?)




