import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
from getAccountInfo import getAccountInfo
from updateInterests import updateInterests
import logs

html_builder.begin_output()

session = Session.get_session()

if session is not None: 
	user = UserAccount.get_account_by_id(session.get_account_id())
	accountInfo = getAccountInfo(user)
	interests = fields.getvalue("interests")
	message = ""

	if interests is not None: 
		user.interests = interests
		user.commit()
		updateInterests(user)
		message = "changes have been committed"
	
	print(open("account_details.html").read()
		.replace("<?name>", accountInfo[0] or "unknown")
		.replace("<?mail>", user.mail or "unknown")
		.replace("<?academic_program>", user.academic_program or "unknown")
		.replace("<?interests>", user.interests or "none")
		.replace("<?campus>", user.campus or "unknown")
		.replace("<?message>", message))

else: 
	print(open("error_must_login.html", "r").read())
		
