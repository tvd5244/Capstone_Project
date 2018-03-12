
from http.server import HTTPServer, CGIHTTPRequestHandler

CGIHTTPRequestHandler.cgi_directories = ["/scripts"]

HTTPServer(("", 8001), CGIHTTPRequestHandler).serve_forever()
