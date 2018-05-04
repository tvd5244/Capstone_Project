import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

html_builder.begin_output()
session = Session.get_session()
ID = fields.getvalue("ID")


if session is not None:
	user = UserAccount.get_account_by_id(session.get_account_id())

	if ID is not None: 
		print(open("messenger.html", "r").read().replace("<?ID1>", str(user.ID)).replace("<?ID2>", str(ID)))
	else: 
		print(open("error_messenger_not_friend.html", "r").read())

else: 
	print(open("error_must_login.html", "r").read())