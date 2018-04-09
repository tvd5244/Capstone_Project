from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
from email.utils import formatdate
import datetime
import time
from http import HTTPStatus

class Handler(CGIHTTPRequestHandler): 
	cgi_directories = ["/scripts"]

	def do_SSE(self): 
		self.wfile.write(("""\
HTTP/1.1 200 OK\r\n\
Date: """ + formatdate(timeval = time.mktime(datetime.datetime.now().timetuple()), localtime = False, usegmt = True) + """\r\n\
Content-Type: text/event-stream\r\n\
Cache-Control: no-cache\r\n\
Connection: keep-alive\r\n\
\r\n
""").encode("UTF-8"))

		while not(self.wfile.closed): 
			self.wfile.write(("data:" + str(datetime.datetime.now()) + "\n\n").encode("UTF-8"))
			self.wfile.flush()
			time.sleep(1)


	def do_GET(self): 
		if self.path == "/scripts/SSE.py": 
			self.do_SSE()
		else: 
			super().do_GET()


class Server(ThreadingMixIn, HTTPServer): 
	pass


Server(("", 8080), Handler).serve_forever()
