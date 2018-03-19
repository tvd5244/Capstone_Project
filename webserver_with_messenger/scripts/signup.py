
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
import UserAccountSet
from UserAccountPropertySet import UserAccount

print("""\
Content-Type: text/html
\r\n
""")

mail = fields.getvalue("mail")
pwd = fields.getvalue("pwd")

if mail is None or pwd is None: 
	print(open("signup.html", "r").read().replace("<?mail>", mail or "").replace("<?pwd>", pwd or ""))
else: 
	try: 
		user = UserAccount.create(mail, pwd)
		user.send_verify_email()
		user.commit()
	except UserAccountSet.ACCOUNT_ALREADY_EXISTS: 
		message = "<?mail> has already been registered"
		print(open("signup_verify_result.html", "r").read()
			.replace("<?message>", message)
			.replace("<?mail>", mail))
	else: 
		message = "To finish the sign-up process, please click the verification link sent to <?mail>"
		print(open("signup_verify_result.html", "r").read()
			.replace("<?message>", message)
			.replace("<?mail>", mail))


