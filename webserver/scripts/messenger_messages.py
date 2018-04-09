import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
import signal
import sys
import time

source = fields.getvalue("source")
done = False

def finish(): 
	global done

	done = True

signal.signal(signal.SIGTERM, finish)

print("""\
Content-Type: text/event-stream\r\n
Cache-Control: no-cache\r\n
Connection: keep-alive\r\n
\r\n
""")

if source is not None: 
	file = open(source, "r")

	while not done: 
		line = file.readline()

		if line != "":
			time.sleep(1)
			print("data:" + "hello world" + "\r\n")
			sys.stdout.flush()
			

else: 
	print(open("error.html", "r").read())

