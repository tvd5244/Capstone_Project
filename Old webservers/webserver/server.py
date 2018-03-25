from http.server import *

server = HTTPServer(("", 80), CGIHTTPRequestHandler).serve_forever()
