
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
from email.utils import formatdate
import time
import datetime
import urllib.parse as parse


#from scripts import database
#from scripts.UserAccountPropertySet import UserAccount 
import scripts.logs as logs

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

		query = parse.parse_qs(parse.urlparse(self.path).query)
		source = UserAccount.get_account_by_id(query["source"])
		destination = UserAccount.get_account_by_id(query["destination"]
		conn = database.create_conn()

		while not(self.wfile.closed): 
			self.wfile.write(("data:" + "hello world" + "\n\n").encode("UTF-8"))
			self.wfile.flush()
			time.sleep(1)

		logs.print_line("an SSE connection has been closed.")

	def do_GET(self): 
		logs.print_line("request: " + self.path)
		if self.path.startswith("/scripts/messenger_messages.py"): 
			self.do_SSE()
		else: 
			super().do_GET()


class Server(ThreadingMixIn, HTTPServer):
	pass

Server(("", 8002), Handler).serve_forever()
