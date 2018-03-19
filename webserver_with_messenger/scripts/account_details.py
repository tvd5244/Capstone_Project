import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

session = Session.get_session()

if session is not None: 
	print("""\
Content-Type: text/html
\r\n
"""	)

	
	user = UserAccount.get_account_by_id(session.get_account_id())
	interests = fields.getvalue("interests")
	message = ""

	if interests is not None: 
		user.interests = interests
		user.commit()
		message = "changes have been committed."

	print(open("account_details.html").read()
		.replace("<?mail>", user.mail or "unknown")
		.replace("<?academic_program>", user.academic_program or "unknown")
		.replace("<?interests>", user.interests or "none.")
		.replace("<?message>", message))


else: 
	print(open("error_must_login.html", "r").read())
		
