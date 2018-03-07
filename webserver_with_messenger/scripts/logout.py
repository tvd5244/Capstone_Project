
from Session import Session

session = Session.get_session()

if session is not None: 
	session.logout()
	print(open("logout_success.html", "r").read())
else: 
	print(open("logout_failure.html", "r").read())


