import datetime
import time
import sys

print("""\
Content-Type: text/event-stream\r\n\
Cache-Control: no-cache\r\n\
\r\n\
""")


while True: 
	print("data:" + str(datetime.datetime.now()) + "\n\n")
	sys.stdout.flush()
	time.sleep(1)

