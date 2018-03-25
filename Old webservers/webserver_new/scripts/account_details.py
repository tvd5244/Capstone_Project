import cgitb; cgitb.enable()
from Session import Session
from UserAccountVerifySet import UserAccount

session = Session.get_session()

if session is not None: 
	print("""\
Content-Type: text/html
\r\n
"""	)

	user = UserAccount.get_account_by_id(session.get_account_id())
	print(open("account_details.html").read().replace("<?mail>", user.mail or "unknown"))

else: 
	print(open("error_must_login.html", "r").read())
		
