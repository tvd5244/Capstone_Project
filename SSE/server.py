from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
import datetime
import time

class Handler(CGIHTTPRequestHandler): 
	cgi_directories = ["/scripts"]

	def do_SSE(self): 
		self.wfile.write("""\
HTTP/1.1 200 OK\r\n
Date: """ + str(datetime.datetime.now()) + """
Content-Type: text/event-stream\r\n\
Cache-Control: no-cache\r\n\
Connection: keep-alive\r\n\
\r\n
""".encode("UTF-8"))

		while not(self.wfile.closed): 
			self.wfile.write(("data:" + str(datetime.datetime.now())).encode("UTF-8"))
			time.sleep(1)


	def do_GET(self): 
		if self.path == "/scripts/SSE.py": 
			self.do_SSE()
		else: 
			super().do_GET()


class Server(ThreadingMixIn, HTTPServer): 
	pass


Server(("", 8080), Handler).serve_forever()
