<<<<<<< HEAD
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

messageid = fields.getvalue("deletebox")
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("delete from messages where ID = " + str(messageid));
print(open("messenger_delete.html", "r").read())
conn.commit()
=======
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

messageid = fields.getvalue("deletebox")
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("delete from messages where ID = " + str(messageid));
print(open("messenger_delete.html", "r").read())
conn.commit()
>>>>>>> cfb83555628e86e8b96ca99b962658d593aacd1d
conn.close()