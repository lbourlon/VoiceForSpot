import cgi

print("Content-type: text/html; charset=utf-8\n")

html = """<html lang = "en">
<head>
    This is the head of the file
</head>

<Body>
    <p> 
      Click on this link to authenticate yourself in the spotify john app
    </p>

  <form method="get" action="https://accounts.spotify.com/authorize?client_id=7f4c93f7c66c4df0b38ffadf72fd190d&response_type=code&redirect_uri=https://localhost/confirmation.py&scope=user-modify-playback-state%20user-read-playback-state">
      <input type="submit" value="Authenticate on Spotify" />
  </form>
    
</Body>
</html>
"""

print(html)

#https://www.youtube.com/watch?v=FBW4HTd8ilA&t=16s&ab_channel=FormationVid%C3%A9o