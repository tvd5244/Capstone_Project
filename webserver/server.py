
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
from email.utils import formatdate
import time
import datetime
import urllib.parse as parse


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

		source = parse.parse_qs(parse.urlparse(self.path).query)["source"][0]
		file = open(source, "r")

		while not(self.wfile.closed): 
			self.wfile.write(("data:" + source + "\n\n").encode("UTF-8"))
			self.wfile.flush()
			time.sleep(1)


	def do_GET(self): 
		file = open("log.txt", "a")
		file.write(self.path + "\n")
		file.close()
		if self.path.startswith("/scripts/messenger_messages.py"): 
			self.do_SSE()
		else: 
			super().do_GET()


class Server(ThreadingMixIn, HTTPServer):
	pass

Server(("", 8002), Handler).serve_forever()
