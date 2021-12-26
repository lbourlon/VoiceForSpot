import http.server
import ssl
import socket
import socketserver


def run_secure_socketed_server():
    port = 4433
    address = ("", port)
    httpd = http.server.HTTPServer(address, http.server.SimpleHTTPRequestHandler)

    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)

    httpd.serve_forever() 
    pass


def run_cgi_server():
    port = 7777 
    address = ("", port)

    server = http.server.HTTPServer
    
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/"]


    httpd = server(address, handler)
    
    print(f"Server starded on the port {port}")
    
    httpd.serve_forever()


run_cgi_server()