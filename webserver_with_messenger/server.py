
from http.server import HTTPServer, CGIHTTPRequestHandler

CGIHTTPRequestHandler.cgi_directories = ["/scripts"]

HTTPServer(("", 80), CGIHTTPRequestHandler).serve_forever()
