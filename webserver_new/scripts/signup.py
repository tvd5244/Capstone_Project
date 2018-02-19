
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import UserAccount

print("""\
Content-Type: text/html
\r\n
""")

mail = fields.getvalue("mail")
pwd = fields.getvalue("pwd")

if mail is None or pwd is None: 
	print(open("scripts/signup.html", "r").read().replace("<?mail>", mail or "").replace("<?pwd>", pwd or ""))
else: 
	try: 
		user = UserAccount.create(mail, pwd)
		user.send_verify_email()
		user.commit()
	except: 
		print(open("scripts/signup_failure.html", "r").read())
	else: 
		print(open("scripts/signup_successful.html", "r").read().replace("<?mail>", mail))


