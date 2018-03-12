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
	message = ""
	interests = fields.getvalue("interests")

	if interests is not None: 
		user.interests = interests
		user.commit()
		message = "changes have been committed."

	print(open("account_details.html").read().replace("<?mail>", user.mail or "unknown")).replace("<?program>", user.program or "unknown").replace("<?message>", message)


else: 
	print(open("error_must_login.html", "r").read())
		
