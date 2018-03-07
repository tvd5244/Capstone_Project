
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session

mail = fields.getvalue("mail")
pwd = fields.getvalue("pwd")

session = Session.login(mail, pwd)

if session is not None: 
	print("""\
Content-Type: text/html
Set-Cookie: SESSION=""" + session.secret + """
\r\n
"""	)

	print(open("login_success.html", "r").read())

else: 
	print(open("login_failure.html", "r").read())

