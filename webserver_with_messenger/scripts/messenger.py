import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
import sqlite3
import UserAccountSet
from UserAccountPropertySet import UserAccount
from Session import Session

print("""\
Content-Type: text/html
\r\n
""")

conn = sqlite3.connect("database.db")
c = conn.cursor()
session = Session.get_session()
user_id = session.get_account_id()
sender = c.execute('select mail from UserAccountSet where id = ' + str(user_id))
sender = str(sender.fetchone())[2:-3]
query = c.execute('select sender, message, timestamp from messages where recipient = "' + str(sender) + '"')
messages = ""
for msg in c:
	messages = messages + "<tr><td>" + msg[0] + "</td>"
	messages = messages + "<td>" + msg[1] + "</td>"
	messages = messages + "<td>" + msg[2] + "</td></tr>"
	
print(open("messenger_private.html", "r").read()
.replace("<?messages>", messages))
conn.close()
