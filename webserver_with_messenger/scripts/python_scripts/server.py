
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn


class Handler(CGIHTTPRequestHandler): 
	cgi_directories = ["/scripts"]
	

class Server(ThreadingMixIn, HTTPServer): 
	pass

Server(("", 8002), Handler).serve_forever()
