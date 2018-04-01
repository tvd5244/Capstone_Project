import datetime
import time

print("""\
Content-Type: text/event-stream\r\n\
Cache-Control: no-cache\r\n\
\r\n
""")


while True: 
	print(str(datetime.datetime.now()))
	time.sleep(1)

