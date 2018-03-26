import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
from getAccountInfo import getAccountInfo

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
	#if(accountInfo):
	#	user.academic_program = accountInfo[4]
	#	user.commit()

	if interests is not None: 
		user.interests = interests
		user.commit()
		message = "changes have been committed."

	print(open("account_details.html").read()
		.replace("<?mail>", user.mail or "unknown")
		.replace("<?name>", accountInfo[0] or "unknown")
		.replace("<?academic_program>", accountInfo[4] or "unknown")
		.replace("<?campus>", accountInfo[3] or unknown)
		.replace("<?interests>", user.interests or "none.")
		.replace("<?message>", message))


else: 
	print(open("error_must_login.html", "r").read())
		
