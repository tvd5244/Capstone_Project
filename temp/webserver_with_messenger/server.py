
from http.server import HTTPServer, CGIHTTPRequestHandler

class Handler(CGIHTTPRequestHandler): 
	cgi_directories = ["/scripts"]
	

HTTPServer(("", 8002), Handler).serve_forever()
