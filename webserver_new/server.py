
from http.server import HTTPServer, CGIHTTPRequestHandler

CGIHTTPRequestHandler.cgi_directories = ["/scripts"]

HTTPServer(("", 1025), CGIHTTPRequestHandler).serve_forever()
