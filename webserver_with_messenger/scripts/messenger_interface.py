import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

session = Session.get_session()
target = fields.getvalue("target")

print("""\
Content-Type: text/html
\r\n
""")

if session is not None and target is not None:
	user = UserAccount.get_account_by_id(session.get_account_id())
	target = UserAccount.get_account_by_id(int(target))

	if target in user.get_friends(): 
		print(open("messenger.html", "r").read()
			.replace("<?source>", user.create_conversation_source(target)))
		user.commit()

	else: 
		print(open("error_messenger_not_friend.html", "r").read())

else: 
	print(open("error_must_login.html", "r").read())