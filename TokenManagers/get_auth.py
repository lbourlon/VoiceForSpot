from webbrowser import open
from http.server import BaseHTTPRequestHandler
import socketserver
            
class requestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><h1>It worked !</h1></html>")
    
    def do_GET(self):
        self.code = self.path[7:]
        #print(f"code : '{self.code}'")
        global global_code
        global_code = self.code

        self._set_response()

def fun_auth():
    port = 6789

    scopes = "user-modify-playback-state%20user-read-playback-state%20playlist-modify-public%20playlist-modify-private%20"
    client_id ="7f4c93f7c66c4df0b38ffadf72fd190d" # pass as argument to the function
    redirect_uri = f"http://localhost:{port}"

    open(f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}")

    with socketserver.TCPServer(("", port), requestHandler) as httpd:
        #print("serving at port", port)
        httpd.handle_request()

    #print(f"global_code = f{global_code}")
    return global_code

if __name__ == "__main__":
    fun_auth()