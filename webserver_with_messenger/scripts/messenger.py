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
sender = c.execute('select sender, message from messages where recipient = ' + str(user_id))
messages = ""
for msg in c
	messages = messages + "<
	
print(open("messenger_private.html", "r").read()
.replace("<?messages>", messages)
conn.close()
