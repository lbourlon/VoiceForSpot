from http.server import BaseHTTPRequestHandler
import socketserver

PORT = 6789

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print(f"path : {self.path}")
        print(f"headers : {self.headers}")
        self._set_response()

handler = Handler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
