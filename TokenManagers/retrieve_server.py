from http.server import BaseHTTPRequestHandler
import socketserver

PORT = 6789

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        print("_set_response")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><h1>It worked !</h1></html>")
    

    def do_GET(self):
        print('do_GET')
        self.code = self.path[7:]
        print(f"code : '{self.code}'")
        #print(f"headers : {self.headers}")
        self._set_response()

handler = Handler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)

    httpd.handle_request()
