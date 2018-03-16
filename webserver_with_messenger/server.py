
from http.server import HTTPServer, CGIHTTPRequestHandler

CGIHTTPRequestHandler.cgi_directories = ["/scripts"]

HTTPServer(("", 8002), CGIHTTPRequestHandler).serve_forever()
