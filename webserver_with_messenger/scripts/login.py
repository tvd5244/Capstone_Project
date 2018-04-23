import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
import logs

script = "login"
mail = fields.getvalue("mail")
pwd = fields.getvalue("pwd")

session = Session.login(mail, pwd)
logs.print_line("login complete: " + str(session) + ".")
html_builder.begin_output()

if session is not None:

	status = "0"
	message = "Login successful"
	print(open("login_result.html", "r").read()
		.replace("<?script>", script)
		.replace("<?status>", status)
		.replace("<?message>", message))

else:
	status = "-1"
	message = "An error occurred while logging in"
	print(open("login_result.html", "r").read()
		.replace("<?script>", script)
		.replace("<?status>", status)
		.replace("<?message>", message))
