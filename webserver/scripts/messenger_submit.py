import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
import disable_auto_update_session; disable_auto_update_session.disable_auto_update_session()
from Session import Session
from UserAccountPropertySet import UserAccount
import database
import time
import logs

session = Session.get_session()
ID1 = fields.getvalue("ID1")
ID2 = fields.getvalue("ID2")
new_message = fields.getvalue("message")

print("""\
Content-Type: text/html
\r\n
""")

conn = database.create_conn()

conn.execute("""
create table if not exists Conversations2 (
	ID Integer primary key autoincrement, 
	ID1 Integer, 
	ID2 Integer, 
	message Text
)
""")

if ID1 is not None and ID2 is not None: 
	message = ""

	if new_message is not None: 
		logs.print_line("new message: from = " + str(ID1) + ", to = " + str(ID2) + ": " + new_message)
		conn.execute("""
insert into Conversations2 
(ID1, ID2, message) 
values (?, ?, ?)
"""		, (int(ID1), int(ID2), new_message, ))
		conn.commit()
		message = "sent at " + str(time.time()) + "."

	print(open("messenger_submit.html", "r").read()
		.replace("<?ID1>", ID1)
		.replace("<?ID2>", ID2)
		.replace("<?message>", message))

else: 
	print(open("error.html", "r").read())