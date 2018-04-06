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
user = c.execute('select mail from UserAccountSet where id = ' + str(user_id))
user = str(user.fetchone())[2:-3]
query = c.execute('select sender, subject, timestamp, message, ID from messages where recipient = "' + str(user) + '"')
messages = ""
hidescript = ""
for msg in c:
	messages = messages + "<tr><td>" + msg[0] + "</td>"
	messages = messages + '<td><a href="javascript:toggledisplay(msg' + str(msg[4]) + ');">' + msg[1] + '</a></td>'
	messages = messages + "<td>" + msg[2] + "</td></tr>"
	messages = messages + '<tr id="msg' + str(msg[4]) +'" style="display: none;"><td colspan="3">' + msg[3] + '</td></tr>'
	hidescript = hidescript + 'msg' + str(msg[4]) + ' = document.getElementById("msg' + str(msg[4]) +'");\r\n'
	
print(open("messenger_private.html", "r").read()
.replace("<?messages>", messages)
.replace("<?hidescript>", hidescript))
conn.close()
