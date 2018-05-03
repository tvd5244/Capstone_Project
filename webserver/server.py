
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
from email.utils import formatdate
import time
import datetime
import urllib.parse as parse


from scripts import database
#from scripts.UserAccountPropertySet import UserAccount 
import scripts.logs as logs

CONNECTION_TIMEOUT = 4

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

		logs.print_line("an SSE connection has been opened.")

		query = parse.parse_qs(parse.urlparse(self.path).query)
		ID1 = int(query["ID1"][0])
		ID2 = int(query["ID2"][0])
		conn = database.create_conn()
		conn.execute("""
create table if not exists Conversations2 (
	ID Integer primary key autoincrement, 
	ID1 Integer, 
	ID2 Integer, 
	message Text
)
"""		)
		logs.print_line("accessing: ========================> " + str(query["last_ID"]))
		last_ID = int(query["last_ID"][0]) or -1
		start_time = time.time()
		
		while not(self.wfile.closed) and (time.time() - start_time) < CONNECTION_TIMEOUT: 
			cursor = conn.cursor()
			res = cursor.execute("""
select message, ID 
from Conversations2 
where ID > ? 
and ((ID1 = ? and ID2 = ?) or (ID1 = ? and ID2 = ?)) 
order by ID asc
"""			, (last_ID, ID1, ID2, ID2, ID1, ))

			for (message, ID, ) in res: 
				last_ID = ID
				response = "id: " + str(last_ID) + "\n\ndata:" + str(message).replace("\r\n", "\n").replace("\n", "\\n").replace("\\", "\\\\") + "\n\n"
				logs.print_line("SSE sent: \"" + response + "\"")
				self.wfile.write(response.encode("UTF-8"))

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
