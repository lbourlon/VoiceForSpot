# Voice4Spot

The idea was to make a vocal assistant that mostly interacts with Spotify.

This project was mostly done as a fun side project to learn about how to interact with webAPIs.
Especially when it comes to authentication, it uses the "Authorization Code Flow" for this :
https://developer.spotify.com/documentation/general/guides/authorization/code-flow/


At the moment for the first authentication it lauches opens a page in a browser for the
authentication, starts a local server to retrieve the response. Then handles the different
authentication tokens.

Features : search and play a certain music, resume/pause and volume control
