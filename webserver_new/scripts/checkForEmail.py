
import sqlite3
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import UserAccount

print("""\
Content-Type: text/html
\r\n
""")

conn = sqlite3.connect("accounts.db")
mail = "shauby19@gmail.com"

#mail = fields.getvalue("mail")

data = checkEmail(conn, mail)

def checkEmail(conn, mail):
	query = conn.executescript("""
	select mail from UserAccountSet where mail = ?
	"""	, mail).fetchone()[0]

	if query is None:
		print("query = ")
		print(query)
		return false # email does not exist in database
	else:
		print("nope")
		return true # email already exists, dont let user register with this email