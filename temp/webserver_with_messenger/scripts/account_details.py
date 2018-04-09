import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
from getAccountInfo import getAccountInfo
from updateInterests import updateInterests

session = Session.get_session()

if session is not None: 
	print("""\
Content-Type: text/html
\r\n
"""	)

	
	user = UserAccount.get_account_by_id(session.get_account_id())
	interests = fields.getvalue("interests")
	message = ""
	accountInfo = getAccountInfo(user.mail)

	if interests is not None: 
		user.interests = interests
		user.commit()
		updateInterests(session.get_account_id(), interests)
		message = "changes have been committed."

	if accountInfo:
		print(open("account_details.html").read()
			.replace("<?name>", accountInfo[0])
			.replace("<?mail>", user.mail or "unknown")
			.replace("<?academic_program>", accountInfo[4] or "unknown")
			.replace("<?campus>", accountInfo[3] or "unknown")
			.replace("<?interests>", user.interests or "none.")
			.replace("<?about_me>", "")
			.replace("<?classes>", "")
			.replace("<?message>", message))
	else:
		print(open("account_details.html").read()
			.replace("<?name>", "unknown")
			.replace("<?mail>", user.mail or "unknown")
			.replace("<?academic_program>", user.academic_program or "unknown")
			.replace("<?campus>", user.campus or "unknown")
			.replace("<?interests>", user.interests or "none.")
			.replace("<?about_me>", "")
			.replace("<?classes>", "")
			.replace("<?message>", message))
			


else: 
	print(open("error_must_login.html", "r").read())
		
