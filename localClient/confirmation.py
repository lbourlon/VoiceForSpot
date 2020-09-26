import cgi
import cgitb

#cgitb.enable()
#form = cgi.FieldStorage

print("Content-type: text/html; charset=utf-8\n")

html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>This is the second page of the website</title>
    </head>

    <form>
        <label for"code">Code here:</label><br>
        <input type="text" id="code" name="code"><br>
    </form>


<form>
    <label for="lname">Last name:</label><br>
  <input type="text" id="lname" name="lname">
</form>

    <body>
        <h1>heyo</h1>
        <p>if you're here its because the redirect worked corectly</p>
    </body>
</html>
"""

print(html)